import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from pydantic import SecretStr

load_dotenv()

# Keep API keys typed correctly for LangChain stubs (SecretStr | None)
_google_api_key = os.getenv("GOOGLE_API_KEY")
_groq_api_key = os.getenv("GROQ_API_KEY")

# Gemini 2.0 Flash: Our "Deep Researcher"
# Use this for processing large amounts of web data
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=SecretStr(_google_api_key) if _google_api_key else None
)

# Groq Llama 3: Our "Fast Analyst"
# Use this for quick summaries or formatting
groq_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=SecretStr(_groq_api_key) if _groq_api_key else None
)
