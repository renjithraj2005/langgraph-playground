import logging

from flask_restx import Resource, Namespace, fields
from salonist.agent.graph import AgentGraph

# Create namespace
ns = Namespace('multi-agent', description='Multi-agent operations')

# Define input/output models
multi_agent_input = ns.model('MultiAgentInput', {
    'query': fields.String(required=True, description='The multi-agent query')
})

multi_agent_response = ns.model('MultiAgentResponse', {
    'response': fields.String(description='The AI response'),
    'metadata': fields.Nested(ns.model('Metadata', {
        'processing_time': fields.Float(description='Time taken to process the request')
    }))
})

@ns.route('')
class MultiAgent(Resource):
    """Multi-agent endpoint for handling multi-agent queries."""
    
    def __init__(self, *args, **kwargs):
        self.agent = AgentGraph()
        super().__init__(*args, **kwargs)

    @ns.expect(multi_agent_input)
    @ns.response(200, 'Success', multi_agent_response)
    @ns.response(400, 'Bad Request')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        """Process a multi-agent query and return the AI response."""
        try:
            data = ns.payload
            query = data.get('query')

            if not query:
                return {'error': 'Query is required'}, 400

            thread_id = 1234

            # Run the workflow
            message, dialog_state = self.agent.run_workflow(query, thread_id)

            return {
                'response': message,
                'dialog_state' : dialog_state
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500