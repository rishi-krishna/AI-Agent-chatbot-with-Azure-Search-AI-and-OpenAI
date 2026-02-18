# Azure OpenAI: No Quota – What to Do

If your Azure OpenAI resource shows **“no quota”** or you can’t create deployments, use one of the options below.

---

## 1. Request access (first time)

If your subscription has never used Azure OpenAI:

1. Go to **https://aka.ms/oai/access**.
2. Sign in and complete the form (subscription, company, use case).
3. Submit. Approval can take from a few hours to a few business days.
4. After approval, create or open your Azure OpenAI resource and try creating a deployment again.

---

## 2. Request a quota increase (Portal)

1. Go to **https://portal.azure.com**.
2. In the top search bar, type **Subscriptions** and open your subscription.
3. In the left menu, click **Usage + quotas** (or search **Quotas** in the top bar).
4. Set the filter to **Microsoft.CognitiveServices** or **Azure OpenAI** (depending on what your tenant shows).
5. Select your **region** (e.g. East US).
6. Find the row for **Azure OpenAI** (e.g. “Total tokens per minute” or a specific model).
7. Select it and click **Request quota increase** (or **New quota request**).
8. Enter the **new limit** you want and a **short reason** (e.g. “RAG chatbot – embedding + GPT-4o, dev/testing”).
9. Submit. Some requests are auto-approved; others are reviewed (often within 1–2 business days).

---

## 3. Try a different region

Quota is per **region**. A new resource in another region often has quota available.

1. In Azure Portal, create a **new** Azure OpenAI resource.
2. Choose a **different region**, e.g.:
   - **Sweden Central**
   - **East US 2**
   - **West Europe**
   - **South Central US**
3. After the resource is created, go to **https://oai.azure.com** → select this new resource.
4. Create your **embedding** and **chat** deployments there.
5. In your app’s `.env`, set **AZURE_OPENAI_ENDPOINT** and **AZURE_OPENAI_API_KEY** to this new resource’s values (from Keys and Endpoint in the Portal).

---

## 4. Use an existing resource that has quota

If you already have an Azure OpenAI resource that **does** have quota (e.g. one that lists RPM/TPM and lets you deploy):

1. Open **https://oai.azure.com** and select **that** resource (the one with quota).
2. In **Deployments**, create:
   - An **embedding** deployment (e.g. `text-embedding-ada-002`, name `text-embedding-ada-002`).
   - A **chat** deployment (e.g. `gpt-4o`, name `gpt-4o`).
3. In the Azure Portal, open that resource → **Keys and Endpoint**.
4. In your project’s **`.env`** set:
   - **AZURE_OPENAI_ENDPOINT** = that resource’s endpoint (must be `*.openai.azure.com`).
   - **AZURE_OPENAI_API_KEY** = Key 1 from that resource.
   - **AZURE_OPENAI_EMBEDDING_DEPLOYMENT** = the embedding deployment name you created.
   - **AZURE_OPENAI_CHAT_DEPLOYMENT** = the chat deployment name you created.

That way you use the resource that already has quota instead of the one with “no quota.”

---

## Summary

| Situation              | Action |
|------------------------|--------|
| First time / no access | Use **https://aka.ms/oai/access** and request access. |
| Resource has no quota  | Request quota increase (Portal → Subscription → Usage + quotas) or try **another region**. |
| Another resource has quota | Use that resource in **oai.azure.com**, create deployments there, and point `.env` at it. |
