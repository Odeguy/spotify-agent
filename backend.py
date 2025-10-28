from fastapi import FastAPI

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

    message: str

@app.post("/chat")

async def chat(query):

    agent = app.state.agent

    response = await invoke_our_graph(agent, query.input)

    if agent is None:

        return {"error": "Agent not initialized"}

    print(response)

    return {"response": response}