# AI Streaming Chat

A real-time AI-powered conversational application built using React, Python FastAPI, and Google Gemini API. The application delivers AI-generated responses progressively through HTTP streaming, providing an interactive chat experience similar to modern AI assistants.

## Project Overview

AI Streaming Chat demonstrates how Large Language Models (LLMs) can be integrated into modern full-stack web applications using real-time streaming technology.

The project is designed for developers, AI enthusiasts, students, and researchers interested in building AI-powered conversational applications.

## Features

- Real-time AI response streaming
- Interactive ChatGPT-style interface
- Google Gemini LLM integration
- Python FastAPI REST API
- Server-Sent Events (SSE) streaming
- Stop response generation
- New chat functionality
- Responsive web interface
- Error handling and input validation
- Secure environment variable configuration
- Interactive Swagger API documentation

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Backend | Python FastAPI |
| AI Model | Google Gemini |
| AI SDK | Google GenAI |
| Build Tool | Vite |
| Streaming | Server-Sent Events |
| Web Server | Uvicorn |
| Styling | CSS |
| Version Control | Git and GitHub |

## System Architecture

```text
User
  |
  v
React Frontend
  |
  | HTTP POST Request
  v
Python FastAPI Backend
  |
  v
Google Gemini API
  |
  | Streaming Response
  v
FastAPI StreamingResponse
  |
  v
React Real-Time Chat Interface
```

## Project Structure

```text
ai-streaming-chat/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── index.html
├── .gitignore
└── README.md
```

## Prerequisites

Before running the application, install:

- Python 3.13
- Node.js
- npm
- Git
- Visual Studio Code (optional)
- Google Gemini API key

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/kkshahi18/ai-streaming-chat.git
cd ai-streaming-chat
```

### 2. Configure the backend

The following commands are intended for Windows PowerShell.

```powershell
cd backend
py -3.13 -m venv .venv
```

Install the required Python dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure Gemini API credentials

Obtain your Gemini API key from Google AI Studio:

https://aistudio.google.com/apikey

Create a local environment configuration file:

```powershell
Copy-Item .env.example .env
```

Update the `.env` file:

```dotenv
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Replace the placeholder with your actual API key. Select a Gemini model available to your account if the configured model is unavailable.

### 4. Start the backend server

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

Backend URL:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

### 5. Configure the frontend

Open a new terminal from the project root:

```powershell
cd frontend
npm.cmd install
```

Start the React development server:

```powershell
npm.cmd run dev
```

### 6. Access the application

Open the following URL in your browser:

http://localhost:5173

Keep both the backend and frontend servers running.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API home endpoint |
| GET | /health | Backend health check |
| POST | /chat/stream | Generate and stream AI responses |
| GET | /docs | Interactive API documentation |

### Example API Request

```json
{
  "message": "Explain artificial intelligence with examples."
}
```

### Example Streaming Response

```text
data: {"type":"chunk","text":"Artificial intelligence"}

data: {"type":"chunk","text":" enables machines to perform intelligent tasks."}

data: {"type":"done"}
```

## How AI Streaming Works

1. The user submits a question through the React interface.
2. React sends an HTTP POST request to FastAPI.
3. FastAPI communicates with the Google Gemini API.
4. Gemini generates the response in incremental chunks.
5. FastAPI streams the generated chunks using SSE.
6. React receives and displays the response progressively.

This approach improves perceived responsiveness by displaying available text before the complete AI response has been generated.

## Security

- API credentials must be stored in the backend `.env` file.
- Never commit API keys to GitHub.
- Never expose API credentials in frontend JavaScript.
- The `.env.example` file contains placeholder values only.
- Each developer should configure their own Gemini API key.
- API usage is subject to Google's applicable quotas, pricing, and rate limits.

Authentication, rate limiting, and additional security controls are recommended before deploying the application for unrestricted public access.

## Troubleshooting

| Error | Possible Solution |
|---|---|
| Failed to fetch | Check whether FastAPI is running and verify CORS settings |
| Invalid API key | Verify Gemini API credentials |
| 429 Resource Exhausted | Check API quotas and rate limits |
| 404 Model Not Found | Verify the configured Gemini model |
| ModuleNotFoundError | Install backend dependencies |
| npm execution policy error | Use npm.cmd in Windows PowerShell |

## Future Enhancements

- Conversation memory
- Persistent chat history
- Markdown and code syntax highlighting
- User registration and authentication
- Multiple LLM provider integration
- OpenAI, Groq, and Ollama integration
- Retrieval-Augmented Generation (RAG)
- PDF and document question answering
- Voice-based interaction
- Token usage and API cost monitoring
- Docker containerization
- CI/CD using GitHub Actions
- Cloud deployment
- Automated testing

## Learning Objectives

This project demonstrates practical knowledge of:

- AI application development
- Large Language Model integration
- Python backend development
- React frontend development
- REST API development
- Real-time HTTP streaming
- Asynchronous communication
- Secure API configuration
- Full-stack application architecture
- Git and GitHub version control

## Contributions

Suggestions, bug reports, and feature proposals are welcome through GitHub Issues and Pull Requests.

## License

A project license will be specified separately. Public visibility alone does not grant permission to redistribute or modify the source code.

## Author

**Krishna Kirti Shahi**

IT Project Management | AI Application Development | Digital Transformation

GitHub: https://github.com/kkshahi18

---

Built with Python, React, FastAPI, and Google Gemini.

If you find this project useful, consider giving the repository a star.