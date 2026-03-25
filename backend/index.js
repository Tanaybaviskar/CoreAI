const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const port = 3001;
const AGENT_API_URL_BASE = 'http://localhost:5001';

app.use(cors());
app.use(express.json());

// Main chat streaming endpoint
app.post('/api/chat', async (req, res) => {
  const { message, thread_id } = req.body;
  if (!message || !thread_id) return res.status(400).json({ error: 'Message and thread_id are required' });

  try {
    const agentResponse = await axios.post(`${AGENT_API_URL_BASE}/invoke`, 
      { message, thread_id }, 
      { responseType: 'stream', timeout: 120000 }
    );
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    agentResponse.data.pipe(res);
  } catch (error) {
    res.status(500).send('Error: Could not connect to the AI assistant.');
  }
});

// --- Generic Proxy for all other backend routes ---
const createProxy = (path) => {
    app.all(`/api${path}`, async (req, res) => {
        try {
            const response = await axios({
                method: req.method,
                url: `${AGENT_API_URL_BASE}${path}`,
                data: req.body,
                headers: {'Content-Type': 'application/json'},
                timeout: 10000 
            });
            res.status(response.status).json(response.data);
        } catch (error) {
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


app.listen(port, () => {
  console.log(`[Proxy] Node.js server listening at http://localhost:${port}`);
});

