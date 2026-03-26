# 🔐 OAuth & API Keys Setup Guide

This guide walks you through setting up OAuth 2.0 and all API integrations for CoreAI.

## 📋 Table of Contents

1. [Google OAuth 2.0 Setup (Recommended)](#google-oauth-20-setup)
2. [Weather API Setup](#weather-api-setup)
3. [News API Setup](#news-api-setup)
4. [Optional Integrations](#optional-integrations)

---

## 🔑 Google OAuth 2.0 Setup

OAuth 2.0 gives your agents **full access** to user's Google Calendar, Gmail, and Meet.

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **"Select a Project"** → **"New Project"**
3. Name: `CoreAI` → Click **"Create"**
4. Wait for project creation, then select it

### Step 2: Enable Required APIs

1. Go to **"APIs & Services"** → **"Library"**
2. Search and enable these APIs (click "Enable" for each):
   - ✅ **Google Calendar API**
   - ✅ **Gmail API**
   - ✅ **Google Meet API** (part of Calendar API)

### Step 3: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Choose **"External"** → Click **"Create"**
3. Fill in the form:
   ```
   App name: CoreAI
   User support email: [your email]
   App logo: [optional]
   Developer contact info: [your email]
   ```
4. Click **"Save and Continue"**

### Step 4: Add Scopes

1. Click **"Add or Remove Scopes"**
2. Add these scopes manually:
   ```
   https://www.googleapis.com/auth/calendar
   https://www.googleapis.com/auth/calendar.events
   https://www.googleapis.com/auth/gmail.readonly
   https://www.googleapis.com/auth/gmail.send
   https://www.googleapis.com/auth/gmail.modify
   ```
3. Or filter and select:
   - Calendar API: All scopes
   - Gmail API: Read, send, and modify
4. Click **"Update"** → **"Save and Continue"**

### Step 5: Add Test Users

1. Click **"Add Users"**
2. Add your Gmail address
3. Click **"Save and Continue"**
4. Review and click **"Back to Dashboard"**

### Step 6: Create OAuth Client

1. Go to **"Credentials"** → **"Create Credentials"** → **"OAuth client ID"**
2. Application type: **"Desktop app"** (easiest for local development)
   - Or choose **"Web application"** for production
3. Name: `CoreAI Desktop Client`
4. Click **"Create"**

### Step 7: Download Credentials

1. After creation, you'll see your credentials
2. Click **"Download JSON"**
3. Save the file

### Step 8: Configure CoreAI

**Option A: Use JSON file (Recommended)**
```bash
# Move downloaded file to CoreAI directory
mv ~/Downloads/client_secret_*.json backend/agentic/credentials.json
```

**Option B: Use Environment Variables**

Open the downloaded JSON file and copy the values to `.env`:

```env
# Open backend/agentic/.env and add:
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8080
```

### Step 9: Test OAuth Flow

```bash
cd backend/agentic
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**First time running:**
- A browser window will open
- Sign in with your Google account
- Grant permissions
- Close the browser
- Credentials are saved in `token.pickle`

**Future runs:**
- Automatically uses saved credentials
- No browser window needed

---

## 🌤️ Weather API Setup

### Option 1: OpenWeatherMap (Recommended)

**Why:** Free tier is generous (60 calls/min), reliable, comprehensive data

1. **Sign Up**
   - Go to [OpenWeatherMap](https://openweathermap.org/api)
   - Click **"Sign Up"**
   - Verify your email

2. **Get API Key**
   - Go to [API Keys](https://home.openweathermap.org/api_keys)
   - Copy your default API key
   - Or create a new one

3. **Add to .env**
   ```env
   WEATHER_API_KEY=your_openweathermap_api_key_here
   WEATHER_API_PROVIDER=openweathermap
   WEATHER_API_UNITS=metric
   ```

4. **Test**
   ```python
   # In Python console
   from utils.api_clients import get_weather_client
   client = get_weather_client()
   weather = client.get_current_weather("New York")
   print(weather)
   ```

### Option 2: WeatherAPI.com

**Why:** Even more generous free tier (1M calls/month)

1. **Sign Up**
   - Go to [WeatherAPI.com](https://www.weatherapi.com/)
   - Click **"Sign Up Free"**

2. **Get API Key**
   - Dashboard → **"Copy"** your API key

3. **Add to .env**
   ```env
   WEATHER_API_KEY=your_weatherapi_key_here
   WEATHER_API_PROVIDER=weatherapi
   WEATHER_API_UNITS=metric
   ```

---

## 📰 News API Setup

1. **Sign Up**
   - Go to [NewsAPI.org](https://newsapi.org/)
   - Click **"Get API Key"**
   - Fill in the form (choose **Developer** plan - it's free)

2. **Get API Key**
   - Check your email for activation
   - Login and go to [Account](https://newsapi.org/account)
   - Copy your API key

3. **Add to .env**
   ```env
   NEWS_API_KEY=your_newsapi_key_here
   NEWS_API_COUNTRY=us
   NEWS_API_LANGUAGE=en
   ```

4. **Free Tier Limits**
   - 100 requests per day
   - 7-day news history
   - Upgrade to paid for more

5. **Test**
   ```python
   from utils.api_clients import get_news_client
   client = get_news_client()
   news = client.get_top_headlines(limit=5)
   print(news)
   ```

---

## 🔧 Optional Integrations

These are nice-to-have but not required:

### Slack Integration

1. Go to [Slack API](https://api.slack.com/apps)
2. **"Create New App"** → **"From scratch"**
3. Add to workspace
4. Get **Bot Token** (`xoxb-...`)
5. Add to `.env`:
   ```env
   SLACK_BOT_TOKEN=xoxb-your-token
   ```

### Microsoft Teams

1. Go to [Azure Portal](https://portal.azure.com)
2. Register application
3. Get credentials
4. Add to `.env`:
   ```env
   MICROSOFT_APP_ID=your_app_id
   MICROSOFT_APP_PASSWORD=your_password
   ```

### Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. **"New integration"**
3. Get token
4. Add to `.env`:
   ```env
   NOTION_API_KEY=secret_your_token
   ```

---

## ✅ Verification Checklist

After setup, verify everything works:

### Core APIs (Required)

- [ ] GOOGLE_API_KEY - Working
- [ ] SERPER_API_KEY - Working

### Google OAuth (Recommended)

- [ ] OAuth flow completes successfully
- [ ] `token.pickle` file created
- [ ] No errors in console

### Weather API (Optional)

- [ ] WEATHER_API_KEY added
- [ ] Test query returns real data
- [ ] No "simulated data" message

### News API (Optional)

- [ ] NEWS_API_KEY added
- [ ] Test query returns real articles
- [ ] No "simulated data" message

---

## 🧪 Testing API Integration

### Test All APIs at Once

```bash
cd backend/agentic
python -c "
from utils.api_clients import get_weather_client, get_news_client
from utils.oauth_helper import get_calendar_service

# Test Weather
weather = get_weather_client()
print('Weather:', weather.get_current_weather('London'))

# Test News
news = get_news_client()
print('News:', news.get_top_headlines(limit=3))

# Test OAuth
calendar = get_calendar_service()
print('Calendar:', 'Connected' if calendar else 'Not configured')
"
```

### Test in Chat Interface

Start CoreAI and try these:

```
User: What's the weather in Tokyo?
Expected: Real weather data (if API configured) or simulated data

User: What's in the news?
Expected: Real headlines (if API configured) or simulated data
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file**
   ```bash
   # Already in .gitignore, but double-check:
   echo ".env" >> .gitignore
   echo "token.pickle" >> .gitignore
   echo "credentials.json" >> .gitignore
   ```

2. **Rotate API keys regularly**
   - Every 3-6 months for development
   - More frequently for production

3. **Use environment-specific keys**
   - Different keys for dev/staging/prod
   - Never use production keys in development

4. **Restrict API key permissions**
   - In Google Cloud Console, restrict by IP
   - In OpenWeatherMap, enable domain restrictions

5. **Monitor API usage**
   - Check dashboards regularly
   - Set up alerts for unusual activity

---

## 🐛 Troubleshooting

### OAuth Issues

**"redirect_uri_mismatch"**
- Solution: Add `http://localhost:8080` to authorized redirect URIs

**Browser doesn't open**
- Solution: Copy the URL from terminal and open manually

**"Access blocked: This app's request is invalid"**
- Solution: Add your email to test users in OAuth consent screen

### API Key Issues

**Weather: "Invalid API key"**
- Check the key is copied correctly (no extra spaces)
- Verify key is activated (can take 10 minutes)

**News: "Rate limit exceeded"**
- Free tier: 100 requests/day
- Wait until reset or upgrade plan

**"Module not found"**
```bash
cd backend/agentic
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Additional Resources

- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
- [Gmail API Guide](https://developers.google.com/gmail/api/guides)

---

## 🎉 You're All Set!

Once configured, your agents will:
- ✅ Access real Google Calendar data
- ✅ Send and read real Gmail
- ✅ Fetch real weather forecasts
- ✅ Show actual news headlines

**Important:** The app works great even without these APIs! It will use simulated data for testing, and you can add real APIs later.

Need help? Check the main [SETUP_GUIDE.md](SETUP_GUIDE.md) or open an issue on GitHub.
