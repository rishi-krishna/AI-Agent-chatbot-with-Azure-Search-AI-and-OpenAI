using System.Text.Json.Serialization;

namespace CooChat.Api.Models;

public sealed class AppSettings
{
    public string AzureSearchEndpoint { get; set; } = "https://coo-chat-search.search.windows.net";
    public string AzureSearchIndexName { get; set; } = "coo-help-chunks";
    public string AzureSearchApiKey { get; set; } = "YOUR_AZURE_SEARCH_API_KEY";
    public string AzureSearchApiVersion { get; set; } = "2024-07-01";

    public string AzureOpenAIEndpoint { get; set; } = "https://your-openai-resource.openai.azure.com/";
    public string AzureOpenAIApiKey { get; set; } = "YOUR_AZURE_OPENAI_API_KEY";
    public string AzureOpenAIApiVersion { get; set; } = "2024-02-15-preview";
    public string AzureOpenAIEmbeddingDeployment { get; set; } = "text-embedding-ada-002";
    public string AzureOpenAIChatDeployment { get; set; } = "gpt-4o";

    public int TopK { get; set; } = 5;
    public int CitationSnippetLength { get; set; } = 200;
}

public sealed class ChatRequest
{
    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;
}

public sealed class Citation
{
    [JsonPropertyName("source_file")]
    public string SourceFile { get; set; } = string.Empty;

    [JsonPropertyName("source_title")]
    public string SourceTitle { get; set; } = string.Empty;

    [JsonPropertyName("content_snippet")]
    public string ContentSnippet { get; set; } = string.Empty;

    [JsonPropertyName("relevance_score")]
    public double? RelevanceScore { get; set; }
}

public sealed class ChatResponse
{
    [JsonPropertyName("reply")]
    public string Reply { get; set; } = string.Empty;

    [JsonPropertyName("citations")]
    public List<Citation> Citations { get; set; } = new();
}

public sealed class SearchChunk
{
    public string Content { get; set; } = string.Empty;
    public string SourceFile { get; set; } = string.Empty;
    public string SourceTitle { get; set; } = string.Empty;
    public int StartLine { get; set; }
    public int EndLine { get; set; }
    public double? RelevanceScore { get; set; }
}
