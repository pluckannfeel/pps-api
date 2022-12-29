# fastapi
from fastapi import APIRouter, Depends, status, Request, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError

# helpers, libraries
from typing import List, Type
from dotenv import load_dotenv

# models
from models.user import User
from models.company import Company, company_pydantic
from models.company_schema import CreateCompany, GetCompanies, UpdateCompany, DeleteCompany

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
    # dependencies=[Depends(e.g get_token_header)] # from dependencies.py
    responses={404: {"some_description": "Not found"}}
)

# @router.get("/", response_model=List[company_pydantic])
# async def get_companies():
#     return await company_pydantic.from_queryset(Company.all())

@router.post('/company_list')
async def get_companies(user: GetCompanies):
    try:
        username = user.dict()['user']
        the_user = await User.get(username=username).values('id')
        
        companies = Company.filter(user_id=the_user['id']).order_by('-created_at').all()
        
        company_list = await company_pydantic.from_queryset(companies)
        
        return {'data': company_list, "msg": "list of companies"}
    except Exception as e:
        print("error: ", e)
        
    return {'data': {}, 'msg': 'no data found.'}
    
    

@router.post('/add', status_code=status.HTTP_201_CREATED)
async def create_company(company: CreateCompany):
    company_info = company.dict(exclude_unset=True)
    print("username", company_info['username'])
    # user id
    the_user = await User.get(username=company_info['username']).values('id')
    
    company_data = await Company.create(
        # creds
        user_id=the_user['id'],
        name=company_info['name'],
        rep_name=company_info['rep_name'],
        rep_position=company_info['rep_position'],
        year_established=company_info['year_established'],
        address=company_info['address'],
        contact_number=company_info['contact_number'],
        website=company_info['website'],
        registered_industry=company_info['registered_industry'],
        services=company_info['services'],
        regular_workers=int(company_info['regular_workers']),
        parttime_workers=int(company_info['parttime_workers']),
        foreign_workers=int(company_info['foreign_workers']),
        contact_person_name=company_info['contact_person_name'],
        contact_person_position=company_info['contact_person_position'],
        contact_person_number=company_info['contact_person_number'],
        contact_person_email=company_info['contact_person_email']
    )
    
    new_company = await company_pydantic.from_tortoise_orm(company_data)
    
    return { "msg": "New Company Added.", "new_data": new_company}

@router.put('/update', status_code=status.HTTP_200_OK)
async def update_company(company: UpdateCompany):
    company_data = company.dict(exclude_unset=True)
    the_user = await User.get(username=company_data['username']).values('id')
    # uuid
    user = the_user['id']
    company_id = company_data['id']
    
    # remove primary key id and username to object (immutated)
    copied_company = company_data.copy()
    copied_company.pop("id")
    copied_company.pop("username")
    
    print(list(copied_company))
    
    await Company.filter(id=company_id, user_id=user).update(**copied_company)
    
    # companies = Company.filter(user_id=the_user['id']).all()
        
    # company_list = await company_pydantic.from_queryset(companies)
    new_company = await company_pydantic.from_queryset_single(Company.get(id=company_id))
    
    return {"msg": "Company Updated.", "new_data": new_company}

@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_company(company_details: DeleteCompany):
    data = company_details.dict(exclude_unset=True)
    the_user = await User.get(username=data['user']).values('id')
    
    user = the_user['id']
    company_id = data['id']
    
    try:
        await Company.filter(id=company_id, user_id=user).delete()
        
        return {"msg": "Company Deleted.", "del_data": company_id}
    except Exception as e:
        print(e)
        return {"msg": e}
    
    
    
    