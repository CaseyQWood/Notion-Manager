import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")

client = OpenAI(api_key=openai_api_key, organization=openai_organization)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class Message(BaseModel):
    role: str
    content: str
    function_call: Optional[str] = None
    tool_calls: Optional[str] = None


@app.get("/chat-completion")
async def root():

    # response: Message = client.chat.completions.create(
    #     model="gpt-4-turbo-preview",
    #     messages=convo.get_messages(),
    #     tools=tools,
    #     tool_choice="auto",
    # )

    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}
