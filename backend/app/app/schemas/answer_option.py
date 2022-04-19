from pydantic import BaseModel


class AnswerOptionBase(BaseModel):
    text: str
    poll_id: int


class AnswerOptionCreate(AnswerOptionBase):
    pass


class AnswerOptionUpdate(AnswerOptionBase):
    pass


class AnswerOptionInDBBase(AnswerOptionBase):
    id: int

    class Config:
        orm_mode = True


class AnswerOption(AnswerOptionInDBBase):
    pass


class AnswerOptionInDB(AnswerOptionInDBBase):
    pass
