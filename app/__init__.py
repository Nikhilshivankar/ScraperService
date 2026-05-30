from flask import Flask
from flasgger import Swagger
from app.core.config import get_config
from app.core.logger import setup_logger
from app.core.swagger_config import SWAGGER_CONFIG, SWAGGER_TEMPLATE
from app.api.health import api_bp as health_bp
from app.api.jobs import api_bp as jobs_bp
from app.api.clients import api_bp as clients_bp
from app.models.base import Base
import app.models.db_dto.product_info
from app.db import engine
from flask import g

logger = setup_logger(__name__)


def create_app(config_name: str = None) -> Flask:
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name:
        app.config.from_object(f'app.core.config.{config_name}')
    else:
        config = get_config()
        app.config.from_object(config)
    
    # Setup logging
    setup_logger('app', app.config.get('LOG_LEVEL', 'INFO'))
    
    # Initialize database tables
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized")
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(jobs_bp, url_prefix='/api')
    app.register_blueprint(clients_bp, url_prefix='/api')
    
    # Initialize Swagger after routes are registered
    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'ScraperService',
            'version': '1.0.0',
            'api_version': 'v1',
            'endpoints': {
                'health': 'GET /api/health',
                'jobs': {
                    'list': 'GET /api/jobs',
                    'get': 'GET /api/jobs/<job_id>'
                },
                'clients': {
                    'list': 'GET /api/clients',
                    'get': 'GET /api/clients/<id>'
                },
                'scrape': 'POST /api/scrape/<client_id>'
            }
        }
    
    logger.info("Application initialized successfully")
    return app




