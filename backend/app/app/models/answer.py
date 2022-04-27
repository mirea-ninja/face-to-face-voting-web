from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Answer(Base):
    id = Column(Integer, primary_key=True, index=True)
    answer_option_id = Column(Integer, ForeignKey("answeroption.id"))
    answer_option = relationship("AnswerOption", back_populates="answers")
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="answers")
    poll_id = Column(Integer, ForeignKey("poll.id"))
    poll = relationship("Poll", back_populates="answers")
    created_at = Column(DateTime, server_default=func.now())
