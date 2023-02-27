# fastapi
import json
from fastapi import APIRouter, Depends, status, Request, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, FileResponse

# tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError

# helpers, libraries
from typing import List, Type
from dotenv import load_dotenv


# models
from models.user import User
from models.company import Company
from models.contract import Contract, contract_pydantic
from models.contract_schema import GetContracts, CreateContracts, UpdateContract, DeleteContract

# generate pdf
from helpers.generate_pdf import fill_pdf_contract_professional
from helpers.datetime import to_day_string
from helpers.general import zipfiles
from datetime import datetime
from dateutil import tz

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
    # dependencies=[Depends(e.g get_token_header)] # from dependencies.py
    responses={404: {"some_description": "Not found"}}
)

@router.post('/contract_list')
async def get_contracts(user: GetContracts):
    try:
        username = user.dict()['user']
        the_user = await User.get(username=username).values('id')
        
        contracts = await Contract.filter(user=the_user['id']).select_related('company').values('id', 'worker_name', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'site_employment', 'contract_duration', 'contract_terms', 'bonus', 'salary_increase', 'work_start_time', 'work_end_time', 'work_rest', 'work_working_days', 'work_days_off', 'work_leave', 'work_other_leave', 'utilities', 'housing_accomodation','housing_cost', 'job_title', 'job_description', 'job_duties', 'job_criteria_degree', 'job_criteria_jlpt_level', 'job_criteria_year_exp', 'job_criteria_other', 'job_basic_salary', 'job_total_deductions', 'job_income_tax', 'job_social_insurance', 'job_utilities', 'job_accomodation', 'job_net_salary', 'benefits_housing', 'benefits_utilities', 'benefits_transportation', 'benefits_other', 'company_id', company_name='company__name', company_address='company__address', company_contact_number='company__contact_number')
        
        # print(contracts)
        return {'data': contracts, "msg": "list of employment contracts"}
    except Exception as e:
        print("error: ", e)
        
    return {'data': {}, 'msg': 'no data found.'}

@router.get('/generate')
async def generate_contracts(contract_id: str):
    
    try:
        contract_data = await Contract.filter(id=contract_id).select_related('company').values('id', 'worker_name', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'site_employment', 'contract_duration', 'contract_terms', 'bonus', 'salary_increase', 'work_start_time', 'work_end_time', 'work_rest', 'work_working_days', 'work_days_off', 'work_leave', 'work_other_leave', 'utilities', 'housing_accomodation', 'housing_cost', 'job_title', 'job_description', 'job_duties', 'job_criteria_degree', 'job_criteria_jlpt_level', 'job_criteria_year_exp', 'job_criteria_other', 'job_basic_salary', 'job_total_deductions', 'job_income_tax', 'job_social_insurance', 'job_utilities', 'job_accomodation', 'job_net_salary', 'benefits_housing', 'benefits_utilities', 'benefits_transportation', 'benefits_other', 'company_id', company_name='company__name', company_rep_name='company__rep_name',company_rep_position='company__rep_position', company_address='company__address', company_contact_number='company__contact_number')
        
        
        # print(contract_data)
        
        pdf = fill_pdf_contract_professional(contract_data)
        
        # print(pdf)
        
        return zipfiles(pdf, f'files_{contract_id}')
    except Exception as e:
        print("error while generating contract: ", e)
        
    return {'data': {}, 'msg': 'no data found.'}

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_contract(contract: CreateContracts):
    contract_info = contract.dict(exclude_unset=True)
    
    the_user = await User.get(username=contract_info['user']).values('id')
    
    the_company = await Company.get(id=contract_info['company_id']).values('id', 'name', 'address', 'contact_number')
    
    # remove not part of payload
    # del contract_info['date_filled']
    # del contract_info['place_filled']
    del contract_info['user']
    try:
        contract_data = await Contract.create(
            user_id=the_user['id'],
            **contract_info
        )
        
        new_contract = await contract_pydantic.from_tortoise_orm(contract_data)
        
        copied_new_contract = new_contract.dict(exclude_unset=True)
        
        # add company details to the object
        copied_new_contract['company_name'] = the_company['name']
        copied_new_contract['company_address'] = the_company['address']
        copied_new_contract['company_contact_number'] = the_company['contact_number']
        
        # print(copied_new_contract)
    except Exception as e:
        print("error: ", e)
        return {'msg': 'error creating contract.', 'error': str(e)}
    
    return { "msg": "New Employment Contract Added.", "new_data": copied_new_contract}

@router.put('/update', status_code=status.HTTP_200_OK)
async def update_contract(contract_details: UpdateContract):
    contract_data = contract_details.dict(exclude_unset=True)
    the_user = await User.get(username=contract_data['user']).values('id')
    
    # get the contract id
    the_contract = await Contract.get(user_id=the_user['id'],id=contract_data['id']).values('id')
    
    copied_contract = contract_data.copy()
    # slice all unnecessary payloads here
    del copied_contract['id']
    del copied_contract['user']
    
    # print(copied_contract)
    
    await Contract.filter(id=the_contract['id'], user_id=the_user['id']).update(**copied_contract)
    
    updated_contract = await Contract.get(id=the_contract['id']).select_related('company').values('id', 'worker_name', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'site_employment', 'contract_duration', 'contract_terms', 'bonus', 'salary_increase', 'work_start_time', 'work_end_time', 'work_rest', 'work_working_days', 'work_days_off', 'work_leave', 'work_other_leave', 'utilities', 'housing_accomodation', 'housing_cost', 'job_title', 'job_description', 'job_duties', 'job_criteria_degree', 'job_criteria_jlpt_level', 'job_criteria_year_exp', 'job_criteria_other', 'job_basic_salary', 'job_total_deductions', 'job_income_tax', 'job_social_insurance', 'job_utilities', 'job_accomodation', 'job_net_salary', 'benefits_housing', 'benefits_utilities', 'benefits_transportation', 'benefits_other', 'company_id', company_name='company__name', company_address='company__address', company_contact_number='company__contact_number')
    
    return {"msg":"Contract Updated.", "new_data": updated_contract}

@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_contract(contract_details: DeleteContract):
    data = contract_details.dict(exclude_unset=True)
    the_user = await User.get(username=data['user']).values('id')
    
    user = the_user['id']
    cont_id = data['id']
    
    try:
        await Contract.filter(id=cont_id, user_id=user).delete()
        
        return {"msg": "Contract Deleted.", "del_data": cont_id}
    except Exception as e:
        print(e)
        return {"msg": str(e)}