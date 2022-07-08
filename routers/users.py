from typing import List
from fastapi import APIRouter, Depends, status
from models.user import User, user_pydantic, userIn_pydantic

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(e.g get_token_header)] # from dependencies.py
    responses={404: {"some_description": "Not found"}}
)  # if you put args here this will be pass to all funcs below you can override it by adding it directly to each


@router.get("/users", response_model=List[user_pydantic])
async def get_users():
    return await user_pydantic.from_queryset(User.all())


@router.get("/users/me")
async def read_user_me():
    return {"username": "jarvis"}


@router.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}


@router.post("/users", response_model=user_pydantic, status_code=status.HTTP_201_CREATED)
async def create_user(user: userIn_pydantic):
    if user:
        user_obj = await User.create(**user.dict(exclude_unset=True))
        print(user_obj)
        return await user_pydantic.from_tortoise_orm(user_obj)

    return {'msg': "error creating new user"}
