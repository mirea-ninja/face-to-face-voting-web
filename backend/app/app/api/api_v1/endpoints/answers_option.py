from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.security import can_user_manage_voting, can_user_view_poll_info

router = APIRouter()


@router.get("/", response_model=List[schemas.AnswerOption])
def read_answers_options(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve answer options.
    """
    if crud.user.is_superuser(current_user):
        items = crud.answer_option.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return items


@router.get("/{event_id}", response_model=List[schemas.AnswerOption])
def read_answers_options_by_event(
    event_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve answer options. A regular user can only get the options of events in which he is a
    participant or moderator of the voting.
    """
    event = crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    can_view_options = can_user_view_poll_info(current_user.id, event)
    if can_view_options is False:
        if not crud.user.is_superuser(current_user):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    answer_options = crud.answer_option.get_multi_by_event(db=db, event_id=event_id)
    return answer_options


@router.post("/", response_model=schemas.AnswerOption)
def create_option(
    *,
    db: Session = Depends(deps.get_db),
    option_in: schemas.AnswerOptionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new answer option.
    """
    poll = crud.poll.get(db, id=option_in.poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    event = crud.event.get(db, id=poll.event_id)
    if can_user_manage_voting(current_user.id, event) is False:
        if not crud.user.is_superuser(current_user):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    if poll.is_running:
        raise HTTPException(
            status_code=400,
            detail="You cannot create new answer options while the poll is running",
        )

    answer_option = crud.answer_option.create(db=db, obj_in=option_in)
    return answer_option


@router.put("/{id}", response_model=schemas.AnswerOption)
def update_option(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    option_in: schemas.AnswerOptionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an answer option.
    """

    answer_option = crud.answer_option.get(db=db, id=id)
    if not answer_option:
        raise HTTPException(status_code=404, detail="Answer option not found")

    poll = crud.poll.get(db, id=option_in.poll_id)
    event = crud.event.get(db, id=poll.event_id)
    if can_user_manage_voting(current_user.id, event) is False:
        if not crud.user.is_superuser(current_user):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    answer_option = crud.answer_option.update(
        db=db, db_obj=answer_option, obj_in=option_in
    )
    return answer_option


@router.delete("/{id}", response_model=schemas.AnswerOption)
def delete_answer_option(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an answer option.
    """
    answer_option = crud.answer_option.get(db=db, id=id)
    if not answer_option:
        raise HTTPException(status_code=404, detail="Answer option not found")
    poll = crud.poll.get(db, id=answer_option.poll_id)
    event = crud.event.get(db, id=poll.event_id)
    if can_user_manage_voting(current_user.id, event) is False:
        if not crud.user.is_superuser(current_user):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    if poll.is_running:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete answer options while the poll is running",
        )

    if len(answer_option.answers) > 0:
        raise HTTPException(
            status_code=400,
            detail="There are answers with this option. First, delete them",
        )

    answer_option = crud.answer_option.remove(db=db, id=id)
    return answer_option
