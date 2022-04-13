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

acess_moderator_events_association_table = Table(
    "acess_moderator_events_association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("event_id", ForeignKey("event.id"), primary_key=True),
)

voting_moderator_events_association_table = Table(
    "voting_moderator_events_association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("event_id", ForeignKey("event.id"), primary_key=True),
)


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    academic_group = Column(String, index=True, nullable=True)
    is_student = Column(Boolean(), default=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
    events_owner = relationship("Event", back_populates="owner")
    events = relationship(
        "Event",
        secondary=user_events_association_table,
        back_populates="participants",
        viewonly=True,
    )
    access_moderator_in = relationship(
        "Event",
        secondary=acess_moderator_events_association_table,
        back_populates="access_moderators",
        viewonly=True,
    )
    voting_moderator_in = relationship(
        "Event",
        secondary=acess_moderator_events_association_table,
        back_populates="voting_moderators",
        viewonly=True,
    )
