from fastapi import FastAPI, Body

from pydantic import BaseModel

from agent_script import create_graph, invoke_our_graph

import asyncio

from contextlib import asynccontextmanager

from typing import List, Dict, Any

from dotenv import load_dotenv



load_dotenv()

@asynccontextmanager

async def lifespan(app: FastAPI):

    # Startup: Create the agent when the server starts

    print("Starting up... Creating Spotify agent...")

    app.state.agent = await create_graph()

    print("Agent created successfully!")

   

    yield  # Server is running


    # Shutdown: Clean up when server stops

    print("Shutting down...")

# Create FastAPI app with lifecycle management

app = FastAPI(

    title="Spotify Agent API",

    description="A FastAPI backend for the Spotify agent",

    lifespan=lifespan

)

class ChatQuery(BaseModel):
    input: list

@app.post("/chat")
async def chat(query: ChatQuery):

    agent = app.state.agent

    response = await invoke_our_graph(agent, query.input)

    if agent is None:
        return {"reponse": "kys"}

    print(response)

    return {"response": response}