from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class JobCreateRequest:
    """DTO for creating a new job"""
    submitted_by: str
    jobtype: str
    status: Optional[str] = 'New'
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    scrape_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'JobCreateRequest':
        """Create from dictionary"""
        return cls(
            submitted_by=data.get('submitted_by'),
            jobtype=data.get('jobtype'),
            status=data.get('status', 'New'),
            client_id=data.get('client_id'),
            client_name=data.get('client_name'),
            scrape_type=data.get('scrape_type')
        )


@dataclass
class JobResponse:
    """DTO for job response"""
    id: int
    submitted_by: str
    submitted_at: datetime
    status: str
    jobtype: str
    client_name: Optional[str] = None
    scrape_type: Optional[str] = None
    changed_by: Optional[str] = None
    changed_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    done_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'submitted_by': self.submitted_by,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'status': self.status,
            'jobtype': self.jobtype,
            'client_name': self.client_name,
            'scrape_type': self.scrape_type,
            'changed_by': self.changed_by,
            'changed_at': self.changed_at.isoformat() if self.changed_at else None,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'done_at': self.done_at.isoformat() if self.done_at else None
        }

    @classmethod
    def from_model(cls, job_model) -> 'JobResponse':
        """Create from Job_Data model"""
        return cls(
            id=job_model.id,
            submitted_by=job_model.submitted_by,
            submitted_at=job_model.submitted_at,
            status=job_model.status,
            jobtype=job_model.jobtype,
            client_name=job_model.client_name,
            scrape_type=job_model.scrape_type,
            changed_by=job_model.changed_by,
            changed_at=job_model.changed_at,
            scheduled_at=job_model.scheduled_at,
            done_at=job_model.done_at
        )
