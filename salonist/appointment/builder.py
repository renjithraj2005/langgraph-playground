import logging

from typing import Tuple
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from langgraph.graph import START, END
from langchain_anthropic import ChatAnthropic

from .state import State
from .base import Assistant
from .agents import get_runnable
from .prompts import info_agent_prompt, booking_agent_prompt, primary_agent_prompt
from .tools.tools import (set_appointment,
                         reschedule_appointment,
                         cancel_appointment,
                         check_availability_by_specialization,
                         check_availability_by_doctor
                         )
from .models.agents import ToAppointmentBookingAssistant, ToGetInfo, ToPrimaryBookingAssistant, CompleteOrEscalate
from .utils.helper import (
    create_tool_node_with_fallback,
    pop_dialog_state,
    RouteUpdater,
    route_to_workflow,
    route_primary_assistant,
    create_entry_node
)
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

conn = sqlite3.connect('checkpoints.db', check_same_thread=False)

memory = SqliteSaver(conn)

# TODO Enable later
# os.environ["LANGCHAIN_TRACING_V2"] = 'true'
# os.environ["LANGCHAIN_ENDPOINT"] = Azure_Creds.LANGCHAIN_ENDPOINT
# os.environ["LANGCHAIN_API_KEY"] = Azure_Creds.LANGCHAIN_API_KEY
# os.environ["LANGCHAIN_PROJECT"] = Azure_Creds.LANGCHAIN_PROJECT

llm = ChatAnthropic(model_name="claude-3-5-sonnet-20240620")  # type: ignore
info_tools = [check_availability_by_specialization, check_availability_by_doctor]
info_runnable = get_runnable(
    llm=llm,
    tools=info_tools + [CompleteOrEscalate],
    agent_prompt=info_agent_prompt
)

booking_tools = [set_appointment, reschedule_appointment, cancel_appointment]
booking_runnable = get_runnable(
    llm=llm,
    tools=booking_tools + [CompleteOrEscalate],
    agent_prompt=booking_agent_prompt
)

primary_tools = [ToAppointmentBookingAssistant, ToGetInfo, ToPrimaryBookingAssistant, CompleteOrEscalate]
primary_runnable = get_runnable(
    llm=llm,
    tools=primary_tools,
    agent_prompt=primary_agent_prompt
)


def build_graph():
    builder = StateGraph(State)

    builder.add_node("primary_assistant", Assistant(primary_runnable))

    builder.add_node(
        "enter_get_info",
        create_entry_node("Get Information Assistant", "get_info"),
    )
    builder.add_node(
        "enter_appointment_info",
        create_entry_node("Appointment Assistant", "appointment_info"),
    )

    builder.add_node("get_info", Assistant(info_runnable))
    builder.add_node("appointment_info", Assistant(booking_runnable))

    builder.add_node(
        "update_info_tools",
        create_tool_node_with_fallback(info_tools),
    )

    builder.add_node(
        "update_appointment_tools",
        create_tool_node_with_fallback(booking_tools),
    )

    builder.add_node("leave_skill", pop_dialog_state)

    builder.add_conditional_edges(START, route_to_workflow)

    builder.add_conditional_edges(
        "primary_assistant",
        route_primary_assistant,
        [
            "enter_appointment_info",
            "enter_get_info",
            END,
        ],
    )

    builder.add_edge("enter_get_info", "get_info")

    builder.add_edge("update_info_tools", "get_info")
    builder.add_conditional_edges(
        "get_info",
        RouteUpdater(info_tools, "update_info_tools").route_update_info,
        ["update_info_tools", "leave_skill", END],
    )

    builder.add_edge("leave_skill", "primary_assistant")

    builder.add_edge("enter_appointment_info", "appointment_info")

    builder.add_edge("update_appointment_tools", "appointment_info")
    builder.add_conditional_edges(
        "appointment_info",
        RouteUpdater(booking_tools, "update_appointment_tools").route_update_info,
        ["update_appointment_tools", "leave_skill", END],
    )

    # memory = MemorySaver()
    graph = builder.compile(
        checkpointer=memory,
    )

    return graph

def run_workflow(self, query: str, thread_id: int) -> Tuple[str, str]:
    logging.info(f'Received the Query - {query} & thread_id - {thread_id}')
    inputs = [
        HumanMessage(content=query)
    ]
    state = {'messages': inputs}
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 10}}
    response = build_graph().invoke(input=state, config=config)

    logging.info('Generated Answer from Graph')
    dialog_states = response['dialog_state']
    dialog_state = dialog_states[-1] if dialog_states else 'primary_assistant'
    messages = response['messages'][-1].content
    return str(messages), dialog_state