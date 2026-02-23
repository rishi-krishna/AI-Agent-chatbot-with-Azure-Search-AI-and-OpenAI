using System.Text;
using System.Text.Json;
using CooChat.Api.Models;
using Microsoft.Extensions.Options;

namespace CooChat.Api.Services;

public sealed class AzureSearchService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly AzureOpenAiService _openAiService;
    private readonly AppSettings _settings;

    public AzureSearchService(
        IHttpClientFactory httpClientFactory,
        AzureOpenAiService openAiService,
        IOptions<AppSettings> settings)
    {
        _httpClientFactory = httpClientFactory;
        _openAiService = openAiService;
        _settings = settings.Value;
    }

    public async Task<List<SearchChunk>> SearchChunksAsync(string query, CancellationToken cancellationToken)
    {
        var vector = await _openAiService.GetEmbeddingAsync(query, cancellationToken);

        var endpoint = _settings.AzureSearchEndpoint.TrimEnd('/');
        var url =
            $"{endpoint}/indexes/{_settings.AzureSearchIndexName}/docs/search?api-version={_settings.AzureSearchApiVersion}";

        var payloadObject = new
        {
            search = "*",
            top = _settings.TopK,
            select = "content,source_file,source_title,start_line,end_line",
            vectorQueries = new object[]
            {
                new
                {
                    kind = "vector",
                    vector,
                    fields = "content_vector",
                    k = _settings.TopK
                }
            }
        };

        var payload = JsonSerializer.Serialize(payloadObject);
        using var request = new HttpRequestMessage(HttpMethod.Post, url)
        {
            Content = new StringContent(payload, Encoding.UTF8, "application/json")
        };
        request.Headers.Add("api-key", _settings.AzureSearchApiKey);

        var client = _httpClientFactory.CreateClient();
        using var response = await client.SendAsync(request, cancellationToken);
        var body = await response.Content.ReadAsStringAsync(cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            throw new InvalidOperationException(
                $"Azure Search query failed ({(int)response.StatusCode}): {body}");
        }

        using var doc = JsonDocument.Parse(body);
        if (!doc.RootElement.TryGetProperty("value", out var valueElement) || valueElement.ValueKind != JsonValueKind.Array)
        {
            return new List<SearchChunk>();
        }

        var chunks = new List<SearchChunk>();
        foreach (var item in valueElement.EnumerateArray())
        {
            var chunk = new SearchChunk
            {
                Content = GetString(item, "content"),
                SourceFile = GetString(item, "source_file"),
                SourceTitle = GetString(item, "source_title"),
                StartLine = GetInt(item, "start_line"),
                EndLine = GetInt(item, "end_line"),
                RelevanceScore = GetNullableDouble(item, "@search.score")
            };

            chunks.Add(chunk);
        }

        return chunks;
    }

    private static string GetString(JsonElement item, string propertyName)
    {
        if (item.TryGetProperty(propertyName, out var prop) && prop.ValueKind == JsonValueKind.String)
        {
            return prop.GetString() ?? string.Empty;
        }
        return string.Empty;
    }

    private static int GetInt(JsonElement item, string propertyName)
    {
        if (!item.TryGetProperty(propertyName, out var prop))
        {
            return 0;
        }

        return prop.ValueKind switch
        {
            JsonValueKind.Number when prop.TryGetInt32(out var val) => val,
            JsonValueKind.String when int.TryParse(prop.GetString(), out var val) => val,
            _ => 0
        };
    }

    private static double? GetNullableDouble(JsonElement item, string propertyName)
    {
        if (!item.TryGetProperty(propertyName, out var prop))
        {
            return null;
        }

        return prop.ValueKind switch
        {
            JsonValueKind.Number when prop.TryGetDouble(out var val) => val,
            JsonValueKind.String when double.TryParse(prop.GetString(), out var val) => val,
            _ => null
        };
    }
}
