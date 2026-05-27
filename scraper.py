import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Domain-specific CSS selectors: (name, price, image)
SITE_SELECTORS = {
    "fashioneyewear.com": {
        "name":  ".h2.product-single__title",
        "price": "span.product__price.on-sale",
        "image": "figure.mz-figure.mz-hover-zoom.mz-ready",
    },
    "amazon.com": {
        "name":  "#productTitle",
        "price": ".a-price .a-offscreen",
        "image": "#landingImage",
    },
    "ebay.com": {
        "name":  "h1.x-item-title__mainTitle span",
        "price": ".x-price-primary span[itemprop='price']",
        "image": "div.ux-image-carousel-item img",
    },
    "walmart.com": {
        "name":  "h1[itemprop='name']",
        "price": "[itemprop='price']",
        "image": "img.hover-zoom-hero-image",
    },
}

DEFAULT_SELECTORS = {
    "name":  "h1",
    "price": "[class*='price']",
    "image": "img",
}


def _get_selectors(url: str) -> dict:
    host = urlparse(url).hostname or ""
    for domain, selectors in SITE_SELECTORS.items():
        if domain in host:
            return selectors
    return DEFAULT_SELECTORS


def _extract(soup: BeautifulSoup, selector: str, attr: str | None = None) -> str | None:
    el = soup.select_one(selector)
    if not el:
        return None
    if attr:
        return el.get(attr)
    return el.get_text(strip=True) or None


def scrape_page(url: str, custom_selectors: dict | None = None, timeout: int = 20) -> dict:
    selectors = custom_selectors or _get_selectors(url)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        return {
            "url": url,
            "status": "ok",
            "name":  _extract(soup, selectors.get("name", "h1")),
            "price": _extract(soup, selectors.get("price", "[class*='price']")),
            "image": _extract(soup, selectors.get("image", "img"), attr="src"),
        }
    except requests.RequestException as exc:
        return {"url": url, "status": "error", "error": str(exc)}


def scrape_pages(urls: list[str], custom_selectors: dict | None = None) -> list[dict]:
    return [scrape_page(url, custom_selectors) for url in urls]
