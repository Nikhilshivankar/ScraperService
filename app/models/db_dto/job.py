from app.db import engine
from app.models.base import Base
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.db_dto.clients import Clients


class Job_Data(Base):
    __tablename__ = "job_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    submitted_by: Mapped[str] = mapped_column(String(100), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='New')
    jobtype: Mapped[str] = mapped_column(String(20), nullable=False, default="Scraper")
    client_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    scrape_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    changed_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    changed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    done_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

