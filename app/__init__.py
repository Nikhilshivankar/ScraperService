from flask import Flask
from app.core.config import get_config
from app.core.logger import setup_logger
from app.api.routes import api_bp

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
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'ScraperService',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'scrape': '/api/scrape',
                'sites': '/api/sites'
            }
        }
    
    logger.info("Application initialized successfully")
    return app
