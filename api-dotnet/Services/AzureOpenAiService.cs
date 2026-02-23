using System.Text;
using System.Text.Json;
using CooChat.Api.Models;
using Microsoft.Extensions.Options;

namespace CooChat.Api.Services;

public sealed class AzureOpenAiService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly AppSettings _settings;
    private readonly ILogger<AzureOpenAiService> _logger;

    private const string SystemPrompt =
        "You are a helpful assistant for the COO (Chief Operating Office) application. " +
        "Answer only using the provided help content. If the answer is not in the context, say so and suggest using " +
        "the in-app navigation or contacting support. When guiding users to a screen, mention the exact menu path " +
        "(e.g. 'Go to Approvals in the main menu' or 'Reports -> Report Library'). Keep answers concise and cite the source document when relevant.";

    public AzureOpenAiService(
        IHttpClientFactory httpClientFactory,
        IOptions<AppSettings> settings,
        ILogger<AzureOpenAiService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _settings = settings.Value;
        _logger = logger;
    }

    public async Task<List<float>> GetEmbeddingAsync(string query, CancellationToken cancellationToken)
    {
        var endpoint = _settings.AzureOpenAIEndpoint.TrimEnd('/');
        var url =
            $"{endpoint}/openai/deployments/{_settings.AzureOpenAIEmbeddingDeployment}/embeddings?api-version={_settings.AzureOpenAIApiVersion}";

        var payload = JsonSerializer.Serialize(new { input = query });
        using var request = new HttpRequestMessage(HttpMethod.Post, url)
        {
            Content = new StringContent(payload, Encoding.UTF8, "application/json")
        };
        request.Headers.Add("api-key", _settings.AzureOpenAIApiKey);

        var client = _httpClientFactory.CreateClient();
        using var response = await client.SendAsync(request, cancellationToken);
        var body = await response.Content.ReadAsStringAsync(cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            throw new InvalidOperationException(
                $"Azure OpenAI embedding call failed ({(int)response.StatusCode}): {body}");
        }

        using var doc = JsonDocument.Parse(body);
        var embeddingArray = doc.RootElement
            .GetProperty("data")[0]
            .GetProperty("embedding")
            .EnumerateArray();

        var vector = new List<float>();
        foreach (var item in embeddingArray)
        {
            vector.Add((float)item.GetDouble());
        }

        return vector;
    }

    public async Task<string> ChatWithContextAsync(string context, string userMessage, CancellationToken cancellationToken)
    {
        var endpoint = _settings.AzureOpenAIEndpoint.TrimEnd('/');
        var url =
            $"{endpoint}/openai/deployments/{_settings.AzureOpenAIChatDeployment}/chat/completions?api-version={_settings.AzureOpenAIApiVersion}";

        var payloadObject = new
        {
            messages = new object[]
            {
                new
                {
                    role = "system",
                    content = $"{SystemPrompt}\n\nRelevant help content:\n\n{context}"
                },
                new
                {
                    role = "user",
                    content = userMessage
                }
            },
            max_tokens = 1024,
            temperature = 0.3
        };

        var payload = JsonSerializer.Serialize(payloadObject);
        using var request = new HttpRequestMessage(HttpMethod.Post, url)
        {
            Content = new StringContent(payload, Encoding.UTF8, "application/json")
        };
        request.Headers.Add("api-key", _settings.AzureOpenAIApiKey);

        var client = _httpClientFactory.CreateClient();
        using var response = await client.SendAsync(request, cancellationToken);
        var body = await response.Content.ReadAsStringAsync(cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            throw new InvalidOperationException(
                $"Azure OpenAI chat call failed ({(int)response.StatusCode}): {body}");
        }

        using var doc = JsonDocument.Parse(body);
        var choices = doc.RootElement.GetProperty("choices");
        if (choices.GetArrayLength() == 0)
        {
            return string.Empty;
        }

        var message = choices[0].GetProperty("message");
        if (message.TryGetProperty("content", out var contentElement))
        {
            return contentElement.GetString() ?? string.Empty;
        }

        _logger.LogWarning("Chat completion response did not include content.");
        return string.Empty;
    }
}
