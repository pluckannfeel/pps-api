from json import JSONEncoder, JSONDecoder
from uuid import UUID

from typing import Type

from models.user import User, user_pydantic

async def get_user_by_username(input_username: str) -> user_pydantic:
    return await user_pydantic.from_queryset_single(User.get(username=input_username))

class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the ob is uuid,
            return str(obj)
        return JSONEncoder.default(self, obj)
    
    
class UUIDDecoder(JSONDecoder):
    def decode(self, obj):
        return JSONDecoder.decode(self, obj)