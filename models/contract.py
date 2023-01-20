from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Contract(Model):
    id = fields.UUIDField(pk=True, index=True)
    user = fields.ForeignKeyField("models.User", related_name="user_contracts", on_delete=fields.CASCADE)
    company = fields.ForeignKeyField("models.Company", related_name="companies_contract", on_delete=fields.CASCADE)
    agency_name = fields.CharField(max_length=128, null=False)
    agency_address = fields.CharField(max_length=128, null=False)
    agency_rep_name = fields.CharField(max_length=128, null=False)
    agency_rep_position = fields.CharField(max_length=128, null=False)
    site_employment = fields.CharField(max_length=128, null=False)
    contract_duration = fields.CharField(max_length=128, null=False)
    contract_terms  = fields.CharField(max_length=128, null=False)
    bonus = fields.CharField(max_length=128, null=False)
    salary_increase = fields.CharField(max_length=128, null=False)
    work_start_time = fields.CharField(max_length=128, null=False)
    work_end_time = fields.CharField(max_length=128, null=False)
    work_workings_days = fields.CharField(max_length=128, null=False)
    work_days_off = fields.CharField(max_length=128, null=False)
    work_leave = fields.CharField(max_length=128, null=False)
    work_other_leave = fields.CharField(max_length=128, null=False)
    job_title = fields.CharField(max_length=128, null=False)
    job_description = fields.TextField(null=False)
    job_duties = fields.TextField(null=False)
    job_basic_salary = fields.CharField(max_length=128, null=False)
    job_total_deductions = fields.CharField(max_length=128, null=False)
    job_income_tax = fields.CharField(max_length=128, null=False)
    job_social_insurance = fields.CharField(max_length=128, null=False)
    job_utilities = fields.CharField(max_length=128, null=False)
    job_accomodation = fields.CharField(max_length=128, null=False)
    job_net_salary = fields.CharField(max_length=128, null=False)
    housing_accomodation = fields.CharField(max_length=128, null=False)
    accomodation_utilities = fields.CharField(max_length=128, null=False)
    transportation = fields.CharField(max_length=128, null=False)
    other_benefits = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    

    class Meta:
        table = "contracts"
        ordering = ["created_at"]
        
contract_pydantic = pydantic_model_creator(
    Contract, name="Contract")

contractIn_pydantic = pydantic_model_creator(
    Contract, name="ContractIn", exclude_readonly=True)

contractOut_pydantic = pydantic_model_creator(
    Contract, name="ContractOut")