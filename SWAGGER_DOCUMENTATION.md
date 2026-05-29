# Swagger API Documentation

## Overview

The ScraperService now includes interactive Swagger/OpenAPI documentation for easy API exploration and testing.

## Accessing Swagger UI

Once the service is running, access the Swagger UI at:

```
http://localhost:5000/api/docs
```

## Features

- **Interactive API Testing**: Test all endpoints directly from the browser
- **Request/Response Examples**: See example payloads and responses
- **Schema Validation**: View request and response schemas
- **Authentication Support**: Test authenticated endpoints (if configured)

## Installation

The Swagger documentation is automatically enabled. Just install dependencies:

```bash
pip install -r requirements.txt
```

## API Endpoints Documentation

### Health Check
- **GET** `/api/v1/health` - Check service health status

### Scraping Operations
- **POST** `/api/v1/scrape/<client_id>` - Scrape multiple URLs with optional custom selectors

### Sites Information
- **GET** `/api/v1/sites` - Get list of supported sites and their CSS selectors

### Jobs Management
- **GET** `/api/v1/jobs` - Get all jobs
- **GET** `/api/v1/jobs/<job_id>` - Get specific job by ID

### Clients Management
- **GET** `/api/v1/clients` - Get all clients
- **GET** `/api/v1/clients/<id>` - Get specific client by ID

## Using Swagger UI

1. **Navigate to endpoint**: Click on any endpoint to expand it
2. **Try it out**: Click the "Try it out" button
3. **Fill parameters**: Enter required parameters and request body
4. **Execute**: Click "Execute" to send the request
5. **View response**: See the response code, body, and headers

## Example: Testing Scrape Endpoint

1. Go to `http://localhost:5000/api/docs`
2. Find the **POST** `/api/v1/scrape/{client_id}` endpoint
3. Click "Try it out"
4. Enter a client_id (e.g., `1`)
5. Enter request body:
```json
{
  "urls": [
    "https://www.amazon.com/dp/B09XYZ"
  ],
  "selectors": {
    "name": "h1.product-title",
    "price": "span.price-value",
    "image": "img.product-image"
  }
}
```
6. Click "Execute"
7. View the response

## Configuration

Swagger configuration is located in `app/core/swagger_config.py`:

- **Title**: ScraperService API
- **Version**: 1.0.0
- **Base Path**: /api
- **Schemes**: http, https

## Customization

To modify Swagger settings, edit `app/core/swagger_config.py`:

```python
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Your API Title",
        "description": "Your API Description",
        "version": "1.0.0"
    },
    # ... other settings
}
```

## API Specification

The OpenAPI specification is available at:

```
http://localhost:5000/apispec.json
```

This JSON file can be imported into tools like Postman, Insomnia, or used for code generation.

## Tags

Endpoints are organized by tags:
- **Health**: Health check endpoints
- **Scraping**: Web scraping operations
- **Sites**: Supported sites information
- **Jobs**: Job management operations
- **Clients**: Client management operations

## Production Deployment

For production, update the `host` in `swagger_config.py`:

```python
SWAGGER_TEMPLATE = {
    "host": "api.yourdomain.com",
    "schemes": ["https"],
    # ...
}
```

## Troubleshooting

**Swagger UI not loading?**
- Ensure flasgger is installed: `pip install flasgger`
- Check that the service is running
- Verify the URL: `http://localhost:5000/api/docs`

**Endpoints not showing?**
- Ensure all routes have proper docstrings with YAML specifications
- Check that blueprints are registered correctly

## Additional Resources

- [Flasgger Documentation](https://github.com/flasgger/flasgger)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
