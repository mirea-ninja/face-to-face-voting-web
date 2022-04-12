from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from .user import user_events_association_table, moderator_events_association_table

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    owner = relationship("User", back_populates="events")
    owner_id = Column(Integer, ForeignKey("user.id"))
    participants = relationship(
        "User", secondary=user_events_association_table, back_populates="events"
    )
    moderators = relationship(
        "User", secondary=moderator_events_association_table, back_populates="moderator_in"
    )