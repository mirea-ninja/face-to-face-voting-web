from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from .user import (
    acess_moderator_events_association_table,
    user_events_association_table,
    voting_moderator_events_association_table,
)

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    is_open = Column(Boolean(), default=False)
    name = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    owner = relationship("User", back_populates="events")
    owner_id = Column(Integer, ForeignKey("user.id"))
    participants = relationship(
        "User", secondary=user_events_association_table, back_populates="events"
    )
    access_moderators = relationship(
        "User",
        secondary=acess_moderator_events_association_table,
        back_populates="access_moderator_in",
    )
    voting_moderators = relationship(
        "User",
        secondary=voting_moderator_events_association_table,
        back_populates="voting_moderator_in",
    )
    access_logs = relationship("AccessLog", back_populates="event")
    created_at = Column(DateTime, server_default=func.now())
    start_at = Column(DateTime, nullable=False)
    close_at = Column(DateTime, nullable=True)
    polls = relationship("Poll", back_populates="event")
