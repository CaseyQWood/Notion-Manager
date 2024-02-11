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


@app.get("/chat-completion")
async def root():

    convo.add_user_message(
        Message(
            role="user",
            content="I need help with my taxes",
        )
    )

    print("HERE", convo.get_messages())

    response: Message = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=convo.get_messages(),
        # tools=tools,
        # tool_choice="auto",
    )

    return {"response": response}
