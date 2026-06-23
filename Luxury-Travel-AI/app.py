import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# ---------------------------
# Load Environment Variables
# ---------------------------

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------
# Load Large System Prompt
# ---------------------------

with open("system_prompt_enhanced.txt","r",encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


# ---------------------------
# Page Config
# ---------------------------

st.set_page_config(
    page_title="Aurora Luxury Travel Consultant",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Aurora Luxury Travel Consultant")
st.write("Curated premium travel experiences.")

# ---------------------------
# Initialize Chat History
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        }
    ]


# ---------------------------
# Display Chat
# ---------------------------

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------------------
# User Input
# ---------------------------

prompt = st.chat_input(
    "Ask Aurora about luxury destinations..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Designing your luxury journey..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1500
            )

            reply = response.choices[0].message.content

            st.markdown(reply)

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":reply
                }
            )