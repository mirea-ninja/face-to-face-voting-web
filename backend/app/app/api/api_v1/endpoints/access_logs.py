from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{event_id}", response_model=List[schemas.AccessLog])
def read_access_logs(
    event_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    given_by_id: int = None,
    received_id: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve logs.
    """
    event = crud.event.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")

    moderator = any(user.id == current_user.id for user in event.access_moderators)
    if (
        not crud.user.is_superuser(current_user)
        and (event.owner_id != current_user.id)
        and not moderator
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if given_by_id:
        user = crud.user.get(db=db, id=given_by_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="user with the id passed to `given_by_id` was not found",
            )
    if received_id:
        user = crud.user.get(db=db, id=received_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="user with the id passed to `received_id` was not found",
            )

    return crud.access_log.get_multi(
        db=db,
        event_id=event_id,
        skip=skip,
        limit=limit,
        given_by_id=given_by_id,
        received_id=received_id,
    )
