from typing import Any, Dict, Tuple
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

import time

from salonist.booking.state import State
from salonist.booking.tool import tool
from salonist.booking.prompts import BOOKING_SYSTEM_PROMPT

class BookingWorkflow:
    """A class to manage the booking agent workflow."""
    
    def __init__(self):
        """Initialize the workflow with required clients."""
        self.llm = ChatAnthropic(
            model_name="claude-3-5-sonnet-20240620",
        )
        tools = [tool]
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.memory = MemorySaver()
        self.graph = self._create_graph()

    def chatbot(self, state: State) -> Dict[str, list]:
        """Process messages using the LLM.
        
        Args:
            state: Current state of the workflow
            
        Returns:
            Dictionary with messages list
        """
        response = self.llm_with_tools.invoke(state.messages)
        return {"messages": [response]}
    
    def _create_graph(self) -> CompiledStateGraph:
        """Create and configure the workflow graph.
        
        Returns:
            Configured and compiled workflow graph
        """
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self.chatbot)

        tool_node = ToolNode(tools=[tool])
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
        )
        # Any time a tool is called, we return to the chatbot to decide the next step
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.set_entry_point("chatbot")
        graph_builder.add_edge("chatbot", END)
        return graph_builder.compile(checkpointer=self.memory)
    
    def run(self, query: str, user_id: str) -> Tuple[str, float]:
        """Run the booking workflow with a given query.
        
        Args:
            query: The user's query to process
            user_id: Unique identifier for the user's session
            
        Returns:
            Tuple of (response, processing_time)
        """
        start_time = time.time()
        
        # Create initial state with system prompt and user query
        initial_state = {
            "messages": [
                SystemMessage(content=BOOKING_SYSTEM_PROMPT),
                HumanMessage(content=query)
            ]
        }
        
        # Run the workflow with thread_id for memory management
        result = self.graph.invoke(initial_state, {"configurable": {"thread_id": user_id}})
        
        output = State(**result)
        
        # Get the last message from the dictionary result
        last_message = output.messages[-1]
        
        if not isinstance(last_message, AIMessage):
            raise ValueError("Expected AI message as final response")
            
        processing_time = time.time() - start_time
        return str(last_message.content), processing_time 