from typing import List

from sqlalchemy.orm import Session

from app.models.answer_option import AnswerOption
from app.schemas.answer_option import AnswerOptionCreate, AnswerOptionUpdate

from .base import CRUDBase


class CRUDAnswerOprion(CRUDBase[AnswerOption, AnswerOptionCreate, AnswerOptionUpdate]):
    def get_multi_by_event(self, db: Session, *, event_id: int) -> List[AnswerOption]:
        return db.query(self.model).filter(AnswerOption.event_id == event_id).all()


answer_option = CRUDAnswerOprion(AnswerOption)
