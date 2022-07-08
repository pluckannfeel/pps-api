# helpers, libraries
from hashlib import new
import json
from typing import List, Type

#fastapi
from fastapi import APIRouter, Depends, status

#tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError

#models
from models.user import User, user_pydantic, userIn_pydantic, userOut_pydantic

#authentication
from auth.authentication import hash_password, verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(e.g get_token_header)] # from dependencies.py
    responses={404: {"some_description": "Not found"}}
)  # if you put args here this will be pass to all funcs below you can override it by adding it directly to each


@router.get("/", response_model=List[user_pydantic])
async def get_users():
    return await user_pydantic.from_queryset(User.all())


@router.get("/me")
async def read_user_me():
    return {"username": "jarvis"}


@router.get("/{username}", name="Get user", response_model=user_pydantic, responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}})
async def read_user(username: str):
    return await user_pydantic.from_queryset_single(User.get(username=username))

# response_model=userOut_pydantic
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: userIn_pydantic)-> Type[dict]:
    if user:
        user_info = user.dict(exclude_unset=True)

        user_info['password_hash'] = hash_password(user_info['password_hash'])
        user_obj = await User.create(**user_info)

        new_user = await user_pydantic.from_tortoise_orm(user_obj)

        return {'user': new_user, 'msg': "new user created."}
        
    # return new_user

# @router.post('verify', status_code=status.HTTP_200_OK)
# async def confirm_password(password: str) -> Type[dict]:
#     if password:
        