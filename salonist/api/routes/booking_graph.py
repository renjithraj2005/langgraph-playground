from flask import request
from flask_restx import Namespace, Resource, fields
from typing import Dict
from langchain_core.messages import HumanMessage

from ...booking.agents import create_graph, State
from ..models.booking_graph import ChatMessage, ChatResponse

# Create namespace
ns = Namespace('booking-graph', description='AI-powered booking operations using LangGraph')

# Define API models for swagger
chat_message = ns.model('ChatMessage', {
    'content': fields.String(required=True, description='The user message content')
})

chat_response = ns.model('ChatResponse', {
    'message': fields.String(description='The agent response message'),
    'current_agent': fields.String(description='The current active agent handling the request'),
    'booking_state': fields.Raw(description='Current state of the booking process')
})

error_response = ns.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

success_response = ns.model('SuccessResponse', {
    'status': fields.String(description='Operation status'),
    'message': fields.String(description='Status message')
})

# Create the workflow graph
workflow = create_graph()

# Store conversation states
conversations: Dict[str, State] = {}

@ns.route('/chat/<string:conversation_id>')
@ns.param('conversation_id', 'Unique identifier for the conversation')
class ChatResource(Resource):
    @ns.expect(chat_message)
    @ns.response(200, 'Success', chat_response)
    @ns.response(400, 'Validation Error', error_response)
    @ns.response(500, 'Internal Server Error', error_response)
    def post(self, conversation_id: str):
        """Send a message to the booking system."""
        # Validate request
        data = request.get_json()
        if not data or "content" not in data:
            return {"error": "Invalid request. Missing content field"}, 400
        
        message = ChatMessage(content=data["content"])
        
        # Initialize or get existing state
        if conversation_id not in conversations:
            conversations[conversation_id] = State(
                messages=[],
                current_agent="supervisor",
                selected_service=None,
                selected_package=None,
                selected_date=None,
                selected_time=None
            )
        
        state = conversations[conversation_id]
        
        # Add user message to state
        state["messages"].append(HumanMessage(content=message.content))
        
        try:
            # Run the workflow with the initial state
            result = workflow.invoke(state)
            
            # Update conversation state
            conversations[conversation_id] = result
            
            # Extract the last message from the result
            if result["messages"] and len(result["messages"]) > 0:
                last_message = result["messages"][-1].content
            else:
                last_message = "No response generated"
            
            # Create response
            response = ChatResponse(
                message=last_message,
                current_agent=result.get("current_agent", "unknown"),
                booking_state={
                    "selected_service": result.get("selected_service"),
                    "selected_package": result.get("selected_package"),
                    "selected_date": result.get("selected_date"),
                    "selected_time": result.get("selected_time")
                }
            )
            
            return response.to_dict()
            
        except Exception as e:
            return {"error": f"Error processing message: {str(e)}"}, 500

    @ns.response(200, 'Success', success_response)
    def delete(self, conversation_id: str):
        """End a conversation and clean up its state."""
        if conversation_id in conversations:
            del conversations[conversation_id]
        return {"status": "success", "message": "Conversation ended"} 