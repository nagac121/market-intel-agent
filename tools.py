import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# We define the search tool. 
# k=3 means it will find the top 3 most relevant search results.
# This keeps it fast and under the free-tier limit.
search_tool = TavilySearchResults(
    k=3,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

# You can add more tools here later (e.g., a PDF reader or a Calculator)
tools = [search_tool]
