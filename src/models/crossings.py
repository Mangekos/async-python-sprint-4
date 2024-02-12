from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Crossings(Base):
    __tablename__ = "crossings"

    id = Column(Integer, primary_key=True)
    link_id = Column(
        ForeignKey("links.id", ondelete="CASCADE"), nullable=False
    )
    link: list = relationship("Links")
    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    user = Column(String)
