using CooChat.Api.Models;
using CooChat.Api.Services;
using CooChat.Api.Utils;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);
var dotEnvPath = Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, "..", ".env"));
DotEnvLoader.LoadIfExists(dotEnvPath);

builder.Services.Configure<AppSettings>(builder.Configuration.GetSection("CooChat"));
builder.Services.PostConfigure<AppSettings>(settings =>
{
    settings.AzureSearchEndpoint = Environment.GetEnvironmentVariable("AZURE_SEARCH_ENDPOINT") ?? settings.AzureSearchEndpoint;
    settings.AzureSearchIndexName = Environment.GetEnvironmentVariable("AZURE_SEARCH_INDEX_NAME") ?? settings.AzureSearchIndexName;
    settings.AzureSearchApiKey = Environment.GetEnvironmentVariable("AZURE_SEARCH_API_KEY") ?? settings.AzureSearchApiKey;
    settings.AzureSearchApiVersion = Environment.GetEnvironmentVariable("AZURE_SEARCH_API_VERSION") ?? settings.AzureSearchApiVersion;

    settings.AzureOpenAIEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? settings.AzureOpenAIEndpoint;
    settings.AzureOpenAIApiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? settings.AzureOpenAIApiKey;
    settings.AzureOpenAIApiVersion = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_VERSION") ?? settings.AzureOpenAIApiVersion;
    settings.AzureOpenAIEmbeddingDeployment =
        Environment.GetEnvironmentVariable("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") ?? settings.AzureOpenAIEmbeddingDeployment;
    settings.AzureOpenAIChatDeployment =
        Environment.GetEnvironmentVariable("AZURE_OPENAI_CHAT_DEPLOYMENT") ?? settings.AzureOpenAIChatDeployment;

    if (int.TryParse(Environment.GetEnvironmentVariable("AZURE_SEARCH_TOP_K"), out var topK))
    {
        settings.TopK = topK;
    }

    if (int.TryParse(Environment.GetEnvironmentVariable("CITATION_SNIPPET_LENGTH"), out var snippetLen))
    {
        settings.CitationSnippetLength = snippetLen;
    }
});

var configOrigins = builder.Configuration.GetSection("Cors:Origins").Get<string[]>() ?? Array.Empty<string>();
var envOrigins = Environment.GetEnvironmentVariable("CORS_ORIGINS");
var corsOrigins = !string.IsNullOrWhiteSpace(envOrigins)
    ? envOrigins.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
    : configOrigins;

if (corsOrigins.Length == 0)
{
    corsOrigins = new[] { "http://localhost:4200" };
}

builder.Services.AddCors(options =>
{
    options.AddPolicy("DefaultCors", policy =>
    {
        policy.SetIsOriginAllowed(origin =>
            corsOrigins.Contains(origin, StringComparer.OrdinalIgnoreCase) ||
            origin.EndsWith(".azurewebsites.net", StringComparison.OrdinalIgnoreCase))
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials();
    });
});

builder.Services.AddHttpClient();
builder.Services.AddScoped<AzureOpenAiService>();
builder.Services.AddScoped<AzureSearchService>();

var app = builder.Build();

app.UseCors("DefaultCors");

app.MapPost("/chat", async (
    ChatRequest request,
    AzureSearchService searchService,
    AzureOpenAiService openAiService,
    IOptions<AppSettings> appSettings,
    ILogger<Program> logger,
    CancellationToken cancellationToken) =>
{
    if (string.IsNullOrWhiteSpace(request.Message))
    {
        return Results.BadRequest(new { detail = "message is required" });
    }

    List<SearchChunk> chunks;
    try
    {
        chunks = await searchService.SearchChunksAsync(request.Message, cancellationToken);
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Retrieval failed");
        return Results.Json(new { detail = $"Retrieval failed: {ex.Message}" }, statusCode: 502);
    }

    var context = string.Join("\n\n---\n\n", chunks.Select(c => $"[{c.SourceFile}] {c.Content}"));
    if (string.IsNullOrWhiteSpace(context))
    {
        return Results.Ok(new ChatResponse
        {
            Reply = "I couldn't find relevant help content for that. Try rephrasing or use the main menu to explore Approvals, Reports, or Settings.",
            Citations = new List<Citation>()
        });
    }

    string reply;
    try
    {
        reply = await openAiService.ChatWithContextAsync(context, request.Message, cancellationToken);
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "LLM failed");
        return Results.Json(new { detail = $"LLM failed: {ex.Message}" }, statusCode: 502);
    }

    var snippetLen = appSettings.Value.CitationSnippetLength;
    var citations = chunks.Select(c => new Citation
    {
        SourceFile = c.SourceFile,
        SourceTitle = c.SourceTitle,
        ContentSnippet = c.Content.Length > snippetLen
            ? c.Content[..snippetLen] + "..."
            : c.Content,
        RelevanceScore = c.RelevanceScore
    }).ToList();

    return Results.Ok(new ChatResponse
    {
        Reply = reply,
        Citations = citations
    });
});

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.Run();
