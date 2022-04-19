from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AnswerOption(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True, nullable=False)
    poll_id = Column(Integer, ForeignKey("poll.id"))
    poll = relationship("Poll", back_populates="answer_options")
    answers = relationship("Answer", back_populates="answer_options")
