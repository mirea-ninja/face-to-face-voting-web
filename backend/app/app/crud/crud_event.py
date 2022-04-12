from .base import CRUDBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

event = CRUDBase[Event, EventCreate, EventUpdate](Event)
