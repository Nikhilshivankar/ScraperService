# Quick Start Guide

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Launch Service
```bash
python run.py
```

The service will start on `http://localhost:5000`

## 3. Test Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Scrape URLs
```bash
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d "{\"urls\": [\"https://example.com\"]}"
```

### Get Supported Sites
```bash
curl http://localhost:5000/api/sites
```

## 4. View Logs

All logs are stored in `logs/scraper_service.log`

```bash
# Windows
type logs\scraper_service.log

# Linux/Mac
tail -f logs/scraper_service.log
```

## Configuration

Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

Edit `.env` to change settings like timeout, retries, log level, etc.
