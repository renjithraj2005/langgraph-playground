from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from typing import Literal

from .supervisor import llm, supervisor_node
from .tool import tavily_tool, python_repl_tool

from .state import State

class AgentGraph:
    def __init__(self):
        # Initialize research agent
        self.research_agent = create_react_agent(
            llm, tools=[tavily_tool], prompt="You are a researcher. DO NOT do any math."
        )

        # Initialize code agent
        self.code_agent = create_react_agent(llm, tools=[python_repl_tool])

        # Build the graph
        self.graph = self._build_graph()

    def _research_node(self, state: State) -> Command[Literal["supervisor"]]:
        result = self.research_agent.invoke(state)
        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name="researcher")
                ]
            },
            goto="supervisor",
        )

    def _code_node(self, state: State) -> Command[Literal["supervisor"]]:
        result = self.code_agent.invoke(state)
        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name="coder")
                ]
            },
            goto="supervisor",
        )

    def _build_graph(self):
        builder = StateGraph(State)
        builder.add_edge(START, "supervisor")
        builder.add_node("supervisor", supervisor_node)
        builder.add_node("researcher", self._research_node)
        builder.add_node("coder", self._code_node)
        return builder.compile()

    def run(self, query: str) -> str:
        """Run the booking workflow with a given query.

        Args:
            query: The user's query to process

        Returns:
            Response string
        """
        messages = {"messages": [("user", query)]}

        for s in self.graph.stream(messages, subgraphs=True):
            print(s)
            print("----")

        return str("Ok")