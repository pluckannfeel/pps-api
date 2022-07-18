# helpers, libraries
import email
from typing import List, Type

# fastapi
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError

# models
from models.user import User, user_pydantic, userIn_pydantic, userOut_pydantic, CreateUser, CreateUserToken

# authentication
from auth.authentication import hash_password, token_generator, verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(e.g get_token_header)] # from dependencies.py
    responses={404: {"some_description": "Not found"}}
)  # if you put args here this will be pass to all funcs below you can override it by adding it directly to each


@router.get("/", response_model=List[user_pydantic])
async def get_users():
    return await user_pydantic.from_queryset(User.all())


@router.get("/{username}", tags=["Users"], name="Get user", response_model=user_pydantic, responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}})
async def read_user(username: str):
    return await user_pydantic.from_queryset_single(User.get(username=username))

# response_model=userOut_pydantic


@router.post("/register", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser) -> Type[dict]:
    # if you use user_pydantic_
    # user: userIn_pydantic
    # user_info = user.dict(exclude_unset=True)

    user_info = user.dict(exclude_unset=True)
    print(user_info)
    user = await User.create(first_name=user_info['first_name'], last_name=user_info['last_name'], username=user_info['username'], email=user_info['email'], password_hash=hash_password(user_info['password_hash'].get_secret_value()))
    # user_obj = await User.create(**user_info)

    new_user = await user_pydantic.from_tortoise_orm(user)

    return {'user': new_user, 'msg': "new user created."}


# CreateUserToken |
@router.post("/token", tags=["Users"])
async def generate_token(request_form: CreateUserToken) -> Type[dict]:
    # async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()) -> Type[dict]:
    token = await token_generator(request_form.username, request_form.password)
    print(token)
    return {"access_token": token, "token_type": "bearer"}
