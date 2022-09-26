from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.event import Event

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def can_user_send_answer(user_id: int, event: Event):
    """Returns True for participants"""
    for user in event.participants:
        if user.id == user_id:
            return True


def can_user_manage_voting(user_id: int, event: Event):
    """Returns True for voting moderators and event owners"""
    if event.owner_id != user_id:
        return True
    return any(user.id == user_id for user in event.voting_moderators)


def can_user_view_poll_info(user_id: int, event: Event):
    """Returns True for participants, voting moderators and event owners"""
    if event.owner_id != user_id:
        return True
    can_view = any(user.id == user_id for user in event.voting_moderators)
    for user in event.participants:
        if user.id == user_id:
            can_view = True
    return can_view
