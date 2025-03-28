from typing import Dict, Union, Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from tavily import TavilyClient
from pydantic.v1 import SecretStr
import time

from ..config import settings

class WorkflowState(TypedDict):
    messages: list[Union[HumanMessage, AIMessage]]
    current_step: str
    context: Dict[str, Any]
    search_results: list[Dict[str, Any]]

class SearchWorkflow:
    """A class to manage the search agent workflow.
    
    This class encapsulates the workflow logic for the search agent,
    including the search and analysis steps.
    """
    
    def __init__(self):
        """Initialize the workflow with required clients."""
        self.llm = ChatAnthropic(
            model_name="claude-3-5-sonnet-20240620",
        )
        self.tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.graph = self._create_graph()
    
    def _search(self, state: WorkflowState) -> WorkflowState:
        """Search for information using Tavily.
        
        Args:
            state: Current state of the workflow
            
        Returns:
            Updated state with search results
        """
        # Set a breakpoint here to inspect the state
        last_message = str(state["messages"][-1].content)
        
        search_result = self.tavily_client.search(
            query=last_message,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            max_results=5
        )
        
        state["search_results"] = search_result.get("results", [])
        state["current_step"] = "analyze"
        
        return state
    
    def _analyze(self, state: WorkflowState) -> WorkflowState:
        """Analyze search results and generate a response.
        
        Args:
            state: Current state of the workflow
            
        Returns:
            Updated state with AI response
        """
        context = "\n\n".join([
            f"Title: {result['title']}\nContent: {result['content']}"
            for result in state["search_results"]
        ])
        
        system_message = f"""You are a helpful AI assistant. Use the following search results to answer the user's question:

{context}

Provide a clear, concise answer based on the search results. If the search results don't contain enough information, say so."""

        response = self.llm.invoke([
            HumanMessage(content=system_message),
            state["messages"][-1]
        ])
        
        state["messages"].append(AIMessage(content=response.content))
        state["current_step"] = "end"
        
        return state
    
    def _should_continue(self, state: WorkflowState) -> Union[str, bool]:
        """Determine if we should continue the workflow.
        
        Args:
            state: Current state of the workflow
            
        Returns:
            Whether to continue or end the workflow
        """
        return state["current_step"] != "end"
    
    def _create_graph(self) -> Any:
        """Create and configure the workflow graph.
        
        Returns:
            Configured and compiled workflow graph
        """
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("search", self._search)
        workflow.add_node("analyze", self._analyze)
        
        # Add edges
        workflow.add_edge("search", "analyze")
        workflow.add_edge("analyze", END)
        
        # Set entry point
        workflow.set_entry_point("search")
        
        return workflow.compile()
    
    def run(self, query: str) -> tuple[str, float]:
        """Run the search workflow with a given query.
        
        Args:
            query: The search query to process
            
        Returns:
            Tuple of (response, processing_time)
        """
        start_time = time.time()
        
        # Create initial state as a dictionary
        initial_state: WorkflowState = {
            "messages": [HumanMessage(content=query)],
            "current_step": "search",
            "context": {},
            "search_results": []
        }
        
        # Run the workflow
        result = self.graph.invoke(initial_state)
        
        # Ensure we get a string response
        last_message = result["messages"][-1]
        if not isinstance(last_message, AIMessage):
            raise ValueError("Expected AI message as final response")
            
        processing_time = time.time() - start_time
        return str(last_message.content), processing_time 