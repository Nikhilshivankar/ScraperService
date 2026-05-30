from flask import Blueprint, jsonify, request
from app.core.logger import setup_logger
from app.services.database_service import DatabaseService
from app.models.requests_dto.jobs import JobResponse
from app.models.db_dto.job import Job_Data
from app.db import get_db_session

logger = setup_logger(__name__)
api_bp = Blueprint('jobs_api', __name__)

database_service = DatabaseService()


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
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  submitted_by:
                    type: string
                  submitted_at:
                    type: string
                    format: date-time
                  status:
                    type: string
                  jobtype:
                    type: string
                  client_name:
                    type: string
                    nullable: true
                  scrape_type:
                    type: string
                    nullable: true
                  changed_by:
                    type: string
                    nullable: true
            total:
              type: integer
            page:
              type: integer
            page_size:
              type: integer
            total_pages:
              type: integer
    """
    logger.info('Received request to list jobs')
    try:
        # Get formatted data from database service
        result = database_service.get_all_jobs()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


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
              properties:
                id:
                  type: integer
                submitted_by:
                  type: string
                submitted_at:
                  type: string
                  format: date-time
                status:
                  type: string
                jobtype:
                  type: string
                client_name:
                  type: string
                  nullable: true
                scrape_type:
                  type: string
                  nullable: true
                changed_by:
                  type: string
                  nullable: true
                changed_at:
                  type: string
                  format: date-time
                  nullable: true
                scheduled_at:
                  type: string
                  format: date-time
                  nullable: true
                done_at:
                  type: string
                  format: date-time
                  nullable: true
            service:
              type: string
            version:
              type: string
    """
    logger.info('Received request for job id=%s', job_id)
    try:
        # Fetch directly from database using model
        with get_db_session() as session:
            job_model = session.query(Job_Data).filter(Job_Data.id == job_id).first()
            if not job_model:
                return jsonify({'error': 'Job not found'}), 404
            
            # Convert model to JobResponse DTO
            job_response = JobResponse.from_model(job_model)
            
            return jsonify({
                'job': job_response.to_dict(),
                'service': 'database-service',
                'version': '1.0.0'
            }), 200
    except Exception as e:
        logger.error(f"Error fetching job {job_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@api_bp.route('/scrape/<int:client_id>', methods=['POST'])
def scrape_client_products(client_id):
    """
    Create a scrape job for the given client and persist product information.
    ---
    tags:
      - Jobs
    parameters:
      - name: client_id
        in: path
        type: integer
        required: true
        description: Client ID
    requestBody:
      required: false
      content:
        application/json:
          schema:
            type: object
            properties:
              submitted_by:
                type: string
                example: system
    responses:
      200:
        description: Scrape job created and product_info updated
    """
    try:
        payload = request.get_json(silent=True) or {}
        submitted_by = payload.get('submitted_by', 'system')
        logger.info('Received scrape request for client_id=%s submitted_by=%s', client_id, submitted_by)
        result = database_service.create_scrape_job_for_client(client_id, submitted_by=submitted_by)
        logger.info('Completed scrape request for client_id=%s, status=%s', client_id, result.get('status'))
        return jsonify(result), 200
    except ValueError as e:
        logger.error(f"Invalid scrape job request for client {client_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating scrape job for client {client_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@api_bp.route('/jobs/create', methods=['POST'])
def create_job():
    """
    Create job
    ---
    tags:
      - Jobs
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              submitted_by:
                type: string
              jobtype:
                type: string
              client_name:
                type: string
              scrape_type:
                type: string
              status:
                type: string
    responses:
      201:
        description: Job created
    """

    try:
        payload = request.get_json(silent=True) or {}
        logger.info('Received create job request payload=%s', payload)
        if not payload:
            return jsonify({'error': 'Request body is required'}), 400

        job_data = {
            'submitted_by': payload.get('submitted_by', 'system'),
            'jobtype': payload.get('jobtype', 'Scraper'),
            'client_name': payload.get('client_name'),
            'scrape_type': payload.get('scrape_type'),
            'status': payload.get('status', 'New')
        }

        result = database_service.create_job(job_data)
        return jsonify({'job': result, 'service': 'database-service', 'version': '1.0.0'}), 201
    except Exception as e:
        logger.error(f"Error creating job: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


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

