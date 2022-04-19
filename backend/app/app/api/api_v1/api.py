from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    access_logs,
    answers,
    answers_option,
    events,
    items,
    login,
    polls,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(
    access_logs.router, prefix="/access-logs", tags=["access-logs"]
)
api_router.include_router(polls.router, prefix="/polls", tags=["polls"])
api_router.include_router(
    answers_option.router, prefix="/answer-options", tags=["answer-options"]
)
api_router.include_router(answers.router, prefix="/answers", tags=["answers"])
