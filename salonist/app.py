from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from salonist.config import get_settings
from salonist.api import init_api
from salonist.database import db

migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class is None:
        config_class = get_settings()
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize API
    api = init_api(app)
    
    # Register CLI commands
    from salonist.commands import seed_db, list_services, clean_db, visualize_graph, visualize_agent
    app.cli.add_command(seed_db)
    app.cli.add_command(list_services)
    app.cli.add_command(clean_db)
    app.cli.add_command(visualize_graph)
    app.cli.add_command(visualize_agent)
    
    return app 