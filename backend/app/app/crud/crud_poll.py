from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.poll import Poll
from app.schemas.poll import PollCreate, PollUpdate

from .base import CRUDBase


class CRUDPoll(CRUDBase[Poll, PollCreate, PollUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PollCreate, owner_id: int
    ) -> Poll:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Poll]:
        return (
            db.query(self.model)
            .filter(Poll.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_event(self, db: Session, *, event_id: int) -> List[Poll]:
        return db.query(self.model).filter(Poll.event_id == event_id).all()


poll = CRUDPoll(Poll)
