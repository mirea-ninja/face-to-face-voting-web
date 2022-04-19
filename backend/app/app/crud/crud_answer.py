from app.models.answer import Answer
from app.schemas.answer import AnswerCreate, AnswerUpdate

from .base import CRUDBase

answer = CRUDBase[Answer, AnswerCreate, AnswerUpdate](Answer)
