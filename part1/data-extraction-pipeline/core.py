from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import os
load_dotenv()


model = init_chat_model(
    "openai/gpt-oss-120b",
    model_provider="groq"
)

prompt = ChatPromptTemplate.fromtemplate("system","""
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

Text:
{text}
""")

response = model.invoke("Interstellar is a 2014 science-fiction film directed by Christopher Nolan and written by Christopher Nolan and Jonathan Nolan. The story is set in a future where Earth is suffering from severe environmental problems, including widespread crop failures, dust storms, and food shortages. Cooper, played by Matthew McConaughey, is a former NASA pilot and engineer who lives on a farm with his children, Murph and Tom. Although Cooper has become a farmer, he still has a strong interest in science and space exploration. Cooper discovers that NASA is secretly operating a mission to find a new habitable planet for humanity. A wormhole has appeared near Saturn, providing a possible route to distant parts of the galaxy. Cooper joins the mission alongside scientists including Amelia Brand, played by Anne Hathaway. Their goal is to investigate several planets located near a massive black hole called Gargantua and determine whether any of them could support human life. One of the major scientific concepts in the movie is time dilation caused by intense gravity. When Cooper and Amelia visit Miller's planet, which is extremely close to Gargantua, time passes much more slowly there compared with Earth. After spending only a short period on the planet, they discover that many years have passed for people farther away from the black hole. This becomes one of the movie's most emotional consequences because Cooper loses years of his children's lives while he is away. Meanwhile, Murph grows up and becomes a scientist working to solve the problem of Earth's survival. She eventually discovers that gravity can be manipulated in a way that allows humanity to escape Earth. Cooper later enters Gargantua and experiences a strange higher-dimensional environment represented by a structure called the tesseract. From there, he is able to communicate with Murph across time by manipulating gravity. Cooper uses gravitational signals to send important information to Murph, allowing her to complete the equation needed to solve humanity's problem. The movie explores themes including love, family, sacrifice, survival, exploration, time, gravity, and humanity's desire to understand the universe. It also examines the conflict between scientific knowledge and human emotion, particularly through Cooper's relationship with Murph. The film's scientific concepts were developed with assistance from physicist Kip Thorne, whose work influenced the movie's depiction of black holes, wormholes, relativity, and gravitational effects. Interstellar received widespread critical acclaim for its visual effects, scientific ambition, music by Hans Zimmer, cinematography, and emotional storytelling. It became particularly well known for its depiction of Gargantua and its attempt to present scientifically inspired ideas about space and time within a mainstream science-fiction film. can you please extract the summary and information of the movie")


print(response.content)