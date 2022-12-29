from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Application_Prospect(Model):
    id = fields.UUIDField(pk=True, index=True)
    application = fields.ForeignKeyField("models.Company", related_name="applications_prospect", on_delete=fields.CASCADE)
    job_positon = fields.CharField(max_length=128, null=False)
    no_of_workers = fields.IntField(null=False)
    salary = fields.FloatField(null=False)
    description = fields.TextField(null=False)
    duties = fields.TextField(null=False)
    qualification = fields.TextField(null=False)
    income_tax = fields.FloatField(null=False)
    social_insurance = fields.FloatField(null=False)
    total_deduction = fields.FloatField(null=False)
    net_salary = fields.FloatField(null=False)
    other_allowances = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    

    class Meta:
        table = "application_prospects"
        ordering = ["created_at"]
        
ap_pydantic = pydantic_model_creator(
    Application_Prospect, name="Application_Prospect")

apIn_pydantic = pydantic_model_creator(
    Application_Prospect, name="Application_ProspectIn", exclude_readonly=True)

apOut_pydantic = pydantic_model_creator(
    Application_Prospect, name="Application_ProspectOut") 