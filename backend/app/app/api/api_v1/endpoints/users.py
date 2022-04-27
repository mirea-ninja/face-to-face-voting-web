from typing import Any, List

import requests
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/register", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    is_student: bool = Body(False),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    # if not settings.USERS_OPEN_REGISTRATION:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Open user registration is forbidden on this server",
    #     )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )

    if is_student:
        api_url = "https://lk.mirea.ru/local/ajax/mrest.php"
        payload = {"action": "login", "login": email, "password": password}
        response = requests.get(api_url, params=payload)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="error when trying to log in"
            )
        response_data = response.json()
        if "errors" in response_data:
            raise HTTPException(
                status_code=400, detail=response_data["errors"][0],
            )

        token = response_data["token"]
        profile_api_url = api_url + "?action=getData&url=https://lk.mirea.ru/profile/"
        profile_response = requests.get(
            profile_api_url, headers={"Authorization": token}
        )
        if profile_response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="error when trying to get profile data",
            )
        profile_response_data = profile_response.json()
        if "errors" in profile_response_data:
            raise HTTPException(
                status_code=400, detail=profile_response_data["errors"][0],
            )
        name = profile_response_data["arUser"]["NAME"]
        last_name = profile_response_data["arUser"]["LAST_NAME"]
        second_name = profile_response_data["arUser"]["SECOND_NAME"]
        student = list(profile_response_data["STUDENTS"].values())[0]
        academic_group = student["PROPERTIES"]["ACADEMIC_GROUP"][
            "VALUE_TEXT"
        ]
        full_name = f"{name} {second_name} {last_name}"
        user_in = schemas.UserCreate(
            password=password,
            email=email,
            full_name=full_name,
            academic_group=academic_group,
            is_student=True,
        )
    else:
        user_in = schemas.UserCreate(
            password=password, email=email, full_name=full_name, is_student=False
        )

    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
