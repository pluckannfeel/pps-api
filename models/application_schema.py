from datetime import date
from pydantic import BaseModel, EmailStr, SecretStr, root_validator


class GetApplications(BaseModel):
    user: EmailStr

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(values.get(value)) == 0:
                raise ValueError('Form has an empty field.')
            
        return values

class CreateApplication(BaseModel):
    user: str # id
    company_id: str #id
    application_type: str
    employer_category: str
    agency_name: str
    agency_address: str
    agency_rep_name: str
    agency_rep_position: str
    date_filled: date
    place_filled: str
    job_positions: str
    visa_type: str
    
    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(str(values.get(value))) == 0:
                raise ValueError(f'Form has an empty field: {value}')

        # check if password and confirm password not matches
        # password, confirm = values.get('password_hash'), values.get('confirm_password')
        # if password != confirm:
        #     raise ValueError('password and confirm password does not match.')
        
        return values
    
class UpdateApplication(BaseModel):
    id: str
    user: str # id
    company: str #id
    application_type: str
    employer_category: str
    agency_name: str
    agency_address: str
    agency_rep_name: str
    agency_rep_position: str
    date_filled: date
    place_filled: str
    job_positions: str
    visa_type: str
    
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
    
class DeleteApplication(BaseModel):
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