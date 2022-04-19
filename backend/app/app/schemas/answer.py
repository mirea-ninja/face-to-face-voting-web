import datetime

from pydantic import BaseModel

from .poll import Poll
from .user import User


class AnswerBase(BaseModel):
    poll_id: int
    answer_option_id: int


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    answer_option_id: int


class AnswerInDBBase(AnswerBase):
    id: int
    owner_id: int
    owner: User
    poll: Poll
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class Answer(AnswerInDBBase):
    pass


class AnswerInDB(AnswerInDBBase):
    pass
