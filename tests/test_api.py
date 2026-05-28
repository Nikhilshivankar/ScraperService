import pytest
from app import create_app
from app.services.scraper_service import ScraperService


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'service' in data


class TestScrapeEndpoint:
    """Test scrape endpoint"""
    
    def test_scrape_missing_body(self, client):
        response = client.post('/api/scrape')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_scrape_missing_urls(self, client):
        response = client.post('/api/scrape', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_scrape_empty_urls(self, client):
        response = client.post('/api/scrape', json={'urls': []})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_scrape_invalid_urls_type(self, client):
        response = client.post('/api/scrape', json={'urls': 'not-a-list'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_scrape_valid_request(self, client):
        response = client.post('/api/scrape', json={
            'urls': ['https://example.com']
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] == 1
        assert len(data['results']) == 1


class TestSitesEndpoint:
    """Test sites endpoint"""
    
    def test_get_supported_sites(self, client):
        response = client.get('/api/sites')
        assert response.status_code == 200
        data = response.get_json()
        assert 'supported_sites' in data
        assert 'selectors' in data
        assert isinstance(data['supported_sites'], list)


class TestScraperService:
    """Test scraper service"""
    
    def test_scraper_initialization(self):
        scraper = ScraperService()
        assert scraper is not None
        assert scraper.timeout > 0
    
    def test_get_selectors_known_site(self):
        scraper = ScraperService()
        selectors = scraper._get_selectors('https://www.amazon.com/product')
        assert selectors.name == '#productTitle'
    
    def test_get_selectors_unknown_site(self):
        scraper = ScraperService()
        selectors = scraper._get_selectors('https://unknown-site.com/product')
        assert selectors == ScraperService.DEFAULT_SELECTORS
