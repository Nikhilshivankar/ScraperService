import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.core.logger import setup_logger
from app.core.config import get_config
from app.core.exceptions import RequestException, ParsingException
from app.models.scrape_models import ScrapeResult, SiteSelectors

logger = setup_logger(__name__)
config = get_config()


class ScraperService:
    """Service for scraping e-commerce websites"""
    
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    SITE_SELECTORS: Dict[str, SiteSelectors] = {
        "amazon.com": SiteSelectors(
            name="#productTitle",
            price=".a-price .a-offscreen",
            image="#landingImage"
        ),
        "ebay.com": SiteSelectors(
            name="h1.x-item-title__mainTitle span",
            price=".x-price-primary span[itemprop='price']",
            image="div.ux-image-carousel-item img"
        ),
        "walmart.com": SiteSelectors(
            name="h1[itemprop='name']",
            price="[itemprop='price']",
            image="img.hover-zoom-hero-image"
        ),
        "fashioneyewear.com": SiteSelectors(
            name=".h2.product-single__title",
            price="span.product__price.on-sale",
            image="figure.mz-figure img"
        ),
    }
    
    DEFAULT_SELECTORS = SiteSelectors(
        name="h1",
        price="[class*='price']",
        image="img"
    )
    
    def __init__(self, timeout: int = None, max_workers: int = 5):
        self.timeout = timeout or config.REQUEST_TIMEOUT
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def _get_selectors(self, url: str) -> SiteSelectors:
        """Get site-specific selectors based on URL"""
        hostname = urlparse(url).hostname or ""
        for domain, selectors in self.SITE_SELECTORS.items():
            if domain in hostname:
                logger.debug(f"Using selectors for {domain}")
                return selectors
        logger.debug("Using default selectors")
        return self.DEFAULT_SELECTORS
    
    def _extract_text(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text content from HTML element"""
        try:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                return text if text else None
        except Exception as e:
            logger.warning(f"Failed to extract text with selector '{selector}': {e}")
        return None
    
    def _extract_attribute(self, soup: BeautifulSoup, selector: str, attr: str) -> Optional[str]:
        """Extract attribute value from HTML element"""
        try:
            element = soup.select_one(selector)
            if element:
                value = element.get(attr)
                return value if value else None
        except Exception as e:
            logger.warning(f"Failed to extract attribute '{attr}' with selector '{selector}': {e}")
        return None
    
    def scrape_url(self, url: str, custom_selectors: Optional[Dict[str, str]] = None) -> ScrapeResult:
        """Scrape a single URL"""
        logger.info(f"Scraping: {url}")
        
        try:
            # Get selectors
            if custom_selectors:
                selectors = SiteSelectors(**custom_selectors)
            else:
                selectors = self._get_selectors(url)
            
            # Make request with retry logic
            response = None
            for attempt in range(config.MAX_RETRIES + 1):
                try:
                    response = self.session.get(url, timeout=self.timeout)
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if attempt == config.MAX_RETRIES:
                        raise RequestException(f"Failed after {config.MAX_RETRIES} retries: {str(e)}")
                    logger.warning(f"Retry {attempt + 1}/{config.MAX_RETRIES} for {url}")
                    time.sleep(config.RATE_LIMIT_DELAY)
            
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract data
            result = ScrapeResult(
                url=url,
                status="success",
                name=self._extract_text(soup, selectors.name),
                price=self._extract_text(soup, selectors.price),
                image=self._extract_attribute(soup, selectors.image, "src")
            )
            
            logger.info(f"Successfully scraped: {url}")
            return result
            
        except RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return ScrapeResult(url=url, status="error", error=str(e))
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return ScrapeResult(url=url, status="error", error=f"Unexpected error: {str(e)}")
    
    def scrape_urls(self, urls: List[str], custom_selectors: Optional[Dict[str, str]] = None) -> List[ScrapeResult]:
        """Scrape multiple URLs concurrently"""
        logger.info(f"Starting batch scrape of {len(urls)} URL(s)")
        
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.scrape_url, url, custom_selectors): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    url = future_to_url[future]
                    logger.error(f"Failed to process {url}: {e}")
                    results.append(ScrapeResult(url=url, status="error", error=str(e)))
        
        logger.info(f"Batch scrape completed: {len(results)} result(s)")
        return results
    
    def close(self):
        """Close the session"""
        self.session.close()
