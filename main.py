import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from icecream import ic
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# from models.chat_models import UserMessage


class UserMessage(BaseModel):
    """User message model."""

    content: str


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
async def add_message(user_message: UserMessage):
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
