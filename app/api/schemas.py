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


@dataclass
class JobCreateRequest:
    """Schema for creating a job"""
    submitted_by: str
    jobtype: str
    client_name: Optional[str] = None
    scrape_type: Optional[str] = None
    status: str = 'new'
    
    @classmethod
    def from_dict(cls, data: dict) -> 'JobCreateRequest':
        if not data.get('submitted_by'):
            raise ValueError("'submitted_by' is required")
        if not data.get('jobtype'):
            raise ValueError("'jobtype' is required")
        return cls(
            submitted_by=data['submitted_by'],
            jobtype=data['jobtype'],
            client_name=data.get('client_name'),
            scrape_type=data.get('scrape_type'),
            status=data.get('status', 'new')
        )


@dataclass
class ClientCreateRequest:
    """Schema for creating a client"""
    name: str
    created_by: Optional[str] = None
    active: bool = True
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ClientCreateRequest':
        if not data.get('name'):
            raise ValueError("'name' is required")
        return cls(
            name=data['name'],
            created_by=data.get('created_by'),
            active=data.get('active', True)
        )


@dataclass
class ProductUrlCreateRequest:
    """Schema for creating product URL"""
    url: str
    client_id: int
    source_type: str = 'Sitemap'
    active: bool = True
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ProductUrlCreateRequest':
        if not data.get('url'):
            raise ValueError("'url' is required")
        if not data.get('client_id'):
            raise ValueError("'client_id' is required")
        return cls(
            url=data['url'],
            client_id=data['client_id'],
            source_type=data.get('source_type', 'Sitemap'),
            active=data.get('active', True)
        )
