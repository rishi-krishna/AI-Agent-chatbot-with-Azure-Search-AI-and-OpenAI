# Fix 502: DeploymentNotFound (embedding or chat)

If the API returns **502** and the API terminal shows **DeploymentNotFound** or **404** for embeddings or chat, either the deployment name in your `.env` does not match Azure, or you are using the wrong type of resource.

## Cognitive Services vs Azure OpenAI (important)

This app uses **Azure OpenAI** (endpoint like `https://something.openai.azure.com`). It does **not** use **Azure AI / Cognitive Services** (endpoint like `https://something.cognitiveservices.azure.com`).

- If your screenshot or portal shows **Target URI** with **cognitiveservices** in the URL, that is a **different** service. Deployments there are not visible to the Azure OpenAI API.
- You must create embeddings (and chat) in **Azure OpenAI** and set `AZURE_OPENAI_ENDPOINT` in `.env` to the **openai.azure.com** URL, not the cognitiveservices one.
- In **Azure OpenAI Studio** (https://oai.azure.com), pick the resource whose endpoint is `*.openai.azure.com`, then create deployments (embedding + chat) there.

**If you changed `.env` to use the Cognitive Services URL:** change it back. Use the **Azure OpenAI** endpoint only (see below).

### What to put in `.env` for Azure OpenAI

- **AZURE_OPENAI_ENDPOINT** must be the **Azure OpenAI** endpoint, for example:
  - `https://rishi-mlrlkb5c-eastus2.openai.azure.com/`
- It must contain **openai.azure.com** in the URL. It must **not** be a `cognitiveservices.azure.com` URL.
- To get the correct URL: Azure Portal → your **Azure OpenAI** resource (resource type "Azure OpenAI") → **Keys and Endpoint** → copy the **Endpoint** value. Use that in `.env`.

## Your current error

- **Resource:** `rishi-mlrlkb5c-eastus2.openai.azure.com`
- **Requested deployment:** `text-embedding-ada-002`
- **Azure says:** This deployment does not exist on that resource.

So on **rishi-mlrlkb5c-eastus2** there is no deployment whose name is exactly `text-embedding-ada-002`. You must use the **exact** name that exists in Azure.

## Steps to fix

1. Open **Azure OpenAI Studio**: https://oai.azure.com
2. At the top, switch to the resource **rishi-mlrlkb5c-eastus2** (same as in your `AZURE_OPENAI_ENDPOINT`).
3. In the left menu, go to **Deployments**.
4. Find the row that uses an **embedding** model (e.g. text-embedding-ada-002 or text-embedding-3-small). Look at the **Deployment name** column (e.g. `embedding`, `ada-002`, or something else you chose).
5. Open your **project root** `.env` file (folder `Coochat_curser`, not inside `api`).
6. Set the embedding deployment to that **exact** name:
   ```env
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=the-exact-name-from-step-4
   ```
   For example, if the deployment name in Studio is `embedding`, use:
   ```env
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=embedding
   ```
7. Save `.env`. Restart the API (Ctrl+C, then run `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` again from the `api` folder).
8. Try the chat again.

If you see **LLM failed** with DeploymentNotFound later, do the same for the **chat** deployment: find its name in Deployments and set `AZURE_OPENAI_CHAT_DEPLOYMENT=` to that exact name in `.env`.
