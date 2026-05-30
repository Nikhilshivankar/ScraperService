from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ClientCreateRequest:
    """DTO for creating a new client"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None
    active: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> 'ClientCreateRequest':
        """Create from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            deleted_at=data.get('deleted_at'),
            created_by=data.get('created_by'),
            updated_by=data.get('updated_by'),
            deleted_by=data.get('deleted_by'),
            active=data.get('active', True)
        )


@dataclass
class ClientResponse:
    """DTO for Client response"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None
    active: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_by': self.deleted_by,
            'active': self.active
        }

    @classmethod
    def from_model(cls, client_model) -> 'ClientResponse':
        """Create from Clients model"""
        return cls(
            id=client_model.id,
            name=client_model.name,
            created_at=client_model.created_at,
            updated_at=client_model.updated_at,
            deleted_at=client_model.deleted_at,
            created_by=client_model.created_by,
            updated_by=client_model.updated_by,
            deleted_by=client_model.deleted_by,
            active=client_model.active
        )
