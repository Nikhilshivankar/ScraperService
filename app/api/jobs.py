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


@api_bp.route('/jobs', methods=['GET'])
def get_job_list():
    """
    Get all jobs
    ---
    tags:
      - Jobs
    responses:
      200:
        description: List of all jobs
        schema:
          type: object
          properties:
            jobs:
              type: array
              items:
                type: object
            service:
              type: string
            version:
              type: string
    """
    job_list = database_service.get_all_jobs()
    return jsonify({
        'jobs': job_list,
        'service': 'database-service',
        'version': '1.0.0'
    }), 200


@api_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    Get job by ID
    ---
    tags:
      - Jobs
    parameters:
      - name: job_id
        in: path
        type: integer
        required: true
        description: Job ID
    responses:
      200:
        description: Job details
        schema:
          type: object
          properties:
            job:
              type: object
            service:
              type: string
            version:
              type: string
    """
    job = database_service.get_job_by_id(job_id)
    return jsonify({
        'job': job,
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
