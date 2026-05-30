from flask import Blueprint, jsonify
from app.core.logger import setup_logger
from app.services.scraper_service import ScraperService
from app.services.database_service import DatabaseService


logger = setup_logger(__name__)
api_bp = Blueprint('api', __name__)

# Initialize scraper service
# database_service = DatabaseService()
# scraper_service = ScraperService()


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            service:
              type: string
              example: scraper-service
            version:
              type: string
              example: 1.0.0
    """
    logger.info('Received health check request')
    return jsonify({
        'status': 'healthy',
        'service': 'scraper-service',
        'version': '1.0.0'
    }), 200


@api_bp.errorhandler(400)
def bad_request(e):
    """Handle bad request errors"""
    return jsonify({'error': 'Bad request', 'message': str(e)}), 400


@api_bp.errorhandler(404)
def not_found(e):
    """Handle not found errors"""
    return jsonify({'error': 'Resource not found'}), 404


@api_bp.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {e}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500
