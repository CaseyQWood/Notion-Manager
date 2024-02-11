import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from conversation import Conversation
from models.chat_models import Message

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

tools = []

SYSTEM_PROMPT = "You are a helpful assistant that is trying to help a user"

convo = Conversation(SYSTEM_PROMPT)


@app.post("/chat-completion")
async def root(user_message: Message):

    convo.add_user_message(user_message)

    response: Message = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=convo.get_messages(),
        # tools=tools,
        # tool_choice="auto",
    )

    convo.add_assistant_message(response.choices[0].message)

    return {"response": response.choices[0].message}
