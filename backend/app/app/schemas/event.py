import datetime
from typing import List, Optional

from pydantic import BaseModel

from .poll import Poll
from .user import User


# Shared properties
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_at: datetime.datetime
    close_at: Optional[datetime.datetime]


# Properties to receive on Event creation
class EventCreate(EventBase):
    pass


# Properties to receive on Event update
class EventUpdate(EventBase):
    pass


# Properties shared by models stored in DB
class EventInDBBase(EventBase):
    id: int
    owner_id: int
    participants: List[User]
    access_moderators: List[User]
    voting_moderators: List[User]
    polls: List[Poll]

    class Config:
        orm_mode = True


# Properties to return to client
class Event(EventInDBBase):
    pass


# Properties properties stored in DB
class EventInDB(EventInDBBase):
    pass
