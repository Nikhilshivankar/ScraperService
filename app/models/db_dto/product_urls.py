from app.db import engine
from app.models.base import Base
from sqlalchemy import Boolean, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.db_dto.clients import Clients


class Product_Urls(Base):
    __tablename__ = "product_urls"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, default='Sitemap')
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relationships
    client: Mapped["Clients"] = relationship("Clients", back_populates="product_urls", lazy="joined")
    