from typing import List, Dict, Any, Literal, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START
from ..tool import AvailabilityTool

class SchedulingState(TypedDict):
    """The state of the scheduling workflow."""
    messages: list[BaseMessage]
    current_agent: str

# Initialize the tools
availability_tool = AvailabilityTool()

# Create the LLM
scheduling_llm = ChatAnthropic(model_name="claude-3-sonnet-20240229", timeout=120, stop=None)

# Create the scheduling agent with prompt
SCHEDULING_SYSTEM_PROMPT = """You are a Scheduling Agent for a salon booking system. Your role is to help users find and book available time slots.

Your responsibilities:
1. Check availability for requested dates/times
2. Help users find suitable slots
3. Handle date/time selection
4. Validate time slot availability
5. Store selected time slot in state

You have access to the availability tool that can check:
- Specific dates in YYYY-MM-DD format
- "today" for today's availability  
- "tomorrow" for tomorrow's availability
- "next_week" for next week's availability

Always:
1. Be polite and professional
2. Confirm selections before proceeding
3. Handle timezone considerations
4. Provide clear options
5. Help users find alternative slots if their preferred time is unavailable"""

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SCHEDULING_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
])

# Create the agent
scheduling_agent = create_react_agent(
    model=scheduling_llm,
    tools=[availability_tool],
    prompt=prompt
)

def scheduling_node(state: Dict) -> Dict:
    """The scheduling agent node in the graph."""
    # Get the latest message
    messages = state.get("messages", [])
    
    # Run the agent on the messages
    result = scheduling_agent.invoke({"messages": messages})
    
    # Add agent response to messages
    if isinstance(result, dict) and "messages" in result:
        new_messages = result["messages"]
    else:
        new_messages = [AIMessage(content=str(result))]
    
    # Return the updated state
    return {
        "messages": new_messages,
        "current_agent": "scheduling"
    }

# Create the workflow
workflow = StateGraph(SchedulingState)

# Add the scheduling node
workflow.add_node("scheduling", scheduling_node)

# Add the starting edge
workflow.add_edge(START, "scheduling")

# Compile the workflow
workflow = workflow.compile() 