from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.security import can_user_send_answer, can_user_view_poll_info

router = APIRouter()


@router.get("/", response_model=List[schemas.Answer])
def read_answers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve answers.
    """
    if crud.user.is_superuser(current_user):
        items = crud.answer_option.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return items


@router.get("/{poll_id}", response_model=List[schemas.Answer])
def read_answers_by_poll(
    poll_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve answers with specific poll.
    """
    poll = crud.poll.get(db, id=poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    event = crud.event.get(db, id=poll.event_id)
    can_view_options = can_user_view_poll_info(current_user.id, event)
    if can_view_options is False and not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return crud.answer.get_multi_by_poll(db=db, poll_id=poll_id)


@router.post("/", response_model=schemas.Answer)
def send_answer(
    *,
    db: Session = Depends(deps.get_db),
    answer_in: schemas.AnswerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Send new answer.
    """
    poll = crud.poll.get(db, id=answer_in.poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    event = crud.event.get(db, id=poll.event_id)
    if can_user_send_answer(
        current_user.id, event
    ) is False and not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if not poll.is_running:
        raise HTTPException(
            status_code=400, detail="You can only vote in an active poll",
        )

    other_user_answers = crud.answer.get_multi_by_owner(
        db, owner_id=current_user.id, poll_id=answer_in.poll_id
    )
    if len(other_user_answers) > 0:
        raise HTTPException(
            status_code=400,
            detail="You have already submitted your answer to this poll",
        )

    answer = crud.answer.create_with_owner(
        db=db, obj_in=answer_in, owner_id=current_user.id
    )
    return answer


@router.put("/{poll_id}", response_model=schemas.Answer)
def update_answer(
    *,
    db: Session = Depends(deps.get_db),
    poll_id: int,
    answer_in: schemas.AnswerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an answer.
    """

    poll = crud.poll.get(db, id=poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    answers = crud.answer.get_multi_by_poll(
        db=db, poll_id=poll_id, owner_id=current_user.id
    )
    if len(answers) == 0:
        raise HTTPException(status_code=404, detail="Answer not found")

    if not poll.is_running:
        raise HTTPException(
            status_code=400, detail="You can only change the answer in an active poll",
        )

    answer = crud.answer.update(db=db, db_obj=answers[-1], obj_in=answer_in)
    return answer
