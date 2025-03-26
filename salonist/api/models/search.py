from flask_restx import fields

def create_search_input_model(api):
    """Create the search input model."""
    return api.model('SearchInput', {
        'query': fields.String(required=True, description='The search query to process'),
        'max_results': fields.Integer(description='Maximum number of results to return (1-10)', default=5),
        'search_depth': fields.String(description='Depth of search (basic/advanced)', default='advanced')
    })

def create_search_response_model(api):
    """Create the search response model."""
    return api.model('SearchResponse', {
        'query': fields.String(description='The original search query'),
        'response': fields.String(description='AI-generated response'),
        'metadata': fields.Nested(api.model('SearchMetadata', {
            'processing_time': fields.Float(description='Processing time in seconds'),
            'sources_used': fields.Integer(description='Number of sources used'),
            'confidence_score': fields.Float(description='Confidence score of the response')
        }))
    }) 