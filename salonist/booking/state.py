from typing import List, Annotated
from langchain_core.messages import BaseMessage
from pydantic.v1 import BaseModel, Field
from langgraph.graph.message import add_messages

class State(BaseModel):
    """State for the booking workflow."""
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True 