from datetime import date
from pydantic import BaseModel, EmailStr, SecretStr, root_validator


class GetCompanies(BaseModel):
    user: EmailStr

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(values.get(value)) == 0:
                raise ValueError('Form has an empty field.')
            
        return values

class CreateCompany(BaseModel):
    username: str
    name: str
    rep_name: str
    rep_position: str
    year_established: str
    address: str
    contact_number: str
    website: str
    registered_industry: str
    services: str
    regular_workers: int
    parttime_workers: int
    foreign_workers: int
    contact_person_name: str
    contact_person_position: str
    contact_person_number: str
    contact_person_email: EmailStr
    
    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(str(values.get(value))) == 0:
                raise ValueError('Form has an empty field.')

        # check if password and confirm password not matches
        # password, confirm = values.get('password_hash'), values.get('confirm_password')
        # if password != confirm:
        #     raise ValueError('password and confirm password does not match.')
        
        return values
    
class UpdateCompany(BaseModel):
    id: str
    username: str
    name: str
    rep_name: str
    rep_position: str
    year_established: str
    address: str
    contact_number: str
    website: str
    registered_industry: str
    services: str
    regular_workers: int
    parttime_workers: int
    foreign_workers: int
    contact_person_name: str
    contact_person_position: str
    contact_person_number: str
    contact_person_email: EmailStr
    
    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(str(values.get(value))) == 0:
                raise ValueError('Form has an empty field.')

        # check if password and confirm password not matches
        # password, confirm = values.get('password_hash'), values.get('confirm_password')
        # if password != confirm:
        #     raise ValueError('password and confirm password does not match.')
        
        return values
    
class DeleteCompany(BaseModel):
    id: str
    user: str
    
    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(str(values.get(value))) == 0:
                raise ValueError('Form has an empty field.')

        # check if password and confirm password not matches
        # password, confirm = values.get('password_hash'), values.get('confirm_password')
        # if password != confirm:
        #     raise ValueError('password and confirm password does not match.')
        
        return values