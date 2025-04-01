from typing import Literal, TypedDict, Union
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.state import CompiledStateGraph

# Define the possible agent types
AgentTypes = Literal[
    "service_selection",
    "package_selection", 
    "scheduling",
    "confirmation",
    "__end__"
]

class State(TypedDict):
    """The state of the workflow."""
    messages: list[HumanMessage]  # The messages in the conversation
    current_agent: str  # The current agent handling the conversation
    selected_service: str | None  # The selected service
    selected_package: str | None  # The selected package
    selected_date: str | None  # The selected date
    selected_time: str | None  # The selected time

# Create the supervisor LLM
supervisor_llm = ChatAnthropic(model_name="claude-3-sonnet-20240229", timeout=120, stop=None)

SUPERVISOR_SYSTEM_PROMPT = """You are a supervisor agent managing a salon booking workflow. Your role is to route conversations to the appropriate specialized agent based on the current state and user's needs.

The available specialized agents are:
1. Service Selection Agent - Handles selecting salon services
2. Package Selection Agent - Handles selecting service packages
3. Scheduling Agent - Handles appointment scheduling
4. Confirmation Agent - Handles booking confirmation

Your responsibilities:
1. Analyze user messages and current state
2. Route to the appropriate agent
3. Maintain conversation context
4. Handle transitions between agents
5. Ensure booking flow completion

The typical booking flow is:
1. Select service
2. Select package (if applicable)
3. Schedule appointment
4. Confirm booking

However, users may need to go back to previous steps or skip steps if they already know what they want.

Always consider:
1. Current state of the booking
2. User's immediate needs
3. Required information for next steps
4. Logical flow of the booking process"""

def route_message(state: State) -> AgentTypes:
    """Route the message to the appropriate agent."""
    # Get the latest message
    messages = [
        {"role": "system", "content": SUPERVISOR_SYSTEM_PROMPT},
    ] + [{"role": m.type, "content": m.content} for m in state["messages"]]
    
    # Ask the LLM to decide which agent should handle this
    response = supervisor_llm.invoke(messages)
    
    # Extract the routing decision
    # This is a simplified version - you might want to add more sophisticated routing logic
    if isinstance(response.content, str):
        content = response.content.lower()
        
        if "service" in content:
            return "service_selection"
        elif "package" in content:
            return "package_selection"
        elif "schedule" in content or "time" in content or "date" in content:
            return "scheduling"
        elif "confirm" in content or "book" in content:
            return "confirmation"
    
    return "__end__"

def create_graph() -> Union[StateGraph, CompiledStateGraph]:
    """Create the workflow graph."""
    # Initialize the graph
    workflow = StateGraph(State)
    
    # Add the supervisor node
    workflow.add_node("supervisor", route_message)
    
    # Add placeholder nodes for each agent
    # These will be replaced with actual agent nodes later
    workflow.add_node("service_selection", lambda x: x)
    workflow.add_node("package_selection", lambda x: x)
    workflow.add_node("scheduling", lambda x: x)
    workflow.add_node("confirmation", lambda x: x)
    
    # Add the starting edge from START to supervisor
    workflow.add_edge(START, "supervisor")
    
    # Add edges from supervisor to each agent
    workflow.add_conditional_edges(
        "supervisor",
        route_message,
        {
            "service_selection": "service_selection",
            "package_selection": "package_selection",
            "scheduling": "scheduling",
            "confirmation": "confirmation",
            "__end__": END
        }
    )
    
    # Add edges from each agent back to supervisor
    for agent in ["service_selection", "package_selection", "scheduling", "confirmation"]:
        workflow.add_edge(agent, "supervisor")
    
    # Compile the workflow before returning
    return workflow.compile()