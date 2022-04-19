from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Poll(Base):
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="polls_created")
    answers = relationship("Answer", back_populates="poll")
    answer_options = relationship("AnswerOption", back_populates="poll")
    created_at = Column(DateTime, server_default=func.now())
    is_running = Column(Boolean(), default=False)
    stop_at = Column(DateTime, nullable=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    event = relationship("Event", back_populates="polls")
