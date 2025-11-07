import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from agent_script import invoke_our_graph, create_graph
import asyncio
import nest_asyncio
import time
import requests


load_dotenv()  # Load environment variables from a .env file if present

st.title("🎵Spotify Agent🎵")

if "messages" not in st.session_state:

    # default initial message to render in message state

    st.session_state["messages"] = [AIMessage(content="How can I help you?")]

if "agent" not in st.session_state:

    st.session_state["agent"] = asyncio.run(create_graph())

   

agent = st.session_state["agent"]

for msg in st.session_state.messages:

   

    if type(msg) == AIMessage:

        st.chat_message("assistant").write(msg.content)

    if type(msg) == HumanMessage:

        st.chat_message("user").write(msg.content)

# takes new input in chat box from user and invokes the graph

if prompt := st.chat_input():

    st.session_state.messages.append(HumanMessage(content=prompt))

    st.chat_message("user").write(prompt)


    # Process the AI's response and handles graph events using the callback mechanism

    with st.chat_message("assistant"):

        serialized_messages = [msg.dict() if hasattr(msg, 'dict') else msg for msg in st.session_state.messages]

        output = requests.post("http://localhost:8000/chat", json={"input": serialized_messages})

        output = output.json()

        text = output["response"]["messages"][-1]['content']

        print(text)

        placeholder = st.empty()

        streamed_text = ""

        for token in text.split():

            streamed_text += token + " "

            placeholder.write(streamed_text)

            time.sleep(0.07)  # Adjust speed as needed


        st.session_state.messages.append(AIMessage(content=text))