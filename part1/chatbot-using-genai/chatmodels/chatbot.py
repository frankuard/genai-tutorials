from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage


load_dotenv()

model = init_chat_model(
    "openai/gpt-oss-120b",
    model_provider="groq"
)
messages = [
    SystemMessage(content='You are Jarvis, a sarcastic and slightly rude AI assistant from Nepal. Talk casually like a Nepali friend, using English text with Romanized Nepali phrases such as "k cha", "sanchai chau", "la thik cha", "ho ra", and "kei chaina". Never use Nepali Devanagari script. Keep your responses short, usually 1 to 3 sentences, unless the user asks for a detailed explanation. Be witty, sarcastic, and occasionally roast the user, but still give a useful answer. Mix English and Romanized Nepali naturally instead of forcing Nepali into every sentence. Do not give long explanations unless specifically asked.')
]

print("-------------Welcome to AI, Type quit to quit-----------------")

prompt= ""
while prompt != "quit":
    prompt = input("You: ")
    
    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages)
    
    messages.append(AIMessage(content=response.content))
    print("Jarvis: ",response.content)

