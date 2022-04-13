from typing import List

from fastapi.encoders import jsonable_encoder
from requests import Session
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate
from app.utils import ModeratorType

from .base import CRUDBase


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
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

    def add_participant_to_event(
        self, db: Session, *, event_id: int, user: User
    ) -> Event:
        db_obj = db.query(self.model).filter(self.model.id == event_id).first()
        db_obj.participants.append(user)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_moderator_to_event(
        self, db: Session, *, event_id: int, user: User, moderator_type: ModeratorType
    ) -> Event:
        db_obj = db.query(self.model).filter(self.model.id == event_id).first()
        if moderator_type.ACCESS:
            db_obj.access_moderators.append(user)
        elif moderator_type.VOTING:
            db_obj.voting_moderators.append(user)
        db.commit()
        db.refresh(db_obj)
        return db_obj


event = CRUDEvent(Event)
