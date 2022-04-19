import datetime

from pydantic import BaseModel

from .poll import Poll
from .user import User


class AnswerBase(BaseModel):
    text: str
    owner_id: int
    poll_id: int


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    pass


class AnswerInDBBase(AnswerBase):
    id: int
    owner: User
    poll: Poll
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class Answer(AnswerInDBBase):
    pass


class AnswerInDB(AnswerInDBBase):
    pass
