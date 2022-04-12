from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


user_events_association_table = Table(
    "user_events_association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("event_id", ForeignKey("event.id"), primary_key=True),
)


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
    created_events = relationship("Event", back_populates="creator")
    events = relationship("Event", secondary=user_events_association_table, back_populates="users")
