import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from pydantic import SecretStr
from tools import tools

load_dotenv()

# Keep API keys typed correctly for LangChain stubs (SecretStr | None)
_google_api_key = os.getenv("GOOGLE_API_KEY")
_groq_api_key = os.getenv("GROQ_API_KEY")

# Gemini 2.0 Flash: "Deep Researcher"
# Use this for processing large amounts of web data
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=SecretStr(_google_api_key) if _google_api_key else None
)

# Bind Tavily (and other) tools so Gemini can decide to search.
model_with_tools = gemini_model.bind_tools(tools)

# Groq Llama 3:  "Fast Analyst"
# Using this for quick summaries or formatting
groq_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=SecretStr(_groq_api_key) if _groq_api_key else None
)

# Bind the tools to Groq.
groq_with_tools = groq_model.bind_tools(tools)