from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ChatMessage:
    """Chat message model."""
    content: str

@dataclass
class ChatResponse:
    """Chat response model."""
    message: str
    current_agent: str
    booking_state: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        return {
            "message": self.message,
            "current_agent": self.current_agent,
            "booking_state": self.booking_state
        } 