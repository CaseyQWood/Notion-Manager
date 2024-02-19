from pydantic import BaseModel


class UserMessage(BaseModel):
    """User message model."""

    content: str
