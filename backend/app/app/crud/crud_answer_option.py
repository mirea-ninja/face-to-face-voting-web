from app.models.answer_option import AnswerOption
from app.schemas.answer_option import AnswerOptionCreate, AnswerOptionUpdate

from .base import CRUDBase

answer_option = CRUDBase[AnswerOption, AnswerOptionCreate, AnswerOptionUpdate](
    AnswerOption
)
