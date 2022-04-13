# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.access_log import AccessLog  # noqa
from app.models.answer import Answer  # noqa
from app.models.answer_option import AnswerOption  # noqa
from app.models.event import Event  # noqa
from app.models.item import Item  # noqa
from app.models.poll import Poll  # noqa
from app.models.user import User  # noqa
