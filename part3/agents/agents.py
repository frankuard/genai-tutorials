from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print
# weather tool


@tool
def get_weather(city:str) -> str:
    """
    Get the current weather for a city.

    Use this tool when the user asks about:
    - current weather
    - temperature
    - humidity
    - wind
    - weather conditions
    """
    
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},NP&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    ## print("DEBUG:",data)
    
    if data.get('cod') != 200:
        return f"Error: {data.get('message',' Could not fetch weather')}"
    
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    
    return f"Weather in {city}: {desc}, {temp}℃"


## Tavily news tool

tavily_client =TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city:str) -> str:
    """
    Get latest news about the city
    """
    
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )
    
    results = response.get("results", [])
    
    if not results:
        return f"No news found for {city}"
    
    news_list = []
    
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")
        
        news_list.append(
            f"- {title}\n  🔗 {url}\n  📝 {snippet[:100]}..."
        )
    
    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


llm = ChatGroq(
    model="openai/gpt-oss-120b"
)

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}   

llm_with_tool = llm.bind_tools([get_weather,get_news])

## creating agent loop (very imporant)

