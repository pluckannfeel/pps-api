from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Company(Model):
    id = fields.UUIDField(pk=True, index=True)
    user = fields.ForeignKeyField("models.User", related_name="user_companies", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=256, null=False)
    rep_name = fields.CharField(max_length=128, null=False)
    rep_position = fields.CharField(max_length=128, null=False)
    year_established = fields.CharField(max_length=64, null=False)
    address = fields.TextField(null=False)
    contact_number = fields.CharField(max_length=128, null=False)
    website = fields.CharField(max_length=256, null=False)
    registered_industry = fields.TextField(null=False)
    services = fields.TextField(null=False)
    regular_workers = fields.IntField(null=False)
    parttime_workers = fields.IntField(null=False)
    foreign_workers = fields.IntField(null=False)
    contact_person_name = fields.CharField(max_length=128, null=False)
    contact_person_position = fields.CharField(max_length=128, null=False)
    contact_person_number = fields.CharField(max_length=128, null=False)
    contact_person_email = fields.CharField(max_length=128, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "companies"
        ordering = ["created_at"]
        
company_pydantic = pydantic_model_creator(
    Company, name="Company")

companyIn_pydantic = pydantic_model_creator(
    Company, name="CompanyIn", exclude_readonly=True)

companyOut_pydantic = pydantic_model_creator(
    Company, name="CompanyOut")