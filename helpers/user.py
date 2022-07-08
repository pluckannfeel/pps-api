from typing import Type
from models.user import User, user_pydantic 

async def get_user_by_username(input_username: str) -> Type[user_pydantic]:
    return await user_pydantic.from_queryset_single(User.get(username=input_username))