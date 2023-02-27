from datetime import date
from pydantic import BaseModel, EmailStr, SecretStr, root_validator

class GetContracts(BaseModel):
    user: EmailStr

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(values.get(value)) == 0:
                raise ValueError('Form has an empty field.')
            
        return values
    
class CreateContracts(BaseModel):
    user: str # id
    company_id: str #id
    worker_name: str
    agency_name: str
    agency_address: str
    agency_rep_name: str
    agency_rep_position: str
    site_employment: str
    contract_duration: str # <num> <year(s)>
    contract_terms: str # choose option but will be 'x' on pdf
    bonus: str # once,twice,byperformance
    salary_increase: str # once,twice,byperformance
    work_start_time: str # 9:00 AM
    work_end_time: str # 5:00 PM
    work_rest: int
    work_working_days: str # Tuesday to Saturday
    work_days_off: str # Sunday & Monday
    work_leave: int # 15
    work_other_leave: str
    utilities: str
    housing_accomodation: str
    housing_cost: int
    job_title: str
    job_description: str
    job_duties: str # list/object str
    job_criteria_degree: str
    job_criteria_jlpt_level: str
    job_criteria_year_exp: str
    job_criteria_other: str
    job_basic_salary: str
    job_total_deductions: str
    job_income_tax: str
    job_social_insurance: str
    job_utilities: str
    job_accomodation: str
    job_net_salary: str
    benefits_housing: str
    benefits_utilities: str
    benefits_transportation: str
    benefits_other: str # object e.g key : benefit name value: benefit value or contents
    
    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(str(values.get(value))) == 0:
                raise ValueError(f'Form has an empty field. : {value}')

        # check if password and confirm password not matches
        # password, confirm = values.get('password_hash'), values.get('confirm_password')
        # if password != confirm:
        #     raise ValueError('password and confirm password does not match.')
        
        return values
    
class UpdateContract(BaseModel):
    id: str
    user: str # id
    company_id: str #id
    worker_name: str
    agency_name: str
    agency_address: str
    agency_rep_name: str
    agency_rep_position: str
    site_employment: str
    contract_duration: str # <num> <year(s)>
    contract_terms: str # choose option but will be 'x' on pdf
    bonus: str # once,twice,byperformance
    salary_increase: str # once,twice,byperformance
    work_start_time: str # 9:00 AM
    work_end_time: str # 5:00 PM
    work_rest: int
    work_working_days: str # Tuesday to Saturday
    work_days_off: str # Sunday & Monday
    work_leave: int # 15
    work_other_leave: str
    utilities: str
    housing_accomodation: str
    housing_cost: int
    job_title: str
    job_description: str
    job_duties: str # list/object str
    job_criteria_degree: str
    job_criteria_jlpt_level: str
    job_criteria_year_exp: str
    job_criteria_other: str
    job_basic_salary: str
    job_total_deductions: str
    job_income_tax: str
    job_social_insurance: str
    job_utilities: str
    job_accomodation: str
    job_net_salary: str
    benefits_housing: str
    benefits_utilities: str
    benefits_transportation: str
    benefits_other: str # object e.g key : benefit name value: benefit value or contents
    
    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }

    @root_validator(pre=True)
    def user_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(str(values.get(value))) == 0:
                raise ValueError(f'Form has an empty field. : {value}')

        # check if password and confirm password not matches
        # password, confirm = values.get('password_hash'), values.get('confirm_password')
        # if password != confirm:
        #     raise ValueError('password and confirm password does not match.')
        
        return values

class DeleteContract(BaseModel):
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