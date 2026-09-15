from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import os
load_dotenv()


model = init_chat_model(
    "openai/gpt-oss-120b",
    model_provider="groq"
)

prompt = ChatPromptTemplate.from_messages([
    ("system","""
You are an information extraction assistant.

Analyze the following text and extract the most useful information about the movie.

Provide the answer in clear, simple plain text. Do not use JSON.

Include the following sections:

Movie Information:
- Movie name
- Release year
- Genre
- Director
- Writers
- Main cast and the characters they play

Story Information:
- Main characters
- Setting
- Main plot
- Important events
- Important locations

Themes:
- Main themes explored in the movie

Scientific or Technical Concepts:
- Important scientific or technical concepts mentioned
- Brief explanation of each concept

Production Information:
- Composer or music
- Important collaborators
- Other notable production details

Reception:
- Critical reception or impact mentioned in the text

Quick Summary:
- Give a short summary of the entire text in 2 to 4 sentences.

Important rules:
- Only use information provided in the text.
- Do not invent information.
- If something is not mentioned, say "Not mentioned."
- Keep the information concise and easy to read.
- Do not use JSON.
- Do not provide unnecessary explanations.
"""
),
('human',"""
 Extract information from this paragraph:
 
 {paragraph}
 """)
])


para = input("Give your paragraph: ")


final_prompt = prompt.invoke(
    {"paragraph": para}
    )

response = model.invoke(final_prompt)


print(response.content)