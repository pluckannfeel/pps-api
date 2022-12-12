from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Company_Img(Model):
    id = fields.UUIDField(pk=True, index=True)
    company = fields.ForeignKeyField("models.Company", related_name="company_imgs", on_delete=fields.CASCADE)
    img_url = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)    
    
    def __str__(self):
        return self.img_url
    
    class Meta: 
        table = "company_imgs"
        ordering = ["created_at"]
        
user_img_pydantic = pydantic_model_creator(Company_Img, name="Company_Img")