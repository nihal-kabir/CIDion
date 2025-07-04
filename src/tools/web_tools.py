"""
Web search and scraping tools.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from src.tools.base import Tool

class WebSearchTool(Tool):
    """Tool for searching the web using DuckDuckGo."""
    
    @property
    def name(self) -> str:
        return "web_search"
    
    @property
    def description(self) -> str:
        return "Search the web for information"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, query: str, max_results: int = 5) -> str:
        """Search the web for information."""
        try:
            # Using DuckDuckGo instant answer API (simplified)
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            
            # Add abstract if available
            if data.get("Abstract"):
                results.append(f"Summary: {data['Abstract']}")
            
            # Add related topics
            if data.get("RelatedTopics"):
                results.append("Related information:")
                for topic in data["RelatedTopics"][:max_results]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append(f"- {topic['Text']}")
            
            # Add answer if available
            if data.get("Answer"):
                results.append(f"Direct answer: {data['Answer']}")
            
            return "\n".join(results) if results else f"No specific results found for '{query}'. Consider refining your search."
            
        except Exception as e:
            return f"Error searching web: {str(e)}"

class WebScrapeTool(Tool):
    """Tool for scraping content from a webpage."""
    
    @property
    def name(self) -> str:
        return "scrape_webpage"
    
    @property
    def description(self) -> str:
        return "Scrape content from a webpage"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL of the webpage to scrape"
                },
                "max_length": {
                    "type": "integer",
                    "description": "Maximum length of content to return",
                    "default": 2000
                }
            },
            "required": ["url"]
        }
    
    async def execute(self, url: str, max_length: int = 2000) -> str:
        """Scrape content from a webpage."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit length
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return f"Content from {url}:\n\n{text}"
            
        except Exception as e:
            return f"Error scraping webpage: {str(e)}"
