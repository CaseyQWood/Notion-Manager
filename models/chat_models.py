from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str
    function_call: Optional[str] = None
    tool_calls: Optional[str] = None
