# 🤖 Deep Market Intelligence Agent (Multi-Agent System)

An autonomous AI research squad designed to perform deep-dive market analysis, verify sources, and generate strategy reports. Built with **LangGraph**, **Gemini 2.0**, and **Groq**.

---

## 🚀 Overview

Information moves faster than humans can read. This project implements a **Multi-Agent Orchestration** pattern to solve the "hallucination problem" in AI research. Unlike a simple chatbot, this system uses a **Stateful Graph** to coordinate specialized agents, ensuring that data is researched, analyzed, and critiqued before reaching the user.

### Key Highlights:

- **Human-in-the-Loop (HITL):** The agent pauses to ask for user approval after the research phase, preventing "runaway" costs and ensuring search quality.
- **Multi-Model Routing:** Uses **Gemini 2.0 Flash** for high-context research and **Groq (Llama 3.3)** for rapid analysis/reporting.
- **Persistence:** Leverages LangGraph's checkpointers to "remember" conversation state even if the session is interrupted.

---

## 🏗️ The Architecture

The system is built as a **Directed Acyclic Graph (DAG)** using LangGraph:

1. **The Researcher:** Uses Tavily Search API to gather real-time data from the web.
2. **The Human-in-the-Loop:** Displays found sources; waits for user feedback ("Proceed" or "Search more").
3. **The Analyst:** Synthesizes raw data into a structured SWOT analysis.
4. **The Critic:** Reviews the final report for accuracy and formatting.

---

## 🛠️ Tech Stack

- **Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph)
- **LLMs:** Google Gemini 2.0 Flash, Groq (Llama 3.3-70B)
- **Search Tool:** Tavily Search API
- **Observability:** [LangSmith](https://smith.langchain.com/) (Full trace monitoring)
- **Interface:** Streamlit (UI/UX)
- **Environment:** WSL2 / Python 3.10+

---

## 🚦 Getting Started

### 1. Prerequisites

- Python 3.10+
- API Keys for: Google AI Studio, Groq, Tavily, and LangSmith.

### 2. Installation

```bash
# Clone the repo
git clone https://github.com/nagac121/market-intel-agent.git
cd market-intel-agent

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
