# Create Azure OpenAI – Step-by-Step (No Code)

Everything you do **outside the code**: in the browser (Azure Portal and Azure OpenAI Studio). After this, you add the values to your `.env` file.

---

## Before You Start

- You need a **Microsoft account** and an **Azure subscription** (same as for Azure AI Search).
- **Azure OpenAI** often requires **approval** for your subscription. If you get “Access denied” or a message about applying for access:
  - In Portal, go to your **Azure OpenAI** resource.
  - Use the **“Request access to Azure OpenAI”** link, or go to [https://aka.ms/oai/access](https://aka.ms/oai/access) and submit the form.
  - Wait for approval (can take a short time or a few days).

---

## Part 1: Sign In to Azure Portal

1. Open a browser and go to: **https://portal.azure.com**
2. Sign in with your Microsoft account.

---

## Part 2: Create an Azure OpenAI Resource

### Step 1: Open “Create Azure OpenAI”

1. In the top **search bar**, type **“Azure OpenAI”**.
2. Click **“Azure OpenAI”** in the results (under Services or Marketplace).
3. Click the **“Create”** button.

### Step 2: Basics

1. **Subscription**  
   - Select your subscription (e.g. Free Trial).

2. **Resource group**  
   - Use the same one as AI Search if you have it (e.g. `coo-chat-rg`), or click **Create new** and name it e.g. `coo-chat-rg`.

3. **Region**  
   - Choose a region (e.g. **East US**, **Sweden Central**).  
   - Not every region has OpenAI; if you see “not available”, pick another (e.g. East US, West Europe).

4. **Name**  
   - Give the resource a unique name, e.g. `coo-chat-openai` or `yourname-coo-openai`.  
   - You’ll use this in the endpoint URL.

5. **Pricing tier**  
   - Usually **Standard S0** (pay-as-you-go).  
   - Click **Next**.

### Step 3: (Optional) Networks / Tags

- You can leave defaults and click **Next** until you see **Review + create**.

### Step 4: Review and create

1. Click **Review + create**.
2. Click **Create**.
3. Wait for deployment to finish, then click **Go to resource**.

You now have the **Azure OpenAI resource**. Next you need the **Endpoint**, **API key**, and **model deployments**.

---

## Part 3: Get Endpoint and API Key

1. You should be on your **Azure OpenAI** resource page in the Portal.
2. In the left menu, under **Resource management** (or **Settings**), click **“Keys and Endpoint”**.
3. You’ll see:
   - **Endpoint** – URL like `https://coo-chat-openai.openai.azure.com/`  
     → Copy this. This is your **AZURE_OPENAI_ENDPOINT**.
   - **KEY 1** (and KEY 2)  
     → Click **Show** next to KEY 1, then **Copy**. This is your **AZURE_OPENAI_API_KEY**.

Keep the resource page or Keys page open; you’ll need the **deployment names** from the next part.

---

## Part 4: Create Model Deployments (Embedding + Chat)

You must **deploy** two models: one for **embeddings** and one for **chat**. This is done in **Azure OpenAI Studio**.

### Step 1: Open Azure OpenAI Studio

1. On your Azure OpenAI resource page in the Portal, find the **“Go to Azure OpenAI Studio”** button (or “Open in Studio”) and click it.  
   - Or go to: **https://oai.azure.com** and sign in; then pick your subscription and your **Azure OpenAI resource**.
2. You should see the **Azure OpenAI Studio** (chat icon, “Playground”, “Deployments”, etc.).

### Step 2: Go to Deployments

1. In the left menu, click **“Deployments”** (or “Model deployments” / “Manage deployments”).
2. You’ll see a list of deployments (may be empty).

### Step 3: Create Embedding Deployment

1. Click **“+ Create new deployment”** (or “Create new deployment”).
2. Fill in:
   - **Select a model:** Choose **“text-embedding-ada-002”** (or **“text-embedding-3-small”** if you prefer).
   - **Deployment name:** Type exactly: **`text-embedding-ada-002`** (or a short name like `embedding` – but then you must use that same name in `.env`).
   - **Model version:** Keep default if shown.
   - **Capacity:** Leave default (e.g. 10 TPM or 120K TPM depending on tier).
3. Click **Create** (or **Save**).
4. Wait until the deployment shows **Succeeded** or **Active**.  
   - **Write down the deployment name** – this is **AZURE_OPENAI_EMBEDDING_DEPLOYMENT** (e.g. `text-embedding-ada-002`).

### Step 4: Create Chat Deployment

1. Click **“+ Create new deployment”** again.
2. Fill in:
   - **Select a model:** Choose **“gpt-4o”** (recommended) or **“gpt-4o-mini”** (cheaper). Avoid deprecated gpt-4 / gpt-35-turbo.
   - **Deployment name:** Type exactly: **`gpt-4o`** (or `gpt-4o-mini` if you chose that model). Use a short, memorable name – this is **AZURE_OPENAI_CHAT_DEPLOYMENT**.
   - **Model version:** Keep default.
   - **Capacity:** Leave default.
3. Click **Create** (or **Save**).
4. Wait until the deployment is **Succeeded** or **Active**.  
   - **Write down the deployment name** – this is **AZURE_OPENAI_CHAT_DEPLOYMENT** (e.g. `gpt-4o` or `gpt-4o-mini`).

---

## Part 5: Put Everything in Your `.env` File

1. Open your project folder and open the file **`.env`** in the **project root** (`Coochat_curser`).
2. Add or update these lines with **your** values:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE-NAME.openai.azure.com/
AZURE_OPENAI_API_KEY=paste-your-key-1-here
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
```

- **AZURE_OPENAI_ENDPOINT:** The URL you copied from Keys and Endpoint (usually ends with `/`).
- **AZURE_OPENAI_API_KEY:** The KEY 1 you copied.
- **AZURE_OPENAI_EMBEDDING_DEPLOYMENT:** The **exact** deployment name you gave for the embedding model (e.g. `text-embedding-ada-002`).
- **AZURE_OPENAI_CHAT_DEPLOYMENT:** The **exact** deployment name you gave for the chat model (e.g. `gpt-4o` or `gpt-4o-mini`).

3. Save the file.

---

## Summary Checklist

- [ ] Signed in at [https://portal.azure.com](https://portal.azure.com).
- [ ] Created **Azure OpenAI** resource (name, region, pricing tier).
- [ ] Opened **Keys and Endpoint** → copied **Endpoint** and **KEY 1**.
- [ ] Opened **Azure OpenAI Studio** (from resource or [https://oai.azure.com](https://oai.azure.com)).
- [ ] Under **Deployments**, created **embedding** deployment (e.g. `text-embedding-ada-002`) and noted the name.
- [ ] Under **Deployments**, created **chat** deployment (e.g. `gpt-4o` or `gpt-4o-mini`) and noted the name.
- [ ] Put all four values in **`.env`** (endpoint, API key, embedding deployment name, chat deployment name).

After this, you can run: create index → run indexing → start API → start frontend (see **SETUP_AND_RUN.md**).

---

## If Something Goes Wrong

- **“You don’t have access to Azure OpenAI”**  
  Your subscription may need approval. Use the “Request access” link on the resource or at [https://aka.ms/oai/access](https://aka.ms/oai/access).

- **“Deployment name already exists”**  
  Pick a different deployment name (e.g. `gpt-4o-coo`) and use that exact name in **AZURE_OPENAI_CHAT_DEPLOYMENT** in `.env`.

- **Model not in the list**  
  Some models are region-specific. Try another region for the resource or choose another model (e.g. gpt-4o-mini instead of gpt-4o).

- **Studio looks different**  
  Menus can change. Look for **“Deployments”** or **“Model deployments”** and **“Create new deployment”**; the idea is the same: one deployment for embeddings, one for chat.
