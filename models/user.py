from dataclasses import field
from enum import auto, unique
from operator import index
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
# from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError, root_validator


class User(Model):
    id = fields.UUIDField(pk=True, index=True)
    first_name = fields.CharField(max_length=128, null=False)
    last_name = fields.CharField(max_length=128, null=False)
    username = fields.CharField(max_length=128, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    password_hash = fields.CharField(max_length=128, null=True)
    is_verified = fields.BooleanField(default=False, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    @staticmethod
    def get_full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        table = "users"
        ordering = ["created_at"]
        
        
class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password_hash: SecretStr
    confirm_password: SecretStr
    
    @root_validator
    def check_passwords_match(cls, values):
        password, confirm = values.get('password_hash'), values.get('confirm_password')
        if password is not None and confirm is not None and password != confirm:
            raise ValueError('passwords do not match')
        return values
    


user_pydantic = pydantic_model_creator(
    User, name="User", exclude=("is_verified", )
)
userIn_pydantic = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True, exclude=("is_verified",)
)

userOut_pydantic = pydantic_model_creator(
    User, name="UserOut", exclude=("password_hash"),
)
