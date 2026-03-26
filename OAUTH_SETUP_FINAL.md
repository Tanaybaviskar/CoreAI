# CoreAI OAuth Configuration - Final Setup

## ✅ Current Configuration (All Fixed)

### **Backend (.env file)**
```
GOOGLE_REDIRECT_URI=http://localhost:5000/oauth/callback
```

### **Frontend (page.tsx)**
```javascript
const API_URL = 'http://localhost:3001/api';        // Chat requests -> Proxy
const BACKEND_URL = 'http://localhost:5000';         // Auth requests -> Backend
```

### **Architecture**
```
OAuth Flow:  Frontend → Backend (5000) → Google → Backend (5000) → Frontend
Chat Flow:   Frontend → Proxy (3001) → Backend (5000)
```

## 🎯 What You Need to Do

### **1. Update Google Cloud Console**
Go to: https://console.cloud.google.com/apis/credentials

1. Click on your OAuth 2.0 Client ID
2. Under **Authorized redirect URIs**, set it to:
   ```
   http://localhost:5000/oauth/callback
   ```
3. **REMOVE** any other redirect URIs (like 3001 or 3000)
4. Click **SAVE**

### **2. Restart All Services**
```bash
stop.bat
start.bat
```

### **3. Test OAuth Login**
1. Open http://localhost:3000 (or whatever port the frontend shows)
2. Click "Sign in with Google"
3. Should redirect to Google and back successfully

### **4. Test Email Agent**
After successful login, try:
```
read the top 5 emails in my inbox
```

Should show your real Gmail emails.

## 🔍 Troubleshooting

**If you still get redirect_uri_mismatch:**
- Double check Google Cloud Console has **ONLY**: `http://localhost:5000/oauth/callback`
- Make sure backend is running on port 5000 (check the backend terminal window)
- Clear browser cookies and try again

**If chat doesn't work:**
- Make sure all 3 services are running (Backend, Proxy, Frontend)
- Check that proxy is on port 3001

## 📊 Port Summary
- **5000**: Python Backend (OAuth + Agents)
- **3001**: Node.js Proxy (Chat + Session)
- **3000**: Next.js Frontend (UI)

All code is now configured correctly. You just need to update Google Cloud Console!