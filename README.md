AutoNotion

Type what you did today → Groq formats it → Notion page created automatically.

---

## Setup (one time, ~10 minutes)

### 1. Install dependency
```bash
pip install requests
```

### 2. Get your Notion API Key
1. Go to [notion.so/my-integrations](https://notion.so/my-integrations)
2. Click **New Integration**
3. Give it a name (e.g. "Work Logger") → Submit
4. Copy the **Internal Integration Token**

### 3. Get your Notion Page ID
1. Open the Notion page where you want logs to appear
2. Look at the URL in your browser:
   ```
   https://notion.so/Your-Page-Title-abc123def456...
   ```
3. The long string at the end is your Page ID
   ```
   abc123def456...
   ```

### 4. Connect the integration to your page
1. Open your Notion page
2. Click **...** (three dots) in top right
3. Go to **Connections** → Add your integration

### 5. Fill in config.py
```python
NOTION_API_KEY = "secret_xxxxxxxxxxxx"
NOTION_PAGE_ID = "abc123def456..."
DEFAULT_PROJECT = "Your Project Name"
```

---

## Daily Usage

```bash
cd notion-updater
python update.py
```

Then just answer the two questions:

```
──────────────────────────────────────────────────
  📝  Notion Work Log Updater
──────────────────────────────────────────────────

  Project name [CommOS]: CommOS

  What did you do today?
  (press Enter twice when done)

  built the auth system, fixed login bug, pushed to github

  What's left / additional work?
  (press Enter twice when done)

  payment integration, write tests for auth

  ⏳ Sending to Gemini for formatting...
  ✅ Gemini done. Pushing to Notion...

──────────────────────────────────────────────────
  Project : CommOS
  Done    : 3 items
  Pending : 2 items
──────────────────────────────────────────────────

  🚀 Notion page created successfully!
  🔗 https://notion.so/...
```

---

## What the Notion page looks like

```
📅 Work Log — 07 April 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━
💼 Project: CommOS

✅ Completed Today
  ☑ Built the authentication system with JWT tokens
  ☑ Fixed the login bug on the /api/login endpoint
  ☑ Pushed all changes to GitHub

📌 Pending / Additional Work
  ☐ Integrate payment gateway
  ☐ Write unit tests for the auth module

🕐 Logged at 11:42 PM
```

---

## Files

| File | Purpose |
|---|---|
| `update.py` | Run this daily |
| `config.py` | Your keys and settings |
| `gemini_client.py` | Talks to Gemini CLI |
| `notion_client.py` | Creates Notion pages |
