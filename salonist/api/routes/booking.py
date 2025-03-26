from flask_restx import Resource, Namespace, fields
from salonist.booking import BookingWorkflow
import time

# Create namespace
ns = Namespace('booking', description='Booking operations')

# Define input/output models
booking_input = ns.model('BookingInput', {
    'query': fields.String(required=True, description='The booking query')
})

booking_response = ns.model('BookingResponse', {
    'response': fields.String(description='The AI response'),
    'metadata': fields.Nested(ns.model('Metadata', {
        'processing_time': fields.Float(description='Time taken to process the request')
    }))
})

@ns.route('')
class Booking(Resource):
    """Booking endpoint for handling booking queries."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workflow = BookingWorkflow()
    
    @ns.expect(booking_input)
    @ns.response(200, 'Success', booking_response)
    @ns.response(400, 'Bad Request')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        """Process a booking query and return the AI response."""
        try:
            data = ns.payload
            query = data.get('query')

            if not query:
                return {'error': 'Query is required'}, 400

            # Run the workflow
            response, processing_time = self.workflow.run(query)

            return {
                'response': response,
                'metadata': {
                    'processing_time': processing_time
                }
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500