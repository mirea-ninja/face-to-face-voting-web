from typing import List

from pydantic import BaseModel

from .answer import Answer


class AnswerOptionBase(BaseModel):
    text: str
    poll_id: int


class AnswerOptionCreate(AnswerOptionBase):
    pass


class AnswerOptionUpdate(BaseModel):
    text: str


class AnswerOptionInDBBase(AnswerOptionBase):
    id: int
    answers: List[Answer]

    class Config:
        orm_mode = True


class AnswerOption(AnswerOptionInDBBase):
    pass


class AnswerOptionInDB(AnswerOptionInDBBase):
    pass
