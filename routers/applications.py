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
from models.company import Company

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
       
        applications = await Application.filter(user=the_user['id']).select_related('company').values('id', 'application_type', 'employer_category', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'date_filled', 'place_filled', 'job_positions', 'visa_type', 'created_at','company_id', company_name='company__name', company_rep_name='company__rep_name', company_rep_position='company__rep_position', company_address='company__address', company_website='company__website', company_contact_number='company__contact_number', company_contact_person_name='company__contact_person_name', company_contact_person_number='company__contact_person_number',company_contact_person_position='company__contact_person_position', company_contact_person_email='company__contact_person_email', company_year_established='company__year_established', company_registered_industry='company__registered_industry', company_services='company__services', company_regular_workers='company__regular_workers', company_parttime_workers='company__parttime_workers', company_foreign_workers='company__foreign_workers')
        
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
async def create_application(application: CreateApplication):
    application_info = application.dict(exclude_unset=True)
    # print("username", application_info['user'])
    # user id
    the_user = await User.get(username=application_info['user']).values('id')
    
    the_company = await Company.get(id=application_info['company_id']).values('id', 'name', 'address', 'contact_number', 'registered_industry', 'services', 'year_established', 'website', 'contact_person_name', 'contact_person_number', 'contact_person_position', 'rep_name', 'rep_position')
    
    print(application_info)
    
    try:
        application_data = await Application.create(
            # creds
            user_id=the_user['id'],
            company_id=the_company['id'],
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
        
        copied_new_application = new_application.dict(exclude_unset=True)
        
        # add company details to the object
        copied_new_application['company_name'] = the_company['name']
        copied_new_application['company_address'] = the_company['address']
        copied_new_application['company_contact_number'] = the_company['contact_number']
        copied_new_application['company_registered_industry'] = the_company['registered_industry']
        copied_new_application['company_services'] = the_company['services']
        copied_new_application['company_year_established'] = the_company['year_established']
        copied_new_application['company_website'] = the_company['website']
        copied_new_application['company_contact_person_name'] = the_company['contact_person_name']
        copied_new_application['company_contact_person_number'] = the_company['contact_person_number']
        copied_new_application['company_contact_person_position'] = the_company['contact_person_position']
        copied_new_application['company_rep_name'] = the_company['rep_name']
        copied_new_application['company_rep_position'] = the_company['rep_position']
            
    except Exception as e:
        print("error: ", e)
        return {'msg': 'error creating application.', 'error': e}
    
    return { "msg": "New Application Added.", "new_data": copied_new_application}

@router.put('/update', status_code=status.HTTP_200_OK)
async def update_application(application_details: UpdateApplication):
    application_data = application_details.dict(exclude_unset=True)
    the_user = await User.get(username=application_data['user']).values('id')
    # uuid
    user_id = the_user['id']

    # get the application id
    the_app = await Application.get(user_id=user_id, id=application_data['id']).values('id')
    
    #uuid
    # app_id = the_app['id']
    app_id = application_data['id']
    
    print("appkeys: ", application_data)
    
    copied_app = application_data.copy()
    del copied_app['user']
    del copied_app['id']
    
    await Application.filter(id=app_id, user_id=user_id).update(
        company_id=copied_app['company'],
        application_type=copied_app['application_type'],
        employer_category=copied_app['employer_category'],
        agency_name=copied_app['agency_name'],
        agency_address=copied_app['agency_address'],
        agency_rep_name=copied_app['agency_rep_name'],
        agency_rep_position=copied_app['agency_rep_position'],
        date_filled=copied_app['date_filled'],
        place_filled=copied_app['place_filled'],
        job_positions=copied_app['job_positions'],
        visa_type=copied_app['visa_type'],
    )
    
    
    updated_app = await Application.get(id=app_id).select_related('company').values('id', 'application_type', 'employer_category', 'agency_name', 'agency_address', 'agency_rep_name', 'agency_rep_position', 'date_filled', 'place_filled', 'job_positions', 'visa_type', 'created_at', company_name='company__name', company_rep_name='company__rep_name', company_rep_position='company__rep_position', company_address='company__address', company_website='company__website', company_contact_number='company__contact_number', company_contact_person_name='company__contact_person_name', company_contact_person_number='company__contact_person_number',company_contact_person_position='company__contact_person_position', company_contact_person_email='company__contact_person_email', company_year_established='company__year_established', company_registered_industry='company__registered_industry', company_services='company__services', company_regular_workers='company__regular_workers', company_parttime_workers='company__parttime_workers', company_foreign_workers='company__foreign_workers')
    
    return {"msg":"Application Updated.", "new_data": updated_app}

@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_application(application_details: DeleteApplication):
    data = application_details.dict(exclude_unset=True)
    the_user = await User.get(username=data['user']).values('id')
    
    user = the_user['id']
    app_id = data['id']
    
    try:
        await Application.filter(id=app_id, user_id=user).delete()
        
        return {"msg": "Application Deleted.", "del_data": app_id}
    except Exception as e:
        print(e)
        return {"msg": str(e)}
    
