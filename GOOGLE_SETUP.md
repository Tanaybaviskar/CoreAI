# Google OAuth Setup Guide

## Step 1: Google Cloud Console Configuration

### 1.1 Create/Configure OAuth Consent Screen
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **OAuth consent screen**
3. Choose **External** user type (for personal use)
4. Fill in required fields:
   - **App name**: CoreAI Assistant
   - **User support email**: Your email
   - **Developer contact**: Your email
5. **IMPORTANT**: Add test users in the "Test users" section
   - Click **+ ADD USERS**
   - Add your Gmail address that you want to test with
   - This bypasses the verification requirement for testing

### 1.2 Configure OAuth Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth 2.0 Client IDs**
3. Choose **Web application**
4. Set **Authorized redirect URIs**:
   ```
   http://localhost:5001/oauth/callback
   ```
5. Download the JSON file or copy the Client ID and Client Secret

### 1.3 Enable Required APIs
Make sure these APIs are enabled:
- **Google Calendar API**
- **Gmail API**
- **Google+ API** (for user info)

## Step 2: Environment Configuration

Update your `.env` file in `backend/agentic/`:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_actual_client_id_here
GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5001/oauth/callback

# Other API keys (optional but recommended)
WEATHER_API_KEY=your_openweathermap_api_key
SERPER_API_KEY=your_serper_api_key
NEWS_API_KEY=your_newsapi_key
```

## Step 3: Testing the OAuth Flow

### 3.1 Start the Application
```bash
# Start backend
cd backend/agentic
python main.py

# Start frontend (in new terminal)
cd frontend
npm run dev
```

### 3.2 Test Authentication
1. Open http://localhost:3000
2. You should see the Google Sign-in button
3. Click it - you'll be redirected to Google
4. **Sign in with the email you added as a test user**
5. Accept the permissions (Calendar, Gmail, Profile)
6. You should be redirected back and logged in

### 3.3 Test Real Data Integration
Once logged in, try these commands:
- "Show my calendar events" (real Calendar data)
- "Check my emails" (real Gmail data)
- "What's my schedule today?" (real Calendar)
- "Send an email to someone@example.com" (real Gmail)
- "What's the weather?" (uses your real IP location)

## Troubleshooting

### OAuth Error "access_denied"
- **Cause**: Your email is not added as a test user
- **Fix**: Add your email in Google Cloud Console → OAuth consent screen → Test users

### "App not verified" warning
- **For testing**: Add test users (recommended)
- **For production**: Submit app for verification (takes days/weeks)

### API not working
- Check if APIs are enabled in Google Cloud Console
- Verify your credentials are correct in .env file
- Check backend logs for specific errors

## Security Notes
- Never commit real credentials to git
- Use environment variables for all sensitive data
- Consider using Google Cloud Secret Manager for production