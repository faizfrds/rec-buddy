# Rec-Buddy - Recovery Training Application

A Recovery Training Application powered by Google Agent ADK that provides AI-powered recovery advice based on your symptoms. Includes user responses to enable a human-in-the-loop approach, supported by multi agent orchestration for personalized support.

## Design Doc
https://docs.google.com/document/d/1JYJujiL7Nh6Qj-PsO2lie2sCFpRFpRCPqpeEL1yIl0k/edit?usp=sharing

## Architecture

- **Backend**: FastAPI (Python) with Google Agent ADK multi-agent AI system
- **Frontend**: Next.js 16 (React/TypeScript) chat interface
- **AI**: Google Gemini via Google Agent ADK

## Quick Start

### 1. Get Your Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" and create a new key
4. Copy the API key

### 2. Configure Environment Variables

Edit `backend/.env` and add your API key:

```bash
GOOGLE_API_KEY="your_actual_api_key_here"
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### 3. Start the Backend (Terminal 1)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 4. Start the Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

### 5. Open the Application

Visit **http://localhost:3000** in your browser.

## Project Structure

```
rec-buddy/
├── backend/
│   ├── app/
│   │   ├── __init__.py      # Environment setup
│   │   ├── main.py          # FastAPI server & routes
│   │   └── agents.py        # Multi-agent AI system
│   ├── .env                 # Environment variables (API keys)
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Main chat interface
│   │   └── styles/
│   │       └── index.css    # Global styles
│   ├── package.json         # Node.js dependencies
│   └── next.config.js       # Next.js config
└── .gitignore               # Git ignore rules
```

## Multi-Agent System

The backend uses 3 specialized AI agents:

| Agent | Purpose |
|-------|---------|
| **DiagnosisAgent** | Analyzes symptoms (pain, dizziness, breathlessness) |
| **RecoveryAgent** | Creates personalized recovery strategies |
| **ValidatorAgent** | Validates safety of recovery plans |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/chat` | Send message and get AI response |

### Chat Request/Response

**Request:**
```json
{
  "message": "I have knee pain when walking",
  "preference": "long-term"
}
```

**Response:**
```json
{
  "response": "Here is my analysis and plan based on your feedback:",
  "diagnosis": "...",
  "recovery_plan": "...",
  "safety_check": "..."
}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI Studio API key | Yes (for AI features) |
| `GOOGLE_GENAI_USE_VERTEXAI` | Set to `FALSE` for AI Studio | No |

### Alternative: Vertex AI Setup

For production, use Vertex AI with service account:

```bash
GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Check `backend/.env` exists with valid `GOOGLE_API_KEY` |
| Frontend can't connect | Ensure backend is running on port 8000 |
| Module not found | Run `pip install -r requirements.txt` in backend |
| 429 Rate limit | Request higher quota at Google AI Studio |

## Security Notes

- Never commit `.env` files to version control
- Never share API keys publicly
- Use Google Cloud Secret Manager for production deployments

## Sources

- [Google Agent ADK Documentation](https://docs.cloud.google.com/agent-builder/agent-engine/develop/adk)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [Gemini - Agent Development Kit](https://google.github.io/adk-docs/agents/models/google-gemini/)
