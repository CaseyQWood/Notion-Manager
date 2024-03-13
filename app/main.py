"""This is main file for the Nexus_Back API."""

import os
import time
import anthropic

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from icecream import ic
from openai import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
from pydantic import BaseModel

## Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")
database_url = os.getenv("DATABASE_URL")

## Initialize clients
client = OpenAI(api_key=openai_api_key, organization=openai_organization)
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

## Initialize database
Base = declarative_base()
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

## Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class UserMessage(BaseModel):
    """User message model."""

    content: str


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    conversation = Column(String)


def wait_on_run(run, thread):
    """Wait for the run to complete."""
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


# @app.get("/get_messages")
# async def get_messages():
#     """Get the messages in the conversation."""

#     return convo.get_messages()


@app.post("/assistants")
async def chat_complete(user_message: UserMessage):
    """Adds message to thread and runs assistant."""

    ic(user_message)

    # thread = client.beta.threads.create()

    my_thread = client.beta.threads.retrieve("thread_imcQEbMQjglqdarbtfmY3teq")

    client.beta.threads.messages.create(
        thread_id=my_thread.id,
        role="user",
        content=user_message.content,
    )

    run = client.beta.threads.runs.create(
        thread_id=my_thread.id,
        assistant_id="asst_kcp9EnAFTB7BvkGmfJqxWdEH",
        instructions="Please address the user as Jane Doe. The user has a premium account.",
    )

    run = client.beta.threads.runs.retrieve(thread_id=my_thread.id, run_id=run.id)

    wait_on_run(run, my_thread)

    messages = client.beta.threads.messages.list(thread_id=my_thread.id)

    return messages.data


@app.post("/anthropic/message")
async def add_message(user_message: UserMessage):
    """Adds message to Anthropic conversation and returns response."""

    message = anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.0,
        system="Respond only in Yoda-speak.",
        messages=[{"role": "user", "content": "How are you today?"}],
    )

    ## Add message to database
    new_user = User(name="John Doe", conversation="johndoe@example.com")
    session.add(new_user)
    session.commit()

    users = session.query(User).all()
    for user in users:
        print(user.name, user.conversation)

    print(message.content)
    return message.content
