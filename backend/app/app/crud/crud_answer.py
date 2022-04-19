from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.schemas.answer import AnswerCreate, AnswerUpdate

from .base import CRUDBase


class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
    def get_multi_by_poll(self, db: Session, *, poll_id: int) -> List[Answer]:
        return db.query(self.model).filter(Answer.poll_id == poll_id).all()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, poll_id: int = None
    ) -> List[Answer]:
        if poll_id:
            return (
                db.query(self.model)
                .filter(Answer.owner_id == owner_id, Answer.poll_id == poll_id)
                .all()
            )
        return db.query(self.model).filter(Answer.owner_id == owner_id).all()

    def create_with_owner(
        self, db: Session, *, obj_in: AnswerCreate, owner_id: int
    ) -> Answer:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


answer = CRUDAnswer(Answer)
