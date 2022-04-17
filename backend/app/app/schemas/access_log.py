import datetime

from pydantic import BaseModel


class AccessLogBase(BaseModel):
    event_id: int
    given_by_id: int
    received_id: int


class AccessLogCreate(AccessLogBase):
    pass


class AccessLogUpdate(AccessLogBase):
    pass


# Properties shared by models stored in DB
class AccessLogInDBBase(AccessLogBase):
    id: int
    received_at: datetime.datetime

    class Config:
        orm_mode = True


# Properties to return to client
class AccessLog(AccessLogInDBBase):
    pass


# Properties properties stored in DB
class AccessLogInDB(AccessLogInDBBase):
    pass
