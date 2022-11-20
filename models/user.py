from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class User(Model):
    id = fields.UUIDField(pk=True, index=True)
    first_name = fields.CharField(max_length=128, null=False)
    last_name = fields.CharField(max_length=128, null=False)
    birth_date = fields.DateField(null=False)
    username = fields.CharField(max_length=128, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    phone = fields.CharField(max_length=20, null=False)
    password_hash = fields.CharField(max_length=128, null=False)
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


user_pydantic = pydantic_model_creator(
    User, name="User", exclude=("is_verified", )
)
userIn_pydantic = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True, exclude=("is_verified",)
)

userOut_pydantic = pydantic_model_creator(
    User, name="UserOut",
)
