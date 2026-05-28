from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class ScrapeResult:
    """Model for scrape result"""
    url: str
    status: str
    name: Optional[str] = None
    price: Optional[str] = None
    image: Optional[str] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class SiteSelectors:
    """Model for site-specific CSS selectors"""
    name: str
    price: str
    image: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return asdict(self)
