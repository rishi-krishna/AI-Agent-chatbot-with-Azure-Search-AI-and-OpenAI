# Help Pack (Story 1)

Approved COO help content used for RAG. Add or edit Markdown files here; the indexing pipeline will chunk and index them into Azure AI Search.

## Conventions

- One topic per file (e.g. `approvals.md`, `reports-dashboard.md`).
- Use clear headings (H1 = title, H2 = sections).
- Include **screen/section names** and **navigation paths** so the bot can guide users.
- Keep paragraphs short for better chunking.

## File naming

Use kebab-case: `topic-name.md`. The pipeline uses the filename as source metadata for citations.
