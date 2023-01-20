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
from models.application import Application, application_pydantic
from models.application_schema import CreateApplication, GetApplications, UpdateApplication, DeleteApplication

# generate pdf
from helpers.generate_pdf import fill_pdf_professional
from helpers.datetime import to_day_string
from helpers.general import zipfiles

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
    # dependencies=[Depends(e.g get_token_header)] # from dependencies.py
    responses={404: {"some_description": "Not found"}}
)

@router.post('/application_list')
async def get_applications(user: GetApplications):
    try:
        username = user.dict()['user']
        the_user = await User.get(username=username).values('id')
        
        #applications = await Application.filter(user=the_user['id']).select_related('company').order_by('-created_at').values('id', 'application_type', 'employer_category', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'date_filled', 'place_filled', 'job_positions', 'visa_type', 'created_at', company_name='company__name', company_rep_name='company__rep_name', company_rep_position='company__rep_position')
        
        applications = await Application.filter(user=the_user['id']).select_related('company').values('id', 'application_type', 'employer_category', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'date_filled', 'place_filled', 'job_positions', 'visa_type', 'created_at', company_name='company__name', company_rep_name='company__rep_name', company_rep_position='company__rep_position', company_address='company__address', company_website='company__website', company_contact_number='company__contact_number', company_contact_person_name='company__contact_person_name', company_contact_person_number='company__contact_person_number',company_contact_person_position='company__contact_person_position', company_contact_person_email='company__contact_person_email', company_year_established='company__year_established', company_registered_industry='company__registered_industry', company_services='company__services', company_regular_workers='company__regular_workers', company_parttime_workers='company__parttime_workers', company_foreign_workers='company__foreign_workers')
        
        # application_list = await application_pydantic.from_queryset(applications)
        
        return {'data': applications, "msg": "list of applications"}
    except Exception as e:
        print("error: ", e)
        
    return {'data': {}, 'msg': 'no data found.'}

@router.get('/generate')
async def generate_application(application_id: str):
    try:
        # get the application data
        application_data = await Application.filter(id=application_id).select_related('company').values('id', 'application_type', 'employer_category', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'date_filled', 'place_filled', 'job_positions', 'visa_type', 'created_at', company_name='company__name', company_rep_name='company__rep_name', company_rep_position='company__rep_position', company_address='company__address', company_website='company__website', company_contact_number='company__contact_number', company_contact_person_name='company__contact_person_name', company_contact_person_number='company__contact_person_number',company_contact_person_position='company__contact_person_position', company_contact_person_email='company__contact_person_email', company_year_established='company__year_established', company_registered_industry='company__registered_industry', company_services='company__services', company_regular_workers='company__regular_workers', company_parttime_workers='company__parttime_workers', company_foreign_workers='company__foreign_workers')
        
        # generate pdf (returns dict)
        pdf = fill_pdf_professional(application_data)
        
        print(list(pdf))
        
        return zipfiles(pdf, f'files_{application_id}')
        
    except Exception as e:
        print("error: ", e)
        
    return {'data': {}, 'msg': 'no data found.'}

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_applicaction(application: CreateApplication):
    application_info = application.dict(exclude_unset=True)
    # print("username", application_info['user'])
    # user id
    the_user = await User.get(username=application_info['user']).values('id')
    
    
    try:
        application_data = await Application.create(
            # creds
            user_id=the_user['id'],
            company_id=application_info['company_id'],
            application_type=application_info['application_type'],
            employer_category=application_info['employer_category'],
            agency_name=application_info['agency_name'],
            agency_address=application_info['agency_address'],
            agency_rep_name=application_info['agency_rep_name'],
            agency_rep_position=application_info['agency_rep_position'],
            date_filled=application_info['date_filled'],
            place_filled=application_info['place_filled'],
            job_positions=application_info['job_positions'],
            visa_type=application_info['visa_type'],
        )
        
        new_application = await application_pydantic.from_tortoise_orm(application_data)
            
            
    except Exception as e:
        print("error: ", e)
        return {'msg': 'error creating application.', 'error': e}
    
    return { "msg": "New Application Added.", "new_data": new_application}