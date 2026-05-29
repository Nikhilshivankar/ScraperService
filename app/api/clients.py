from flask import Blueprint, request, jsonify
from app.core.logger import setup_logger
from app.core.exceptions import ValidationException
from app.services.scraper_service import ScraperService
from app.services.database_service import DatabaseService

from app.routes.schemas import ScrapeRequest

logger = setup_logger(__name__)
api_bp = Blueprint('api', __name__)

# Initialize scraper service
database_service = DatabaseService()
scraper_service = ScraperService()


@api_bp.route('/clients', methods=['GET'])
def get_client_list():
    """
    Get all clients
    ---
    tags:
      - Clients
    responses:
      200:
        description: List of all clients
        schema:
          type: object
          properties:
            clients:
              type: array
              items:
                type: object
            service:
              type: string
            version:
              type: string
    """
    client_list = database_service.get_all_clients()
    return jsonify({
        'clients': client_list,
        'service': 'database-service',
        'version': '1.0.0'
    }), 200


@api_bp.route('/clients/<int:id>', methods=['GET'])
def get_client(id):
    """
    Get client by ID
    ---
    tags:
      - Clients
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Client ID
    responses:
      200:
        description: Client details
        schema:
          type: object
          properties:
            clients:
              type: object
            service:
              type: string
            version:
              type: string
    """
    client_list = database_service.get_client_by_id(id)
    return jsonify({
        'clients': client_list,
        'service': 'database-service',
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
