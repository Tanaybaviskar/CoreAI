const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const port = 3001;
const AGENT_API_URL_BASE = 'http://localhost:5000';

// Configure CORS to allow credentials (cookies)
app.use(cors({
  origin: true, // Allow all origins in development
  credentials: true // Enable credentials (cookies, auth headers)
}));
app.use(express.json());

// Main chat streaming endpoint
app.post('/api/chat', async (req, res) => {
  const { message, thread_id } = req.body;
  if (!message || !thread_id) return res.status(400).json({ error: 'Message and thread_id are required' });

  try {
    // Forward cookies and headers to maintain session
    const headers = {
      'Content-Type': 'application/json',
      'Cookie': req.headers.cookie || '', // Forward session cookies
      'User-Agent': req.headers['user-agent'] || ''
    };

    const agentResponse = await axios.post(`${AGENT_API_URL_BASE}/invoke`,
      { message, thread_id },
      {
        responseType: 'stream',
        timeout: 120000,
        headers: headers
      }
    );
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    agentResponse.data.pipe(res);
  } catch (error) {
    console.error('Chat proxy error:', error.message);
    res.status(500).send('Error: Could not connect to the AI assistant.');
  }
});

// --- Generic Proxy for all other backend routes ---
const createProxy = (path) => {
    app.all(`/api${path}`, async (req, res) => {
        try {
            // Forward cookies and headers to maintain session
            const headers = {
                'Content-Type': 'application/json',
                'Cookie': req.headers.cookie || '', // Forward session cookies
                'User-Agent': req.headers['user-agent'] || ''
            };

            const response = await axios({
                method: req.method,
                url: `${AGENT_API_URL_BASE}${path}`,
                data: req.body,
                headers: headers,
                timeout: 10000
            });
            res.status(response.status).json(response.data);
        } catch (error) {
            console.error(`Proxy error for ${path}:`, error.message);
            const status = error.response?.status || 500;
            const data = error.response?.data || {error: `Failed to proxy to agent endpoint: ${path}`};
            res.status(status).json(data);
        }
    });
};

createProxy('/health');
createProxy('/dashboard');
createProxy('/settings');
createProxy('/memory');
createProxy('/activity');

// Tasks needs its own handler: it has dynamic sub-paths (/api/tasks/5/complete)
// that the fixed-path createProxy() helper above doesn't cover.
app.all(/^\/api\/tasks(\/.*)?$/, async (req, res) => {
  const subPath = req.originalUrl.replace('/api', '');
  try {
    const response = await axios({
      method: req.method,
      url: `${AGENT_API_URL_BASE}${subPath}`,
      data: req.body,
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000
    });
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error(`Proxy error for ${subPath}:`, error.message);
    const status = error.response?.status || 500;
    const data = error.response?.data || { error: `Failed to proxy to agent endpoint: ${subPath}` };
    res.status(status).json(data);
  }
});

// Note: OAuth endpoints (/auth/*) should go directly to backend, not through proxy
// OAuth flow: Frontend -> Backend (port 5000) -> Google -> Backend (port 5000)
// Chat flow: Frontend -> Proxy (port 3001) -> Backend (port 5000)

app.listen(port, () => {
  console.log(`[Proxy] Node.js server listening at http://localhost:${port}`);
  console.log(`[Proxy] OAuth callbacks go directly to backend at http://localhost:${AGENT_API_URL_BASE}`);
});

