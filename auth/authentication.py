from ctypes import Union
import email
import json
from typing import Type
from unicodedata import name
from passlib.context import CryptContext
import jwt
from dotenv import dotenv_values

# FastAPI
from fastapi import HTTPException, status
from tortoise.expressions import Q

# models
from models.user import User

# helper
from helpers.user import UUIDEncoder

# config_credentials
env_credentials = dotenv_values('.env')

# password hash context
password_hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return password_hash_context.hash(password)


def verify_password(input_password: str, hashed_password: str) -> str:
    return password_hash_context.verify(input_password, hashed_password)


async def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, env_credentials["SECRET_KEY"], algorithms="HS256")
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


async def verify_password(input_password: str, hashed_password: str) -> str:
    return password_hash_context.verify(input_password, hashed_password)


async def authenticate_user(username_or_email: str, password_hash: str):
    user = await User.get(Q(username=username_or_email) | Q(email=username_or_email))
    print(authenticate_user)
    if user and verify_password(password_hash, user.password_hash):
        return user

    return False


# password is actually password_hash in models
async def token_generator(username_or_email: str, password: str) -> str:
    user = await authenticate_user(username_or_email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate:": "Bearer"}
        )

    token_data = {
        "id": json.dumps(user.id, cls=UUIDEncoder),
        "username": user.username
    }

    token = jwt.encode(token_data, env_credentials["SECRET_KEY"])
    return token
