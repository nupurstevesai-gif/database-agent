from tavily import TavilyClient
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def web_search(query: str) -> str:
    """Search the web using Tavily and return the results."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = tavily_client.search(query, max_results=5)

    formatted = []
    for r in response["results"]:
        formatted.append(f"Title: {r['title']}\nContent: {r['content']}\n")

    return "\n---\n".join(formatted)

