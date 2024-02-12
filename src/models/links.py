from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .base import Base


class Links(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    full_link = Column(String(100))
    creator = Column(String(30))
    remove = Column(Boolean, default=False)

    crossings: list = relationship("Crossings")

    __mapping_args__: dict = {
        "order_by": created_at.desc(),
        "eager_defaults": True,
    }
