# EasyTrip-Agent

LangGraph-powered travel assistant that searches flights and the web to help plan trips.

## Features

- Conversational trip planning UI
- Flight search tool
- Web research via Tavily
- Flask frontend + LangGraph backend

## Project Structure

```text
EasyTrip-Agent/
├── app.py              # Flask web application
├── backend.py          # LangGraph agent graph
├── test.py             # Quick smoke tests
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
└── tools/
    ├── __init__.py
    ├── flight_tool.py
    └── tavily_tool.py
```

## Prerequisites

- Python 3.10+
- API keys for OpenAI (or your LLM provider) and Tavily

## Setup

```bash
cd EasyTrip-Agent
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Docker

```bash
docker build -t easytrip-agent .
docker run -p 5000:5000 --env-file .env easytrip-agent
```

## License

MIT
