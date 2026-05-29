from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from app.db import get_db_session
from app.core.logger import setup_logger
from app.core.config import get_config
from datetime import datetime

# Import models at module level
from app.models.db_dto.job import Job_Data
from app.models.db_dto.clients import Clients
from app.models.db_dto.product_urls import Product_Urls

logger = setup_logger(__name__)
config = get_config()


class DatabaseService:
    """Service for database operations with SQLAlchemy best practices"""
    
    # READ Operations
    @staticmethod
    def get_all_jobs(page: int = 1, page_size: Optional[int] = None) -> Dict[str, Any]:
        """Get all jobs with pagination"""
        if page_size is None:
            page_size = config.DEFAULT_PAGE_SIZE
        page_size = min(page_size, config.MAX_PAGE_SIZE)
        
        offset = (page - 1) * page_size
        
        with get_db_session() as session:
            total = session.query(Job_Data).count()
            jobs = session.query(Job_Data).offset(offset).limit(page_size).all()
            
            return {
                'items': [
                    {
                        'id': job.id,
                        'submitted_by': job.submitted_by,
                        'submitted_at': job.submitted_at.isoformat() if job.submitted_at else None,
                        'status': job.status,
                        'jobtype': job.jobtype,
                        'client_name': job.client_name,
                        'scrape_type': job.scrape_type,
                        'changed_by': job.changed_by
                    }
                    for job in jobs
                ],
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size if total > 0 else 0
            }
    
    @staticmethod
    def get_job_by_id(job_id: int) -> Optional[Dict[str, Any]]:
        """Get job by ID"""
        with get_db_session() as session:
            job = session.query(Job_Data).filter(Job_Data.id == job_id).first()
            if job:
                return {
                    'id': job.id,
                    'submitted_by': job.submitted_by,
                    'submitted_at': job.submitted_at.isoformat() if job.submitted_at else None,
                    'status': job.status,
                    'jobtype': job.jobtype,
                    'client_name': job.client_name,
                    'scrape_type': job.scrape_type,
                    'changed_by': job.changed_by
                }
            return None
    
    @staticmethod
    def get_all_clients(page: int = 1, page_size: Optional[int] = None) -> Dict[str, Any]:
        """Get all active clients with pagination"""
        if page_size is None:
            page_size = config.DEFAULT_PAGE_SIZE
        page_size = min(page_size, config.MAX_PAGE_SIZE)
        
        offset = (page - 1) * page_size
        
        with get_db_session() as session:
            query = session.query(Clients).filter(Clients.active == True)
            total = query.count()
            clients = query.offset(offset).limit(page_size).all()
            
            return {
                'items': [
                    {
                        'id': client.id,
                        'name': client.name,
                        'created_by': client.created_by,
                        'updated_by': client.updated_by,
                        'active': client.active,
                        'created_at': client.created_at.isoformat() if client.created_at else None
                    }
                    for client in clients
                ],
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size if total > 0 else 0
            }
    
    @staticmethod
    def get_client_by_id(client_id: int) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        with get_db_session() as session:
            client = session.query(Clients).filter(
                Clients.id == client_id,
                Clients.active == True
            ).first()
            
            if client:
                return {
                    'id': client.id,
                    'name': client.name,
                    'created_by': client.created_by,
                    'updated_by': client.updated_by,
                    'active': client.active,
                    'created_at': client.created_at.isoformat() if client.created_at else None
                }
            return None
    
    @staticmethod
    def get_all_product_urls(
        client_id: Optional[int] = None,
        page: int = 1,
        page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all product URLs with pagination and eager loading of client"""
        if page_size is None:
            page_size = config.DEFAULT_PAGE_SIZE
        page_size = min(page_size, config.MAX_PAGE_SIZE)
        
        offset = (page - 1) * page_size
        
        with get_db_session() as session:
            # Use joinedload for eager loading to avoid N+1 queries
            query = session.query(Product_Urls).options(
                joinedload(Product_Urls.client)
            ).filter(Product_Urls.status == True)
            
            if client_id:
                query = query.filter(Product_Urls.client_id == client_id)
            
            total = query.count()
            urls = query.offset(offset).limit(page_size).all()
            
            return {
                'items': [
                    {
                        'id': url.id,
                        'url': url.url,
                        'source_type': url.source_type,
                        'status': url.status,
                        'client_id': url.client_id,
                        'client_name': url.client.name if url.client else None,
                        'created_at': url.created_at.isoformat() if url.created_at else None
                    }
                    for url in urls
                ],
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size if total > 0 else 0
            }
    
    @staticmethod
    def get_product_url_by_id(url_id: int) -> Optional[Dict[str, Any]]:
        """Get product URL by ID with eager loaded client"""
        with get_db_session() as session:
            url = session.query(Product_Urls).options(
                joinedload(Product_Urls.client)
            ).filter(Product_Urls.id == url_id).first()
            
            if url:
                return {
                    'id': url.id,
                    'url': url.url,
                    'source_type': url.source_type,
                    'status': url.status,
                    'client_id': url.client_id,
                    'client_name': url.client.name if url.client else None,
                    'created_at': url.created_at.isoformat() if url.created_at else None
                }
            return None
    
    # CREATE Operations
    @staticmethod
    def create_job(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job"""
        with get_db_session() as session:
            job = Job_Data(
                submitted_by=data['submitted_by'],
                status=data.get('status', 'new'),
                jobtype=data['jobtype'],
                client_name=data.get('client_name'),
                scrape_type=data.get('scrape_type')
            )
            session.add(job)
            session.flush()  # Flush to get the ID without committing
            
            result = {
                'id': job.id,
                'submitted_by': job.submitted_by,
                'status': job.status,
                'jobtype': job.jobtype,
                'client_name': job.client_name,
                'scrape_type': job.scrape_type
            }
            # Context manager handles commit
            return result
    
    @staticmethod
    def create_client(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client"""
        with get_db_session() as session:
            client = Clients(
                name=data['name'],
                created_by=data.get('created_by'),
                active=data.get('active', True)
            )
            session.add(client)
            session.flush()
            
            result = {
                'id': client.id,
                'name': client.name,
                'created_by': client.created_by,
                'active': client.active
            }
            return result
    
    @staticmethod
    def create_product_url(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product URL with foreign key validation"""
        with get_db_session() as session:
            # Validate client exists
            client = session.query(Clients).filter(
                Clients.id == data['client_id'],
                Clients.active == True
            ).first()
            
            if not client:
                raise ValueError(f"Active client with id {data['client_id']} not found")
            
            product_url = Product_Urls(
                url=data['url'],
                source_type=data.get('source_type', 'Sitemap'),
                client_id=data['client_id'],
                status=data.get('status', True)
            )
            session.add(product_url)
            session.flush()
            
            result = {
                'id': product_url.id,
                'url': product_url.url,
                'source_type': product_url.source_type,
                'client_id': product_url.client_id,
                'client_name': client.name,
                'status': product_url.status
            }
            return result
    
    @staticmethod
    def create_product_urls_bulk(urls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple product URLs in a single transaction"""
        with get_db_session() as session:
            # Validate all client_ids exist first
            client_ids = set(data['client_id'] for data in urls)
            existing_clients = session.query(Clients.id).filter(
                Clients.id.in_(client_ids),
                Clients.active == True
            ).all()
            existing_client_ids = {c.id for c in existing_clients}
            
            invalid_ids = client_ids - existing_client_ids
            if invalid_ids:
                raise ValueError(f"Active clients not found for ids: {invalid_ids}")
            
            # Create all product URLs
            product_urls = []
            for data in urls:
                product_url = Product_Urls(
                    url=data['url'],
                    source_type=data.get('source_type', 'Sitemap'),
                    client_id=data['client_id'],
                    status=data.get('status', True)
                )
                product_urls.append(product_url)
            
            session.add_all(product_urls)
            # Context manager handles commit
            
            return {
                'created': len(product_urls),
                'message': f'Successfully created {len(product_urls)} product URLs'
            }
