"""
Chunk help-pack Markdown for RAG.
Uses semantic boundaries (headers) and a max token/chars limit with overlap.
"""
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Chunk:
    """A single chunk with metadata for citation."""
    content: str
    source_file: str
    source_title: str
    start_line: int
    end_line: int


# Approximate: 1 token ~ 4 chars for English
CHUNK_MAX_CHARS = 800
CHUNK_OVERLAP_CHARS = 100
HEADER_PATTERN = re.compile(r"^#{1,6}\s+.+$", re.MULTILINE)


def _extract_title(lines: list[str]) -> str:
    """First H1 line as title, else filename."""
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip().lstrip("# ").strip()
    return ""


def _split_into_blocks(lines: list[str]) -> list[tuple[int, int, list[str]]]:
    """Split by headers; each block is (start_1based, end_1based, lines)."""
    blocks: list[tuple[int, int, list[str]]] = []
    current: list[str] = []
    start = 1
    for i, line in enumerate(lines, start=1):
        if HEADER_PATTERN.match(line.strip()) and current:
            blocks.append((start, i - 1, current))
            current = []
            start = i
        current.append(line)
    if current:
        blocks.append((start, len(lines), current))
    return blocks


def _split_block_if_large(
    block_lines: list[str], start_line: int
) -> list[tuple[int, int, list[str]]]:
    """Split a block by size with overlap; return (start, end, lines) sub-blocks."""
    text = "".join(block_lines)
    if len(text) <= CHUNK_MAX_CHARS:
        return [(start_line, start_line + len(block_lines) - 1, block_lines)]

    sub_blocks: list[tuple[int, int, list[str]]] = []
    acc: list[str] = []
    acc_len = 0
    line_idx = 0
    chunk_start = start_line

    for j, line in enumerate(block_lines):
        line_len = len(line) + 1
        if acc_len + line_len > CHUNK_MAX_CHARS and acc:
            end_line = start_line + line_idx - 1
            sub_blocks.append((chunk_start, end_line, acc))
            # Overlap: keep last overlap chars
            overlap_text = "".join(acc)
            if len(overlap_text) > CHUNK_OVERLAP_CHARS:
                overlap_text = overlap_text[-CHUNK_OVERLAP_CHARS:]
            # Start next chunk with overlap (simplified: one line back)
            prev_lines = acc[-3:] if len(acc) >= 3 else acc
            acc = list(prev_lines)
            acc_len = sum(len(l) + 1 for l in acc)
            line_idx = j - len(prev_lines)
            chunk_start = start_line + line_idx
        acc.append(line)
        acc_len += line_len
        line_idx = j + 1

    if acc:
        sub_blocks.append((chunk_start, start_line + len(block_lines) - 1, acc))
    return sub_blocks


def chunk_file(file_path: Path) -> Iterator[Chunk]:
    """Yield chunks from a single Markdown file."""
    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    title = _extract_title(lines)
    source_file = file_path.name

    for start, end, block_lines in _split_into_blocks(lines):
        for s, e, sub_lines in _split_block_if_large(block_lines, start):
            content = "".join(sub_lines).strip()
            if not content:
                continue
            yield Chunk(
                content=content,
                source_file=source_file,
                source_title=title or source_file,
                start_line=s,
                end_line=e,
            )


def chunk_help_pack(help_pack_dir: Path) -> Iterator[Chunk]:
    """Yield chunks from all .md files in help pack (except README)."""
    for path in sorted(help_pack_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        yield from chunk_file(path)
