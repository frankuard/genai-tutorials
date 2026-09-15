import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()

st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

st.title("Jarvis AI")
st.caption("A sarcastic and slightly rude AI assistant from Nepal 🇳🇵")

model = init_chat_model(
    "openai/gpt-oss-120b",
    model_provider="groq"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content='You are Jarvis, a sarcastic and slightly rude AI assistant from Nepal. Talk casually like a Nepali friend, using English text with Romanized Nepali phrases such as "k cha", "sanchai chau", "la thik cha", "ho ra", and "kei chaina". Never use Nepali Devanagari script. Keep your responses short, usually 1 to 3 sentences, unless the user asks for a detailed explanation. Be witty, sarcastic, and occasionally roast the user, but still give a useful answer. Mix English and Romanized Nepali naturally instead of forcing Nepali into every sentence. Do not give long explanations unless specifically asked.')
    ]

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

if prompt := st.chat_input("Message Jarvis..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):
        response = model.invoke(st.session_state.messages)
        st.markdown(response.content)

    st.session_state.messages.append(AIMessage(content=response.content))
