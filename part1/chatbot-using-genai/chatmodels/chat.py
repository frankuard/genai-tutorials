from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv()

model = init_chat_model(
    "openai/gpt-oss-120b",
    model_provider="groq"
)

response = model.invoke("Hello! How are you today")

print(response.content)

