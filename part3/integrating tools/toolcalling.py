from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain.tools import tool
from rich import print

# creating a tool


@tool

def get_text_length(text: str) -> int :
    """Returns the number of character in a given text"""
    
    return len(text)

llm = ChatGroq(
    model= "openai/gpt-oss-120b"
)


# tool binding

llm_with_tool = llm.bind_tools([get_text_length])

result = llm.invoke("Hello")
result2 = llm.invoke("Hello")


print(result)
print()
print()
print()
print()
print(result2)