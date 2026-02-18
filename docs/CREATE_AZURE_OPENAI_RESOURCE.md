# Create an Azure OpenAI Resource (So Deployments Are OpenAI, Not Cognitive)

If every new deployment ends up as **Cognitive Services** (cognitiveservices.azure.com), you are using an **Azure AI / Cognitive Services** resource. This app needs a **dedicated Azure OpenAI** resource so the endpoint is **openai.azure.com**.

---

## Step 1: Create the correct resource in Azure Portal

1. Go to **https://portal.azure.com** and sign in.
2. Click **Create a resource** (or search in the top bar).
3. In the search box, type **Azure OpenAI** (not "Azure AI Services" and not "Cognitive Services").
4. In the results, choose **Azure OpenAI** (the one whose description says it’s for OpenAI models and has the OpenAI logo).
5. Click **Create**.
6. Fill in:
   - **Subscription** and **Resource group** (e.g. same as your other resources).
   - **Region:** e.g. East US.
   - **Name:** e.g. `my-coo-openai` (this will become `https://my-coo-openai.openai.azure.com`).
   - **Pricing tier:** Standard S0.
7. Click **Review + create** → **Create**.
8. When it finishes, click **Go to resource**.

You now have a **dedicated Azure OpenAI** resource. Its endpoint will be **`https://<your-name>.openai.azure.com`**, not cognitiveservices.

---

## Step 2: Get the endpoint and key

1. On the Azure OpenAI resource page, go to **Keys and Endpoint** (under Resource management).
2. Copy:
   - **Endpoint** (e.g. `https://my-coo-openai.openai.azure.com/`) → use in `.env` as `AZURE_OPENAI_ENDPOINT`.
   - **KEY 1** → use in `.env` as `AZURE_OPENAI_API_KEY`.

---

## Step 3: Create deployments in Azure OpenAI Studio (not AI Studio)

1. Open **https://oai.azure.com** (this is **Azure OpenAI Studio**).
2. At the top, make sure you select the **Azure OpenAI** resource you just created (the one whose endpoint is **openai.azure.com**). Do **not** select a Cognitive Services or “Azure AI Services” resource.
3. In the left menu, go to **Deployments**.
4. Click **+ Create new deployment**:
   - **Embedding:** Model `text-embedding-ada-002`, Deployment name e.g. `text-embedding-ada-002` → Create.
   - **Chat:** Model `gpt-4o`, Deployment name e.g. `gpt-4o` → Create.

Those deployments will be on **openai.azure.com** and will work with this app.

---

## Step 4: Use them in `.env`

In your project root `.env`:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-AZURE-OPENAI-RESOURCE-NAME.openai.azure.com/
AZURE_OPENAI_API_KEY=paste-key-1-here
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
```

The URL **must** contain **openai.azure.com**. If it contains **cognitiveservices**, you are still pointing at the wrong resource.

---

## If your Azure OpenAI resource has “no quota”

New Azure OpenAI resources often start with **no quota** (or very low). You need to request access and/or quota.

### Option A: Request access to Azure OpenAI (first-time)

1. Go to **https://aka.ms/oai/access**.
2. Fill in the form (subscription, use case, etc.) and submit.
3. Wait for approval (can be quick or a few days). Once approved, your subscription gets base quota.

### Option B: Request quota increase (Portal)

1. In **Azure Portal**, open your **Azure OpenAI** resource.
2. In the left menu, look for **Quota** or **Usage and quotas** (or search “Quotas” in the portal top bar).
3. Open **Quotas** and find **Azure OpenAI** (or “AI Services”) for your subscription and region.
4. Select the quota line (e.g. “Total TPM” or the model you need) → **Request quota increase** (or “New quota request”).
5. Enter the requested limit and a short justification (e.g. “COO chatbot RAG – embedding + gpt-4o, low traffic”).
6. Submit. Some increases are auto-approved; others are reviewed (minutes to a few days).

### Option C: Try another region

- Create a **new** Azure OpenAI resource in a **different region** (e.g. **Sweden Central**, **East US 2**, **West Europe**) where quota is often available.
- In **https://oai.azure.com**, switch to that resource and create deployments there.
- Use that resource’s endpoint and key in `.env`.

### Option D: Use an existing resource that already has quota

- If you already have an Azure OpenAI resource that shows quota (e.g. **rishi-mlrlkb5c-eastus2** in eastus2), use **that** resource:
  - In **https://oai.azure.com** select that resource.
  - Create the **embedding** and **chat** deployments there (so they exist on openai.azure.com for that resource).
  - Set `.env` to that resource’s **openai.azure.com** endpoint and key and deployment names.

See **docs/QUOTA_OPENAI.md** for more detail.

---

## Summary

| You want                         | Do this |
|----------------------------------|--------|
| Deployments to work with this app | Create a **Azure OpenAI** resource (Portal → “Azure OpenAI”), then create deployments in **https://oai.azure.com** for that resource. |
| Avoid “Cognitive only”           | Do **not** use “Azure AI Services” / “Cognitive Services” for this app. Create the **Azure OpenAI** resource as above and use only that endpoint in `.env`. |
