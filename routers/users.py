# helpers, libraries
import email
from typing import List, Type

# fastapi
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError

# models
from models.user import User, user_pydantic
from models.user_schema import CreateUser, CreateUserToken

# authentication
from auth.authentication import hash_password, token_generator, verify_password, verify_token_email

# email user verification
from auth.email_verification import send_email

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


@router.get("/verification/", tags=["Users"], name="Verify User", responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}})
async def verify_user(token: str):  # request: Request,
    user = await verify_token_email(token)
    print("user object ", user)
    if user:
        if not user.is_verified:
            user.is_verified = True
            # await User.filter(id=user.id).update()
            await user.save()
            return {"msg": "user successfully verified."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired token.",
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.post("/register", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser) -> dict:
    # if you use user_pydantic_
    # user: userIn_pydantic
    # user_info = user.dict(exclude_unset=True)

    # note: not a good idea to put validations here, e.g for password: password is hashed after this line, its better to check the password field in front end

    user_info = user.dict(exclude_unset=True)

    user_data = await User.create(first_name=user_info['first_name'], last_name=user_info['last_name'], birth_date=user_info['birth_date'], username=user_info['username'], email=user_info['email'], password_hash=hash_password(user_info['password_hash'].get_secret_value()))
    # user_obj = await User.create(**user_info)

    new_user = await user_pydantic.from_tortoise_orm(user_data)

    emails = [new_user.email]

    if new_user:
        print("New user: " + new_user.email)
        # for sending email verification
        # await send_email(emails, new_user)

    return {'user': new_user, 'msg': "new user created."}


@router.post("/login", tags=["Users"], status_code=status.HTTP_200_OK)
async def login_user(request_form: CreateUserToken) -> dict:
    token = await token_generator(request_form.username, request_form.password)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {'token': token}


@router.post("/token", tags=["Users"])
async def generate_token(request_form: CreateUserToken) -> dict:
    # async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()) -> Type[dict]:
    token = await token_generator(request_form.username, request_form.password)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {"access_token": token, "token_type": "bearer"}
