import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from agent_script import invoke_our_graph, create_graph
import asyncio
import nest_asyncio
import time
import requests
import streamlit.components.v1 as components
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


load_dotenv()

st.set_page_config(layout="centered")
st.markdown(
    """
    <style>
    .stMainBlockContainer {
        max-width: 80rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "player_track" not in st.session_state:
        st.session_state.player_track = "6WzRpISELf3YglGAh7TXcG"
#player_track: str = "6WzRpISELf3YglGAh7TXcG"
with st.sidebar:
    st.title("Player")
    components.html(
        f"""
        <iframe data-testid="embed-iframe" style="border-radius:12px"
        src="https://open.spotify.com/embed/track/{st.session_state.player_track}?utm_source=generator&theme=0"
            width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        """,
            height=400,
            width=400
    )
    prompt = st.chat_input(placeholder="Enter song ID")
    if prompt:
        st.session_state.player_track = prompt

st.image(image="spotify-agent-logo.png", width=400)

if "messages" not in st.session_state:

    st.session_state["messages"] = [AIMessage(content="How can I help you?")]

if "agent" not in st.session_state:

    st.session_state["agent"] = asyncio.run(create_graph())

   

agent = st.session_state["agent"]

for msg in st.session_state.messages:

    if type(msg) == AIMessage:

        st.chat_message("assistant", avatar="robot_2_24dp_999999_FILL0_wght400_GRAD0_opsz24.svg").write(msg.content)

    if type(msg) == HumanMessage:

        st.chat_message("user", avatar="mood_24dp_999999_FILL0_wght400_GRAD0_opsz24.svg").write(msg.content)


if prompt := st.chat_input(width="stretch"):

    st.session_state.messages.append(HumanMessage(content=prompt))

    st.chat_message("user", avatar="mood_24dp_999999_FILL0_wght400_GRAD0_opsz24.svg").write(prompt)

    with st.chat_message("assistant", avatar="robot_2_24dp_999999_FILL0_wght400_GRAD0_opsz24.svg"):

        serialized_messages = [msg.dict() if hasattr(msg, 'dict') else msg for msg in st.session_state.messages]

        output = requests.post(BACKEND_URL + "/chat", json={"input": serialized_messages})

        output = output.json()

        print("\n\n")
        print("OUTPUT")
        print(output)
        print("\n\n")

        text = output["response"]["messages"][-1]['content']

        print(text)

        placeholder = st.empty()

        streamed_text = ""

        for token in text.split():

            streamed_text += token + " "

            placeholder.write(streamed_text)

            time.sleep(0.07)
        st.session_state.messages.append(AIMessage(content=text))
