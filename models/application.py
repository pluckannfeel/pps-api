from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Application(Model):
    id = fields.UUIDField(pk=True, index=True)
    company = fields.ForeignKeyField("models.Company", related_name="companies_application", on_delete=fields.CASCADE)
    application_type = fields.CharField(max_length=128, null=False)
    employer_category = fields.CharField(max_length=128, null=False)
    pra_name = fields.CharField(max_length=128, null=False)
    pra_address = fields.CharField(max_length=128, null=False)
    pra_head_name = fields.CharField(max_length=128, null=False)
    pra_head_position = fields.CharField(max_length=128, null=False)
    visa_type = fields.CharField(max_length=128, null=False)
    employment_address = fields.CharField(max_length=128, null=False)
    contract_duration = fields.CharField(max_length=128, null=False)
    bonus = fields.BooleanField(null=False)
    salary_increase = fields.BooleanField(null=False)
    work_days = fields.CharField(max_length=128, null=False)
    work_hours = fields.CharField(max_length=128, null=False)
    rest_period = fields.CharField(max_length=128, null=False)
    rest_days = fields.CharField(max_length=128, null=False)
    leave = fields.IntField(null=False)
    allowance = fields.CharField(max_length=128, null=False)
    deduction = fields.CharField(max_length=128, null=False)
    accomodation = fields.CharField(max_length=128, null=False)
    utility_fees = fields.CharField(max_length=128, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    

    class Meta:
        table = "applications"
        ordering = ["created_at"]
        
application_pydantic = pydantic_model_creator(
    Application, name="Application")

applicationIn_pydantic = pydantic_model_creator(
    Application, name="ApplicationIn", exclude_readonly=True)

applicationOut_pydantic = pydantic_model_creator(
    Application, name="ApplicationOut")