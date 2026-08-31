# 🤖 AI-Powered Daily Trend Research & Content Generation Agent

An autonomous AI agent that researches the latest AI and technology trends from the web and automatically generates platform-specific social media content for **LinkedIn**, **Instagram**, and **Twitter/X**.

---

## ✨ Features

- 🔍 **Real-time Web Research** — Uses Tavily to search and retrieve current AI trends
- 🤖 **LangChain Agent** — Autonomous reasoning and tool usage with LangChain
- 📝 **Multi-Platform Content** — Generates LinkedIn posts, Instagram captions, and Twitter/X threads
- 💾 **Auto Report Saving** — Saves daily JSON reports to the `reports/` folder
- 🌐 **Streamlit UI** — Clean web interface to generate content on demand
- ⏰ **Scheduler** — Automatically runs the agent on a schedule

---

## 🏗️ Project Structure

```
├── agent.py          # Core LangChain agent with Tavily search tool
├── app.py            # Streamlit web UI
├── scheduler.py      # APScheduler for automated daily runs
├── reports/          # Auto-generated JSON reports (git ignored)
├── requirements.txt  # Python dependencies
└── .env              # API keys (NOT pushed to GitHub)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Powered-Daily-Trend-Research-and-Content-Generation-Agent.git
cd AI-Powered-Daily-Trend-Research-and-Content-Generation-Agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
TAVILY_API_KEY=your_tavily_api_key_here
OLLAMA_API_KEY=your_ollama_api_key_here
```

> ⚠️ **Never commit your `.env` file to GitHub!**

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

### 5. Run the CLI Agent

```bash
python agent.py
```

### 6. Run the Scheduler

```bash
python scheduler.py
```

---

## 🔑 API Keys Required

| Service | Purpose | Get API Key |
|---------|---------|-------------|
| [Tavily](https://tavily.com) | Web search | [tavily.com](https://tavily.com) |
| [Ollama](https://ollama.com) | LLM (via OpenAI-compatible API) | [ollama.com](https://ollama.com) |

---

## 📄 Output Format

The agent returns structured JSON:

```json
{
    "topic": "Trending AI topic",
    "summary": "Brief explanation of the trend",
    "sources": [
        { "title": "Source Title", "url": "https://..." }
    ],
    "linkedin": { "post": "Professional LinkedIn post..." },
    "instagram": {
        "caption": "Instagram caption...",
        "hashtags": ["#AI", "#MachineLearning"]
    },
    "twitter": {
        "thread": ["Tweet 1", "Tweet 2", "Tweet 3", "Tweet 4", "Tweet 5"]
    }
}
```

---

## 🛠️ Tech Stack

- **[LangChain](https://langchain.com)** — Agent framework
- **[Tavily](https://tavily.com)** — Real-time web search
- **[Streamlit](https://streamlit.io)** — Web UI
- **[APScheduler](https://apscheduler.readthedocs.io)** — Task scheduling
- **[Ollama](https://ollama.com)** — LLM provider

---

## 📜 License

MIT License — feel free to use and modify.
