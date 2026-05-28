from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from app.core.logger import setup_logger
from app.core.exceptions import ValidationException
from app.services.scraper_service import ScraperService
from app.api.schemas import ScrapeRequest

logger = setup_logger(__name__)
api_bp = Blueprint('api', __name__)

# Initialize scraper service
scraper_service = ScraperService()


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'scraper-service',
        'version': '1.0.0'
    }), 200


@api_bp.route('/scrape', methods=['POST'])
def scrape():
    """
    Scrape multiple URLs
    
    Request body:
    {
        "urls": ["https://example.com/product1", "https://example.com/product2"],
        "selectors": {  # Optional
            "name": "h1.title",
            "price": ".price",
            "image": "img.product"
        }
    }
    """
    try:
        # Validate request
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        # Parse and validate request
        try:
            scrape_request = ScrapeRequest.from_dict(data)
        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            return jsonify({'error': str(e)}), 400
        
        # Scrape URLs
        logger.info(f"Received scrape request for {len(scrape_request.urls)} URL(s)")
        results = scraper_service.scrape_urls(
            urls=scrape_request.urls,
            custom_selectors=scrape_request.selectors
        )
        
        # Format response
        response = {
            'success': True,
            'count': len(results),
            'results': [result.to_dict() for result in results]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in scrape endpoint: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@api_bp.route('/sites', methods=['GET'])
def get_supported_sites():
    """Get list of supported sites with their selectors"""
    sites = {
        domain: selectors.to_dict() 
        for domain, selectors in ScraperService.SITE_SELECTORS.items()
    }
    
    return jsonify({
        'supported_sites': list(sites.keys()),
        'selectors': sites,
        'default_selectors': ScraperService.DEFAULT_SELECTORS.to_dict()
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
