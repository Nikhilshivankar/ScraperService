# ScraperService - Quick Reference

## 🚀 Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Run the server
python run.py

# Server runs on: http://localhost:5000
```

---

## 📡 API Endpoints (v1)

**Base URL:** `http://localhost:5000/api/v1`

### Health Check
```bash
GET /health
```

### Jobs
```bash
GET  /jobs?page=1&page_size=50          # List jobs
POST /jobs                               # Create job
GET  /jobs/{id}                          # Get job by ID
```

### Clients
```bash
GET  /clients?page=1&page_size=50       # List clients
POST /clients                            # Create client
GET  /clients/{id}                       # Get client by ID
```

### Product URLs
```bash
GET  /product-urls?page=1&page_size=50&client_id=2  # List URLs
POST /product-urls                                   # Create URL
POST /product-urls/bulk                              # Bulk create
GET  /product-urls/{id}                              # Get URL by ID
```

### Scraping
```bash
POST /scrape                             # Scrape URLs
GET  /sites                              # Get supported sites
```

---

## 📝 Example Requests

### Create a Client
```bash
curl -X POST http://localhost:5000/api/v1/clients \
  -H "Content-Type: application/json" \
  -d '{"name": "MyClient", "created_by": "admin"}'
```

### Create a Job
```bash
curl -X POST http://localhost:5000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "submitted_by": "admin",
    "jobtype": "scrape",
    "client_name": "MyClient",
    "scrape_type": "product"
  }'
```

### Bulk Insert URLs
```bash
curl -X POST http://localhost:5000/api/v1/product-urls/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      {"url": "https://example.com/1", "client_id": 2},
      {"url": "https://example.com/2", "client_id": 2}
    ]
  }'
```

### Scrape URLs
```bash
curl -X POST http://localhost:5000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://www.fashioneyewear.com/products/ray-ban-rb714"]
  }'
```

---

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Test SQLAlchemy implementation
python test_sqlalchemy.py

# Test specific endpoint
curl http://localhost:5000/api/v1/health
```

---

## 📚 Documentation

| File | Description |
|------|-------------|
| [README.md](README.md) | Complete project documentation |
| [ARCHITECTURE_FIXES.md](ARCHITECTURE_FIXES.md) | Architecture improvements |
| [SQLALCHEMY_BEST_PRACTICES.md](SQLALCHEMY_BEST_PRACTICES.md) | SQLAlchemy guide |
| [CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md) | Cleanup actions performed |

---

## 🗂️ Project Structure

```
app/
├── api/          # API routes and schemas
├── core/         # Configuration, logging, exceptions
├── models/       # SQLAlchemy models
├── services/     # Business logic
└── db.py         # Database configuration

tests/            # Unit tests
logs/             # Application logs
```

---

## ⚙️ Configuration

Edit `.env` file:

```bash
# Database
DATABASE_URL=sqlite:///./scraper_service.db

# Scraper
REQUEST_TIMEOUT=15
MAX_RETRIES=2
RATE_LIMIT_DELAY=0.5

# Pagination
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=100

# Logging
LOG_LEVEL=INFO
```

---

## 🔑 Key Features

- ✅ RESTful API with versioning (`/api/v1`)
- ✅ Pagination on all list endpoints
- ✅ SQLAlchemy ORM with relationships
- ✅ Context managers for safe database operations
- ✅ Eager loading to prevent N+1 queries
- ✅ Bulk operations for performance
- ✅ Comprehensive error handling
- ✅ Request validation with schemas
- ✅ Logging with rotation
- ✅ Environment-based configuration

---

## 🐛 Troubleshooting

**Server won't start:**
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process if needed
taskkill /F /PID <process_id>
```

**Database errors:**
```bash
# Delete and recreate database
del scraper_service.db
python run.py  # Auto-creates tables
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📞 Support

- Check logs: `logs/scraper_service.log`
- Review documentation in project root
- Run tests to verify setup: `pytest tests/`

---

**Version:** 1.0.0  
**API Version:** v1  
**Last Updated:** 2026-05-28
