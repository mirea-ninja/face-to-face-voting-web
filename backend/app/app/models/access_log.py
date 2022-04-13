from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AccessLog(Base):
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    event = relationship("Poll", back_populates="access_logs")
    given_by_id = Column(Integer, ForeignKey("user.id"))
    received_id = Column(Integer, ForeignKey("user.id"))
    received_at = Column(DateTime, server_default=func.now())
