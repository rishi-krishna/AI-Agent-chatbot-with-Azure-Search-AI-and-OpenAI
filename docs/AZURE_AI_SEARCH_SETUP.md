# Create Azure AI Search – Step-by-Step (No Code)

Everything you do **outside the code**: in the browser (Azure Portal) and in your `.env` file.

---

## Before You Start

- You need a **Microsoft account** (Outlook, Hotmail, or any email you use for Microsoft).
- You need an **Azure subscription**. If you don’t have one:
  - Go to [https://azure.microsoft.com/free/](https://azure.microsoft.com/free/)
  - Sign up for a **free account**. You get free credits for 30 days and some services stay free (AI Search has a free tier you can use for learning).

---

## Part 1: Sign In to Azure Portal

1. Open a browser and go to: **https://portal.azure.com**
2. Sign in with your Microsoft account.
3. You should see the **Azure Portal** home (dashboard with “Azure services” and a search bar at the top).

---

## Part 2: Create an Azure AI Search Resource

### Step 1: Open “Create a resource”

1. In the top search bar, type **“Azure AI Search”** (or **“Search service”**).
2. Click the result **“Azure AI Search”** under **Services** or **Marketplace**.
3. Click the **“Create”** button on the overview page.

### Step 2: Basics tab

1. **Subscription**  
   - Select the subscription you want to use (e.g. “Free Trial” or “Pay-As-You-Go”).

2. **Resource group**  
   - Click **“Create new”**.  
   - Name it something like: `coo-chat-rg`  
   - Click **OK**.

3. **Name** (your search service name)  
   - Choose a **unique** name, e.g. `coo-chat-search` or `yourname-coo-search`.  
   - This will become part of your URL: `https://<Name>.search.windows.net`.  
   - Only letters, numbers, hyphens; no spaces.

4. **Location**  
   - Pick a region near you (e.g. **East US**, **West Europe**).  
   - Keep it the same as other resources (e.g. OpenAI) if you use them together.

5. **Pricing tier**  
   - For learning/small use: choose **Free** (F) if available.  
   - For production or if Free isn’t there: **Basic** is the cheapest paid tier.  
   - Click **“Review + create”** (or **Next** if you want to skip the rest for now).

### Step 3: Review and create

1. Review the summary.
2. Click **“Create”**.
3. Wait until deployment finishes (usually under a minute).
4. Click **“Go to resource”** when it says “Your deployment is complete”.

---

## Part 3: Get Your Endpoint and API Key

You need **two values** for your `.env` file: **Endpoint** and **API key**.

### Get the Endpoint

1. You should be on your **Azure AI Search** resource page.
2. In the left menu, under **Settings**, click **“Keys”** (or in the main overview you may see “Url”).
3. At the top you’ll see **URL** (or “Search service endpoint”). It looks like:
   - `https://your-service-name.search.windows.net`
4. **Copy this entire URL** (no slash at the end is fine). This is your **AZURE_SEARCH_ENDPOINT**.

### Get the API Key (Admin key)

1. On the same **Keys** page, you’ll see two keys:
   - **Primary admin key**
   - **Secondary admin key**
2. Click **“Show”** next to **Primary admin key**, then **Copy**.
3. This long string is your **AZURE_SEARCH_API_KEY**.  
   - Store it somewhere safe (e.g. paste into your `.env` file).  
   - Never commit this key to Git or share it publicly.

---

## Part 4: Put Them in Your `.env` File

1. Open your project folder and open the file **`.env`** (in the project root: `Coochat_curser`).
2. Set these two lines (use your real values):

```env
AZURE_SEARCH_ENDPOINT=https://YOUR-SERVICE-NAME.search.windows.net
AZURE_SEARCH_API_KEY=your-primary-admin-key-pasted-here
```

3. For the index name, you can keep:

```env
AZURE_SEARCH_INDEX_NAME=coo-help-chunks
```

4. Save the file.

You do **not** create the index in the Portal. The **code** (the script `indexing/scripts/create_search_index.py`) creates the index when you run it. So after this, you’re done with “account” setup for AI Search.

---

## Summary Checklist

- [ ] Microsoft account and Azure subscription (free tier is OK).
- [ ] Signed in at [https://portal.azure.com](https://portal.azure.com).
- [ ] Created a resource group (e.g. `coo-chat-rg`).
- [ ] Created **Azure AI Search** with a unique **Name**, chosen **Location** and **Pricing tier** (Free or Basic).
- [ ] Deployment completed; opened the Search resource.
- [ ] Copied **URL** → use as **AZURE_SEARCH_ENDPOINT** in `.env`.
- [ ] Copied **Primary admin key** → use as **AZURE_SEARCH_API_KEY** in `.env`.
- [ ] Saved `.env` in project root. No code run in Portal; index is created when you run `create_search_index.py`.

---

## Optional: Find Your Search Resource Again Later

1. Go to [https://portal.azure.com](https://portal.azure.com).
2. In the top search bar, type your search service name (e.g. `coo-chat-search`).
3. Click the resource **“Azure AI Search”**.
4. Use **Keys** to copy the URL or key again if needed.

---

## If Something Goes Wrong

- **“Quota exceeded” or no Free tier:** Your subscription or region might not offer Free. Choose **Basic** (paid, low cost) or try another region.
- **Name not available:** The name is taken. Try a more unique name (e.g. add your name or numbers).
- **No “Keys” in the menu:** Make sure you’re on the **Azure AI Search** resource (not a different type). Keys are under **Settings** → **Keys**.

Once the two values are in `.env`, you’re ready to run the indexing scripts (create index and run indexing) as in **SETUP_AND_RUN.md**.
