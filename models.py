import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr
from tools import tools

load_dotenv()

# Keep API keys typed correctly for LangChain stubs (SecretStr | None)
_groq_api_key = os.getenv("GROQ_API_KEY")

# Groq Llama 3:  "Fast Analyst"
# Using this for quick summaries or formatting
groq_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=SecretStr(_groq_api_key) if _groq_api_key else None,
)

# Bind the tools to Groq.
groq_with_tools = groq_model.bind_tools(tools)
