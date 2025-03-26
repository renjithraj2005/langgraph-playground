from flask_restx import Resource, Namespace
from salonist.langgraph.workflow import SearchWorkflow
from ..models.search import create_search_input_model, create_search_response_model

# Create namespace
ns = Namespace('api', description='API endpoints')

# Create models
search_input = create_search_input_model(ns)
search_response = create_search_response_model(ns)

# Create workflow instance
_search_workflow = SearchWorkflow()

@ns.route('/search')
class Search(Resource):
    @ns.doc('search_query',
        responses={
            200: 'Success',
            400: 'Validation Error',
            401: 'Unauthorized',
            429: 'Too Many Requests',
            500: 'Internal Server Error'
        },
        params={
            'query': 'The search query to process',
            'max_results': 'Maximum number of results to return (1-10)',
            'search_depth': 'Depth of search (basic/advanced)'
        }
    )
    @ns.expect(search_input)
    @ns.response(200, 'Success', search_response)
    @ns.response(400, 'Validation Error')
    @ns.response(401, 'Unauthorized')
    @ns.response(429, 'Too Many Requests')
    @ns.response(500, 'Internal Server Error')
    @ns.marshal_with(search_response)
    def post(self):
        """Search for information using the AI agent."""
        try:
            data = ns.payload
            query = data['query']
            response, processing_time = _search_workflow.run(query)

            return {
                'query': query,
                'response': response,
                'metadata': {
                    'processing_time': round(processing_time, 2),
                    'sources_used': len(_search_workflow.tavily_client.search(query, max_results=5).get("results", [])),
                    'confidence_score': 0.85
                }
            }
        except Exception as e:
            ns.abort(500, str(e))