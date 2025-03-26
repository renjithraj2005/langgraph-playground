from flask import Flask
from flask_restx import Api
from .routes.search import ns as search_ns
from .routes.booking import ns as booking_ns

def init_api(app: Flask):
    """Initialize the API with all routes."""
    api = Api(
        app,
        version='1.0',
        title='Salonist API',
        description='API for Salonist application',
        doc='/docs',
        authorizations={
            'apikey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-API-Key'
            }
        }
    )
    
    # Add namespaces
    api.add_namespace(search_ns, path='/api/search')
    api.add_namespace(booking_ns, path='/api/booking')
    
    return api 