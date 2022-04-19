from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Poll])
def read_polls(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve polls.
    """
    if crud.user.is_superuser(current_user):
        polls = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        polls = crud.poll.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )

    return polls


@router.post("/", response_model=schemas.Poll)
def create_poll(
    *,
    db: Session = Depends(deps.get_db),
    poll_in: schemas.PollCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new poll.
    """
    event = crud.event.get(db=db, id=poll_in.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.owner_id != current_user.id:
        voting_moderator = False
        for user in event.voting_moderators:
            if user.id == current_user.id:
                voting_moderator = True
        if not crud.user.is_superuser(current_user) and (voting_moderator is False):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    poll = crud.poll.create_with_owner(db=db, obj_in=poll_in, owner_id=current_user.id)
    return poll


@router.put("/change-question/{id}", response_model=schemas.Poll)
def change_poll_question(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    poll_in: schemas.PollRename,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update the text of the poll question.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if not crud.user.is_superuser(current_user) and (poll.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    poll = crud.poll.update(db=db, db_obj=poll, obj_in=poll_in)
    return poll


@router.put("/{id}", response_model=schemas.Poll)
def update_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    poll_in: schemas.PollUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an poll. If `is_poll_running` is set to true, then `stop_at` should not be null.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    event = crud.event.get(db=db, id=poll.event_id)
    if event.owner_id != current_user.id:
        voting_moderator = False
        for user in event.voting_moderators:
            if user.id == current_user.id:
                voting_moderator = True
        if not crud.user.is_superuser(current_user) and (voting_moderator is False):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    poll = crud.poll.update(db=db, db_obj=poll, obj_in=poll_in)
    return poll


@router.get("/{id}", response_model=schemas.Poll)
def read_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get poll by ID.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    event = crud.event.get(db=db, id=poll.event_id)
    if event.owner_id != current_user.id:
        participant_with_viewing = False
        for user in event.voting_moderators:
            if user.id == current_user.id:
                participant_with_viewing = True
        for user in event.participants:
            if user.id == current_user.id:
                participant_with_viewing = True
        if not crud.user.is_superuser(current_user) and (
            participant_with_viewing is False
        ):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    return poll
