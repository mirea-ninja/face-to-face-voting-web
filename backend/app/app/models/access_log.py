from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AccessLog(Base):
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    given_by_id = Column(Integer, ForeignKey("user.id"))
    received_id = Column(Integer, ForeignKey("user.id"))
    event = relationship("Event")
    given_by = relationship("User", foreign_keys=[given_by_id])
    received = relationship("User", foreign_keys=[received_id])
    received_at = Column(DateTime, server_default=func.now())
