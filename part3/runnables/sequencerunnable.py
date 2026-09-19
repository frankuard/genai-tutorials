from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
## PROMPT TEMPLATE

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words"
)

## Model 

model = ChatGroq(
    model ="openai/gpt-oss-120b",
)

## Output parser

parser = StrOutputParser()

# ## Step by step manual flow 

# ## format the prompt 

# formatted_prompt = prompt.format_messages(topic="Machine Learning")

# ## call the model manually

# response = model.invoke(formatted_prompt)


# ## parse the output manually

# final_output = parser.parse(response.content)

# print(final_output)


chain = prompt | model | parser

result = chain.invoke("Machine Learning")

print(result)
