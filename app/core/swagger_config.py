"""Swagger configuration for API documentation"""

SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "ScraperService API",
        "description": "Production-ready Flask microservice for scraping multiple e-commerce websites",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@scraperservice.com"
        }
    },
    "host": "localhost:5000",
    "basePath": "/api",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {
            "name": "Health",
            "description": "Health check endpoints"
        },
        {
            "name": "Scraping",
            "description": "Web scraping operations"
        },
        {
            "name": "Sites",
            "description": "Supported sites information"
        },
        {
            "name": "Jobs",
            "description": "Job management operations"
        },
        {
            "name": "Clients",
            "description": "Client management operations"
        }
    ]
}
