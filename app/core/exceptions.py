class ScraperException(Exception):
    """Base exception for scraper errors"""
    pass


class RequestException(ScraperException):
    """Exception for HTTP request failures"""
    pass


class ParsingException(ScraperException):
    """Exception for HTML parsing failures"""
    pass


class ValidationException(ScraperException):
    """Exception for input validation failures"""
    pass
