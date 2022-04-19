from .crud_access_log import access_log
from .crud_answer import answer
from .crud_answer_option import answer_option
from .crud_event import event
from .crud_item import item
from .crud_poll import poll
from .crud_user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
