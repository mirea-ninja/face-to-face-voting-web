from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import ModeratorType

router = APIRouter()


@router.get("/", response_model=List[schemas.Event])
def read_events(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve events.
    """
    if crud.user.is_superuser(current_user):
        events = crud.event.get_multi(db, skip=skip, limit=limit)
    else:
        events = crud.event.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return events


@router.post("/", response_model=schemas.Event)
def create_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: schemas.EventCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new event.
    """
    event = crud.event.create_with_owner(
        db=db, obj_in=event_in, owner_id=current_user.id
    )
    return event


@router.put("/{event_id}/{user_id}", response_model=schemas.Event)
def add_participant_to_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a participant to an event.
    """
    event = crud.event.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if not crud.user.is_superuser(current_user) and (event.owner_id != current_user.id):
        for user in event.access_moderators:
            pass
        else:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    event = crud.event.add_participant_to_event(db=db, event_id=event_id, user=user)
    access_log = schemas.AccessLogCreate(
        event_id=event_id, given_by_id=current_user.id, received_id=user_id
    )
    crud.access_log.create(db, obj_in=access_log)
    return event


@router.put("/mod/{moderator_type}/{event_id}/{user_id}", response_model=schemas.Event)
def add_moderator_to_event(
    *,
    db: Session = Depends(deps.get_db),
    moderator_type: str = Path(
        ModeratorType.ACCESS, enum=[ModeratorType.ACCESS, ModeratorType.VOTING]
    ),
    event_id: int,
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a voting or access moderator to an event. Voting moderators can create new votes for the event.
    Access moderators can give add participants to an event.
    """
    event = crud.event.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if not crud.user.is_superuser(current_user) and (event.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    mod_type = None

    if moderator_type == ModeratorType.ACCESS:
        mod_type = ModeratorType(ModeratorType.ACCESS)
        for user in event.access_moderators:
            if user.id == user_id:
                raise HTTPException(
                    status_code=400, detail="user is already a moderator"
                )
    elif moderator_type == ModeratorType.VOTING:
        mod_type = ModeratorType(ModeratorType.VOTING)
        for user in event.voting_moderators:
            if user.id == user_id:
                raise HTTPException(
                    status_code=400, detail="user is already a moderator"
                )
    else:
        raise HTTPException(
            status_code=400, detail="moderator type is specified incorrectly"
        )

    event = crud.event.add_moderator_to_event(
        db=db, event_id=event_id, user=user, moderator_type=mod_type
    )
    return event


@router.put("/{id}", response_model=schemas.Event)
def update_event(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    event_in: schemas.EventUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an event.
    """
    event = crud.event.get(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    if not crud.user.is_superuser(current_user) and (event.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    event = crud.event.update(db=db, db_obj=event, obj_in=event_in)
    return event


@router.get("/{id}", response_model=schemas.Event)
def read_event(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get event by ID.
    """
    event = crud.event.get(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    if not crud.user.is_superuser(current_user) and (event.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return event


@router.delete("/{id}", response_model=schemas.Event)
def delete_event(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an event.
    """
    event = crud.event.get(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    if not crud.user.is_superuser(current_user) and (event.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    event = crud.event.remove(db=db, id=id)
    return event
