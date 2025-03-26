from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
from pydantic.v1 import BaseModel, Field

class AgentState(BaseModel):
    """State class for the agent workflow."""
    
    messages: List[BaseMessage] = Field(default_factory=list)
    current_step: str = Field(default="search")
    context: Dict[str, Any] = Field(default_factory=dict)
    search_results: List[Dict[str, Any]] = Field(default_factory=list)

    def update_messages(self, new_messages: List[BaseMessage]):
        self.messages.extend(new_messages)

    def update_current_step(self, new_step: str):
        self.current_step = new_step

    def update_search_results(self, new_results: List[Dict[str, Any]]):
        self.search_results.extend(new_results)

    def update_context(self, new_context: Dict[str, Any]):
        self.context.update(new_context)

    def reset(self):
        self.messages = []
        self.current_step = "search"
        self.search_results = []
        self.context = {}

    def to_dict(self):
        return {
            "messages": [{"type": msg.type, "content": msg.content} for msg in self.messages],
            "current_step": self.current_step,
            "search_results": self.search_results,
            "context": self.context
        }

    class Config:
        arbitrary_types_allowed = True 