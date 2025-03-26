from flask_restx import fields

def get_api_description():
    """Get the API description for Swagger documentation."""
    return '''
    A powerful search API powered by LangGraph and Claude AI.
    
    This API provides intelligent search capabilities using:
    * LangGraph for workflow management
    * Claude AI for natural language understanding
    * Tavily for web search
    
    ## Features
    * Semantic search across the web
    * AI-powered response generation
    * Context-aware answers
    * Real-time information retrieval
    
    ## Rate Limits
    * 100 requests per minute per API key
    * Rate limit headers are included in responses
    
    ## Authentication
    * API key required in header: `X-API-Key`
    * Contact support to obtain an API key
    '''

def get_namespace_description():
    """Get the namespace description for Swagger documentation."""
    return '''
    API operations for the search service.
    
    All endpoints in this namespace require authentication.
    Include your API key in the X-API-Key header.
    '''

def create_search_input_model(api):
    """Create the search input model for Swagger documentation."""
    return api.model('SearchInput', {
        'query': fields.String(
            required=True,
            description='The search query to process',
            example='What is LangGraph and how does it work?',
            min_length=3,
            max_length=500
        ),
        'max_results': fields.Integer(
            required=False,
            description='Maximum number of search results to include',
            default=5,
            min=1,
            max=10
        ),
        'search_depth': fields.String(
            required=False,
            description='Depth of search to perform',
            enum=['basic', 'advanced'],
            default='advanced'
        )
    })

def create_search_response_model(api):
    """Create the search response model for Swagger documentation."""
    return api.model('SearchResponse', {
        'query': fields.String(
            description='The original query that was processed',
            example='What is LangGraph and how does it work?'
        ),
        'response': fields.String(
            description='The AI-generated response based on search results',
            example='LangGraph is a framework for building stateful multi-agent applications...'
        ),
        'metadata': fields.Nested(api.model('SearchMetadata', {
            'processing_time': fields.Float(
                description='Time taken to process the query in seconds',
                example=2.5
            ),
            'sources_used': fields.Integer(
                description='Number of sources used to generate the response',
                example=5
            ),
            'confidence_score': fields.Float(
                description='Confidence score of the response (0-1)',
                example=0.85
            )
        }))
    }) 