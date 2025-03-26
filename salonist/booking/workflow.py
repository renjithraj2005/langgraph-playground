from typing import Any, Dict, Tuple
from langgraph.graph import StateGraph
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from pydantic.v1 import SecretStr
import time

from salonist.config import settings
from salonist.booking.state import State

class BookingWorkflow:
    """A class to manage the booking agent workflow."""
    
    def __init__(self):
        """Initialize the workflow with required clients."""
        self.llm = ChatAnthropic(
            model_name="claude-3-5-sonnet-20240620",
            api_key=SecretStr(settings.ANTHROPIC_API_KEY),
            timeout=30
        )
        self.graph = self._create_graph()
    
    def chatbot(self, state: State) -> Dict[str, list]:
        """Process messages using the LLM.
        
        Args:
            state: Current state of the workflow
            
        Returns:
            Dictionary with messages list
        """
        response = self.llm.invoke(state.messages)
        return {"messages": [response]}
    
    def _create_graph(self) -> Any:
        """Create and configure the workflow graph.
        
        Returns:
            Configured and compiled workflow graph
        """
        graph_builder = StateGraph(State)
        
        # Add the chatbot node
        graph_builder.add_node("chatbot", self.chatbot)
        
        # Set entry and finish points
        graph_builder.set_entry_point("chatbot")
        graph_builder.set_finish_point("chatbot")
        
        return graph_builder.compile()
    
    def run(self, query: str) -> Tuple[str, float]:
        """Run the booking workflow with a given query.
        
        Args:
            query: The user's query to process
            
        Returns:
            Tuple of (response, processing_time)
        """
        start_time = time.time()
        
        # Create initial state as dictionary
        initial_state = {"messages": [HumanMessage(content=query)]}
        
        # Run the workflow
        result = self.graph.invoke(initial_state)
        
        output  = State(**result)
        
        # Get the last message from the dictionary result
        last_message = output.messages[-1]
        
        if not isinstance(last_message, AIMessage):
            raise ValueError("Expected AI message as final response")
            
        processing_time = time.time() - start_time
        return str(last_message.content), processing_time 