# ScraperService

A production-ready Flask microservice for scraping multiple e-commerce websites with concurrent processing, error handling, and extensible architecture.

## Features

- ✅ **Concurrent Scraping**: Multi-threaded URL processing for improved performance
- ✅ **Site-Specific Selectors**: Pre-configured selectors for popular e-commerce sites
- ✅ **Custom Selectors**: Override selectors for any website
- ✅ **Retry Logic**: Automatic retry with exponential backoff
- ✅ **Rate Limiting**: Built-in delays to respect server resources
- ✅ **Error Handling**: Comprehensive exception handling and logging
- ✅ **Type Safety**: Dataclass models for request/response validation
- ✅ **Configuration Management**: Environment-based configuration
- ✅ **RESTful API**: Clean API design with proper HTTP status codes
- ✅ **Unit Tests**: Comprehensive test coverage

## Project Structure

```
ScraperService/
├── app/
│   ├── __init__.py              # Application factory
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py            # API endpoints
│   │   └── schemas.py           # Request/response schemas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── logger.py            # Logging setup
│   │   └── exceptions.py        # Custom exceptions
│   ├── models/
│   │   ├── __init__.py
│   │   └── scrape_models.py     # Data models
│   └── services/
│       ├── __init__.py
│       └── scraper_service.py   # Core scraping logic
├── tests/
│   ├── __init__.py
│   └── test_api.py              # Unit tests
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # Documentation
```

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ScraperService
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Service

**Development mode:**
```bash
python run.py
```

**Production mode:**
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

Server runs on `http://localhost:5000`

### API Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "scraper-service",
  "version": "1.0.0"
}
```

#### 2. Scrape URLs
```http
POST /api/scrape
Content-Type: application/json
```

**Request Body:**
```json
{
  "urls": [
    "https://www.amazon.com/dp/B09XYZ",
    "https://www.ebay.com/itm/123456"
  ]
}
```

**With Custom Selectors:**
```json
{
  "urls": ["https://example.com/product"],
  "selectors": {
    "name": "h1.product-title",
    "price": "span.price-value",
    "image": "img.product-image"
  }
}
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "results": [
    {
      "url": "https://www.amazon.com/dp/B09XYZ",
      "status": "success",
      "name": "Product Name",
      "price": "$29.99",
      "image": "https://example.com/image.jpg"
    },
    {
      "url": "https://www.ebay.com/itm/123456",
      "status": "error",
      "error": "Request timeout"
    }
  ]
}
```

#### 3. Get Supported Sites
```http
GET /api/sites
```

**Response:**
```json
{
  "supported_sites": ["amazon.com", "ebay.com", "walmart.com", "fashioneyewear.com"],
  "selectors": {
    "amazon.com": {
      "name": "#productTitle",
      "price": ".a-price .a-offscreen",
      "image": "#landingImage"
    }
  },
  "default_selectors": {
    "name": "h1",
    "price": "[class*='price']",
    "image": "img"
  }
}
```

## Configuration

Environment variables (`.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | `development` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key-change-in-production` |
| `PORT` | Server port | `5000` |
| `REQUEST_TIMEOUT` | HTTP request timeout (seconds) | `15` |
| `MAX_RETRIES` | Maximum retry attempts | `2` |
| `RATE_LIMIT_DELAY` | Delay between requests (seconds) | `0.5` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |

## Logging

The service logs to both console and file:
- **Console**: Real-time logs displayed in terminal
- **File**: `logs/scraper_service.log` (rotates at 10MB, keeps 5 backups)

Log format:
```
2026-05-28 11:26:27 [INFO] app.services.scraper_service - Scraping: https://example.com
```

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Adding New Sites

To add support for a new e-commerce site:

1. Open `app/services/scraper_service.py`
2. Add selectors to `SITE_SELECTORS`:

```python
SITE_SELECTORS = {
    "newsite.com": SiteSelectors(
        name="h1.product-name",
        price="span.product-price",
        image="img.product-image"
    ),
    # ... existing sites
}
```

## Best Practices Implemented

### Architecture
- **Application Factory Pattern**: Flexible app initialization
- **Blueprint Organization**: Modular route management
- **Service Layer**: Business logic separation
- **Repository Pattern**: Data access abstraction

### Code Quality
- **Type Hints**: Full type annotation coverage
- **Dataclasses**: Immutable data models
- **Exception Handling**: Custom exception hierarchy
- **Logging**: Structured logging throughout

### Configuration
- **Environment-Based Config**: Separate dev/prod settings
- **12-Factor App**: Environment variable configuration
- **Secret Management**: Secure credential handling

### Performance
- **Concurrent Processing**: ThreadPoolExecutor for parallel scraping
- **Connection Pooling**: Reusable HTTP sessions
- **Rate Limiting**: Respectful request throttling

### Security
- **Input Validation**: Schema-based request validation
- **Error Sanitization**: No sensitive data in responses
- **HTTPS Support**: Secure communication

### Testing
- **Unit Tests**: Comprehensive test coverage
- **Fixtures**: Reusable test components
- **Mocking**: Isolated component testing

## Limitations & Considerations

- **Anti-Scraping Measures**: Some sites actively block scrapers. Consider:
  - Rotating user agents
  - Using proxy rotation
  - Implementing headless browsers (Selenium/Playwright)
  
- **Legal Compliance**: Ensure scraping complies with:
  - Website Terms of Service
  - robots.txt directives
  - Local data protection laws (GDPR, CCPA)

- **Rate Limiting**: Respect server resources to avoid IP bans

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Using Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

### Environment Variables
Set production environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=<strong-random-key>
export REQUEST_TIMEOUT=20
```

## License

MIT License

## Documentation

- **[ARCHITECTURE_FIXES.md](ARCHITECTURE_FIXES.md)** - Complete list of architecture improvements and fixes
- **[SQLALCHEMY_BEST_PRACTICES.md](SQLALCHEMY_BEST_PRACTICES.md)** - SQLAlchemy optimization and best practices guide

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
