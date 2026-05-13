from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import httpx
import os
from bs4 import BeautifulSoup
import json

load_dotenv()

#initialise the MCP server, with name of the server
mcp = FastMCP("tech_latest_news")

# Name of the application
USER_AGENT = "news-app/1.0"

NEWS_SITES = {
    "arstechnica": "https://arstechnica.com"
}

async def fetch_news(url: str):
     """It pulls and summarizes the latest news from the specified news site."""
     async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs[:5]]) 
            return text
        except httpx.TimeoutException:
            return "Timeout error"


# this indicates that the below function is MCP tool, exposed to agent for access
@mcp.tool()
async def get_tech_news(source: str):
    #below docstring is important for the model to understand how the tool works
    """
    Fetches the latest news from a specific tech news source.

    Args:
    source: Name of the news source (for example, "arstechnica" or "techcrunch").

    Returns:
    A brief summary of the latest news.
    """

    if source not in NEWS_SITES:
        raise ValueError(f"Sorry, I don't have access to news from {source}.")
    
    news_text = await fetch_news(NEWS_SITES[source])
    return news_text

if __name__ == "__main__":
    mcp.run(transport="stdio")