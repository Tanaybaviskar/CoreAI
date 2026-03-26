# ✅ Complete API Setup Checklist

Use this guide to set up all your APIs step-by-step.

---

## 📊 Current Status

✅ **Google Calendar OAuth** - DONE (you have credentials.json)
✅ **Core AI (Gemini)** - DONE (GOOGLE_API_KEY in .env)
✅ **Search (Serper)** - DONE (SERPER_API_KEY in .env)
✅ **.env file** - DONE (updated with OAuth credentials)

---

## 📧 Gmail API Setup (5 minutes)

### ✅ Already Have
- Google Cloud Project (gen-lang-client-0678511160)
- OAuth credentials (credentials.json)

### 🔧 What You Need to Do

**Step 1: Enable Gmail API**

1. Go to: [Google Cloud Console - API Library](https://console.cloud.google.com/apis/library)
2. Make sure your project is selected (top bar): **"gen-lang-client-0678511160"**
3. In the search box, type: **"Gmail API"**
4. Click on **"Gmail API"** in results
5. Click the blue **"Enable"** button
6. Wait 10 seconds for it to enable

**Step 2: Add Gmail Scopes**

1. Go to: [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
2. Click **"Edit App"** button
3. Click **"Save and Continue"** on App Information page
4. On **"Scopes"** page, click **"Add or Remove Scopes"**
5. In the filter box, type: **"gmail"**
6. Check these boxes:
   - ✅ `.../auth/gmail.readonly` - View your email messages and settings
   - ✅ `.../auth/gmail.send` - Send email on your behalf
   - ✅ `.../auth/gmail.modify` - Read, compose, send, and permanently delete email
7. Click **"Update"** (bottom)
8. Click **"Save and Continue"**
9. Click **"Save and Continue"** on Test Users page
10. Click **"Back to Dashboard"**

**Step 3: Verify**

✅ That's it! Gmail is now enabled. Your existing `credentials.json` will work.

---

## 🌤️ Weather API Setup (5 minutes - FREE)

### OpenWeatherMap

**Step 1: Create Account**

1. Go to: [OpenWeatherMap Sign Up](https://home.openweathermap.org/users/sign_up)
2. Fill in:
   ```
   Username: [choose a username]
   Email: [your email]
   Password: [create a password]
   ✅ Check "I am 16 years old and over"
   ✅ Check "I agree with Privacy Policy..."
   ✅ Check "I am not a robot" (reCAPTCHA)
   ```
3. Click **"Create Account"**

**Step 2: Verify Email**

1. Check your email inbox
2. Open email from OpenWeatherMap
3. Click **"Verify your email"** button
4. You'll be redirected to OpenWeatherMap

**Step 3: Get API Key**

1. After verification, go to: [API Keys Page](https://home.openweathermap.org/api_keys)
2. You'll see a default key already created (looks like a long string)
3. **Copy the entire key**

Example: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

**Step 4: Add to .env**

1. Open: `backend/agentic/.env`
2. Find line 41-42:
   ```env
   WEATHER_API_KEY=paste_your_openweathermap_key_here
   WEATHER_API_PROVIDER=openweathermap
   ```
3. Replace `paste_your_openweathermap_key_here` with your actual key
4. Save the file

**Step 5: Wait 10 Minutes**

⚠️ **IMPORTANT:** New API keys take 10 minutes to activate!

Set a timer for 10 minutes, then continue.

**Step 6: Test (After 10 Minutes)**

```bash
cd backend/agentic
venv\Scripts\activate
python -c "from utils.api_clients import get_weather_client; print(get_weather_client().get_current_weather('Tokyo'))"
```

**Expected output:**
```python
{
  'temperature': 18,
  'feels_like': 16,
  'condition': 'Clouds',
  'humidity': 65,
  'wind_speed': 5.2,
  'location': 'Tokyo'
}
```

If you see this, ✅ Weather API works!

If you see `None`, wait a few more minutes for activation.

---

## 📰 News API Setup (5 minutes - FREE)

### NewsAPI.org

**Step 1: Create Account**

1. Go to: [NewsAPI Get Started](https://newsapi.org/register)
2. Fill in:
   ```
   First Name: [your first name]
   Email Address: [your email]
   Password: [create a password]
   ```
3. Select: **"I want the API for: Personal Project"**
4. Click **"Submit"**

**Step 2: Verify Email**

1. Check your email inbox
2. Open email from NewsAPI
3. Click **"Verify Email Address"** button
4. You'll see "Email verified successfully!"
5. Click **"Continue to Dashboard"**

**Step 3: Get API Key**

1. On the dashboard, you'll see:
   ```
   Your API key is: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
2. **Copy the entire key**

Example: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

**Step 4: Add to .env**

1. Open: `backend/agentic/.env`
2. Find line 56:
   ```env
   NEWS_API_KEY=paste_your_newsapi_key_here
   ```
3. Replace `paste_your_newsapi_key_here` with your actual key
4. Save the file

**Step 5: Test**

```bash
cd backend/agentic
venv\Scripts\activate
python -c "from utils.api_clients import get_news_client; news = get_news_client().get_top_headlines(limit=3); print('Found', len(news['articles']), 'articles')"
```

**Expected output:**
```
Found 3 articles
```

If you see this, ✅ News API works!

---

## 🚀 First Time Running with OAuth

After setting up all APIs, run your app:

### Step 1: Start Backend

```bash
cd backend/agentic
venv\Scripts\activate
python main.py
```

### Step 2: OAuth Flow (First Time Only)

**What happens:**

```
[Console output]
🚀 CoreAI Multi-Agent System Starting...
========================================
📋 Available Agents:
   ✓ Calendar Agent: Manages calendar events...
   ✓ Meeting Agent: Creates and manages Google Meet...
   ✓ Email Agent: Manages Gmail - read, send, search...
   ...
========================================

Opening browser for Google authentication...
```

**1. Browser Opens Automatically**

You'll see Google sign-in page

**2. Sign In**

- Click your Google account
- Or sign in if needed

**3. Grant Permissions**

You'll see a screen saying:
```
"CoreAI" wants to access your Google Account

This will allow CoreAI to:
✓ View and manage your calendars
✓ Read, send, and manage your email
✓ Create and manage meetings
```

**4. Click "Allow"**

**5. Success!**

Browser shows:
```
The authentication flow has completed.
You may close this window.
```

**6. Back to Terminal**

```
[Console output]
✅ OAuth credentials obtained and saved
✅ Google Calendar service initialized
✅ Gmail service initialized

🌐 Server Configuration:
   Host: 0.0.0.0
   Port: 5001

✨ CoreAI is ready to assist!
========================================
```

### Step 3: Future Runs

**Every time after first run:**
- ✅ No browser opens
- ✅ Uses saved credentials from `token.pickle`
- ✅ Starts immediately

---

## 📋 Final Checklist

Before running the full app, verify:

### APIs Enabled in Google Cloud Console

- [ ] Google Calendar API - Enabled
- [ ] Gmail API - Enabled

### OAuth Scopes Added

- [ ] `...auth/calendar` - Added
- [ ] `...auth/calendar.events` - Added
- [ ] `...auth/gmail.readonly` - Added
- [ ] `...auth/gmail.send` - Added
- [ ] `...auth/gmail.modify` - Added

### Files in backend/agentic/

- [ ] `credentials.json` - Exists ✅ (you have this)
- [ ] `.env` - Updated with all keys
- [ ] `venv/` - Virtual environment exists

### API Keys in .env

- [ ] GOOGLE_API_KEY - ✅ Already set
- [ ] SERPER_API_KEY - ✅ Already set
- [ ] GOOGLE_CLIENT_ID - ✅ Already set
- [ ] GOOGLE_CLIENT_SECRET - ✅ Already set
- [ ] WEATHER_API_KEY - Add your OpenWeatherMap key
- [ ] NEWS_API_KEY - Add your NewsAPI key

---

## 🎯 Complete Startup Sequence

Once everything is set up:

### Terminal 1 - Python Backend
```bash
cd backend/agentic
venv\Scripts\activate
python main.py

# First time: Browser opens for OAuth
# Future times: Starts immediately
```

### Terminal 2 - Node.js Proxy
```bash
cd backend
npm install
node index.js
```

### Terminal 3 - Frontend
```bash
cd frontend
npm install
npm run dev
```

### Open Browser
```
http://localhost:3000
```

---

## 🧪 Testing Each API

### Test Calendar API

In the app chat, type:
```
Check my calendar availability
```

Expected: Real calendar data from your Google Calendar

### Test Gmail API

In the app chat, type:
```
Show me my recent emails
```

Expected: Real emails from your Gmail inbox

### Test Weather API

In the app chat, type:
```
What's the weather in Paris?
```

Expected: Real weather data for Paris (not simulated)

### Test News API

In the app chat, type:
```
What's in the news?
```

Expected: Real news headlines (not simulated)

---

## 🐛 Troubleshooting

### OAuth Issues

**"Invalid client" error**
- Check credentials.json is in `backend/agentic/`
- Check .env has correct CLIENT_ID and CLIENT_SECRET

**Browser doesn't open**
- Copy the URL from terminal
- Open in browser manually

**"Access blocked" error**
- Add your email to OAuth consent screen "Test users"
- Make sure APIs are enabled

### Weather API Issues

**"Invalid API key"**
- Wait 10 minutes after key creation
- Check key is copied correctly (no spaces)
- Verify at: https://home.openweathermap.org/api_keys

### News API Issues

**"Unauthorized" error**
- Check API key is correct
- Verify email was confirmed

### General Issues

**"Module not found"**
```bash
cd backend/agentic
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ✅ Success!

Once everything is set up:
- ✅ Real Google Calendar access
- ✅ Real Gmail access
- ✅ Real weather forecasts
- ✅ Real news headlines
- ✅ Full AI agent functionality

**Total cost: $0** (all free tiers!)

---

## 📚 Quick Reference

| What | Where | Time |
|------|-------|------|
| **Enable Gmail API** | Google Cloud Console | 2 min |
| **Add Gmail Scopes** | OAuth Consent Screen | 3 min |
| **Get Weather Key** | OpenWeatherMap | 5 min |
| **Get News Key** | NewsAPI | 5 min |
| **First OAuth Run** | Run python main.py | 2 min |
| **TOTAL** | | **15-20 min** |

Happy building! 🚀
