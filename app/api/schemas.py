from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class ScrapeRequest:
    """Schema for scrape request"""
    urls: List[str]
    selectors: Optional[Dict[str, str]] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ScrapeRequest':
        """Create from dictionary with validation"""
        urls = data.get('urls', [])
        
        if not isinstance(urls, list):
            raise ValueError("'urls' must be a list")
        
        if not urls:
            raise ValueError("'urls' cannot be empty")
        
        if not all(isinstance(url, str) for url in urls):
            raise ValueError("All URLs must be strings")
        
        selectors = data.get('selectors')
        if selectors is not None and not isinstance(selectors, dict):
            raise ValueError("'selectors' must be a dictionary")
        
        return cls(urls=urls, selectors=selectors)
