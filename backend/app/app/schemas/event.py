from typing import Optional

from pydantic import BaseModel


# Shared properties
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None


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

    class Config:
        orm_mode = True


# Properties to return to client
class Event(EventInDBBase):
    pass


# Properties properties stored in DB
class EventInDB(EventInDBBase):
    pass
