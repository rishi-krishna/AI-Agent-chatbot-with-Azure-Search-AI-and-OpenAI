export interface Citation {
  source_file: string;
  source_title: string;
  content_snippet: string;
  relevance_score: number | null;
}

export interface ChatResponse {
  reply: string;
  citations: Citation[];
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  loading?: boolean;
}
