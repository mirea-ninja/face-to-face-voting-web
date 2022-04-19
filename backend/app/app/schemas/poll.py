import datetime
from typing import Optional

from pydantic import BaseModel

from .user import User


# Shared properties
class PollBase(BaseModel):
    question: str
    event_id: int


class PollCreate(PollBase):
    pass


class PollRename(BaseModel):
    question: str


class PollUpdate(BaseModel):
    is_running: bool = False
    stop_at: Optional[datetime.datetime]


# Properties shared by models stored in DB
class PollInDBBase(PollBase):
    id: int
    owner: User
    created_at: datetime.datetime
    owner_id: int
    is_running: bool = False
    stop_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Poll(PollInDBBase):
    pass


# Properties properties stored in DB
class PollInDB(PollInDBBase):
    pass
