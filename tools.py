import requests
from  langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from rich import print
from bs4 import BeautifulSoup

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool

def Web_Search(query: str) -> str:
    """
    Perform a web search using Tavily API and return the top results.
    and give recent and reliable information. The query should be a string representing
    the search term or question you want to look up. The function returns a string containing
    the search results or an error message if the search fails.
    The function uses the Tavily API to perform the search.
    """
    
    response = tavily.search(query=query, max_results=5)
    output = []
    for r in response["results"]:
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content']}\n")
    return "\n".join(output)


@tool
def Scrape_url(url : str) -> str:
    """
    Scrape the content of a given URL and return the text content.
    The function takes a string representing the URL to scrape.
    It returns a string containing the scraped text content or an error message if the scraping fails.
    """
    try:
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from the HTML
        text_content = soup.get_text(separator='\n', strip=True)
        return text_content[:3000]  # Return the first 3000 characters to avoid excessive output
    except requests.exceptions.RequestException as e:
        return f"Error scraping the URL: {e}"



