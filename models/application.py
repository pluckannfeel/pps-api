from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Application(Model):
    id = fields.UUIDField(pk=True, index=True)
    user = fields.ForeignKeyField("models.User", related_name="user_applications", on_delete=fields.CASCADE)
    company = fields.ForeignKeyField("models.Company", related_name="company_applications", on_delete=fields.CASCADE)
    application_type = fields.CharField(max_length=128, null=False)
    employer_category = fields.CharField(max_length=128, null=False)
    agency_name = fields.CharField(max_length=128, null=False)
    agency_address = fields.CharField(max_length=128, null=False)
    agency_rep_name = fields.CharField(max_length=128, null=False)
    agency_rep_position = fields.CharField(max_length=128, null=False)
    date_filled = fields.DateField(null=False)
    place_filled  = fields.CharField(max_length=128, null=False)
    job_positions = fields.TextField(null=False)
    visa_type = fields.CharField(max_length=128, null=False)
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