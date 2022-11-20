from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class User_Img(Model):
    id = fields.UUIDField(pk=True, index=True)
    user = fields.ForeignKeyField("models.User", related_name="user_imgs", on_delete=fields.CASCADE)
    img_url = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)    
    
    def __str__(self):
        return self.img_url
    
    class Meta: 
        table = "user_imgs"
        ordering = ["created_at"]
        
user_img_pydantic = pydantic_model_creator(User_Img, name="User_Img")