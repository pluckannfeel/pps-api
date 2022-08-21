from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Applicant(Model):
    id = fields.UUIDField()
    user_id = fields.ForeignKeyField("models.User", related_name="applicants", on_delete=fields.OnDelete.CASCADE)
    first_name = fields.CharField(max_length=128, null=False)
    middle_name = fields.CharField(max_length=128, null=True)
    last_name = fields.CharField(max_length=128, null=False)
    address = fields.TextField(null=False)
    birth_date = fields.DateField(null=False)
    birth_place = fields.TextField(null=False)
    gender = fields.CharField(max_length=24, null=False)
    civil_status = fields.CharField(max_length=24, null=False)
    email = fields.CharField(max_length=200, null=False, unique=True)
    phone_number = fields.CharField(max_length=128, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)    
    
    staticmethod
    def get_full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        table = "users"
        ordering = ["created_at"]
        
applicant_pydantic = pydantic_model_creator(
    Applicant, name="Applicant")

applicantIn_pydantic = pydantic_model_creator(
    Applicant, name="ApplicantIn", exclude_readonly=True)

applicantOut_pydantic = pydantic_model_creator(
    Applicant, name="ApplicantOut")