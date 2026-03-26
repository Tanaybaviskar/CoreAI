# CoreAI Agent Testing Guide

## 🧪 How to Test All Agent Functionality

### Prerequisites
1. Complete the Google OAuth setup (see GOOGLE_SETUP.md)
2. Both backend and frontend running
3. Successfully logged in with Google account

## 📧 Email Agent Testing

### Test Commands:
```
"Check my emails"
"Show my inbox"
"Read my latest emails"
"Send an email to friend@example.com with subject Test and message Hello from CoreAI"
"Search for emails about meeting"
"Create a draft email to boss@company.com"
```

### Expected Results:
- **Real Gmail data**: Your actual inbox emails
- **Send functionality**: Real emails sent from your Gmail
- **Search**: Real search results from your Gmail
- **Drafts**: Real drafts created in your Gmail account

### Fallback Behavior:
If Gmail API fails, you'll get simulated data with source: "simulated"

## 📅 Calendar Agent Testing

### Test Commands:
```
"Show my calendar"
"What's my schedule today?"
"Check my availability for tomorrow"
"Schedule a meeting for 2 PM today"
"Book an appointment for next Monday at 10 AM"
"Cancel my 3 PM meeting" (requires event ID)
```

### Expected Results:
- **Real Calendar data**: Your actual Google Calendar events
- **Availability**: Real free/busy times from your calendar
- **Event creation**: Real events created in your Google Calendar
- **Event management**: Real event modifications

### Fallback Behavior:
If Calendar API fails, you'll get simulated data with source: "simulated"

## 🌤️ Weather Agent Testing

### Test Commands:
```
"What's the weather?"
"How's the weather today?"
"What's the weather in New York?"
"Tell me the weather forecast"
```

### Expected Results:
- **Auto-location**: Uses your real IP address to detect location
- **Real weather data**: From OpenWeatherMap or WeatherAPI
- **Specific locations**: Weather for any city you specify

### Fallback Behavior:
If no API key configured, returns simulated weather data

## 📰 News Agent Testing

### Test Commands:
```
"What's the latest news?"
"Show me technology news"
"Get business headlines"
"Search news about AI"
```

### Expected Results:
- **Real news**: From Serper API (Google News) or NewsAPI
- **Category filtering**: Real news by category
- **Search functionality**: Real search results

### Fallback Behavior:
If no API key configured, returns simulated news data

## 🤖 General Agent Testing

### Test Commands:
```
"What can you do?"
"Help me with my tasks"
"What's your status?"
"Show me agent info"
```

### Expected Results:
- Agent capability descriptions
- System status information
- Available agent list

## 🔍 How to Verify Real vs Simulated Data

### Check the Response Source:
Every agent response includes a `source` field:
- `"source": "real_gmail_api"` = Real Gmail data
- `"source": "real_calendar_api"` = Real Calendar data
- `"source": "real_weather_api"` = Real weather data
- `"source": "simulated"` = Fallback simulated data

### Real Data Indicators:
- **Gmail**: See your actual email subjects, senders, dates
- **Calendar**: See your actual events, times, attendees
- **Weather**: See weather for your detected IP location
- **News**: See current, real headlines with actual URLs

## 🚨 Troubleshooting Test Issues

### Gmail Agent Not Working:
1. Check if Gmail API is enabled in Google Cloud
2. Verify you granted Gmail permissions during OAuth
3. Check backend logs for specific errors
4. Try: `"Check my emails"` and look for `source: "real_gmail_api"`

### Calendar Agent Not Working:
1. Check if Calendar API is enabled in Google Cloud
2. Verify you granted Calendar permissions during OAuth
3. Try: `"Show my calendar"` and look for `source: "real_calendar_api"`

### Weather Not Showing Your Location:
1. Check if WEATHER_API_KEY is set in .env
2. Verify your IP can be geolocated (not localhost)
3. Check backend logs for geolocation errors

### OAuth Issues:
1. Make sure your email is added as a test user
2. Try logging out and logging back in
3. Check if redirect URI matches exactly: `http://localhost:5001/oauth/callback`

## 📊 Testing Checklist

- [ ] Google OAuth login works
- [ ] Gmail agent shows real emails (source: real_gmail_api)
- [ ] Calendar agent shows real events (source: real_calendar_api)
- [ ] Weather shows your IP-detected location
- [ ] News shows current headlines
- [ ] Can send real emails through Gmail
- [ ] Can create real calendar events
- [ ] Fallbacks work when APIs unavailable

## 🎯 Expected User Experience

Once everything is working:
1. **Seamless authentication**: One-click Google login
2. **Real data integration**: All your actual Gmail and Calendar data
3. **Smart location detection**: Automatic weather for your location
4. **Full functionality**: Send emails, create events, get real information
5. **Reliable fallbacks**: System works even if some APIs fail

This makes CoreAI a truly functional personal assistant that works with your real accounts and data!