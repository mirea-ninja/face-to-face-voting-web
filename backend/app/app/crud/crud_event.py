from typing import List

from fastapi.encoders import jsonable_encoder
from requests import Session
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

from .base import CRUDBase


class CRUDItem(CRUDBase[Event, EventCreate, EventUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: EventCreate, owner_id: int
    ) -> Event:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Event]:
        return (
            db.query(self.model)
            .filter(Event.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


event = CRUDItem(Event)
