from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Product_Info(Base):
    __tablename__ = "product_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    price: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
