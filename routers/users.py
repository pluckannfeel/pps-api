from datetime import datetime
import shutil, os, time

# helpers, libraries
from typing import List, Type
from dotenv import load_dotenv
from helpers.definitions import get_directory_path
from helpers.s3_file_upload import upload_image_to_s3
from helpers.data_checker import DataChecker as data_checker

# fastapi
from fastapi import APIRouter, Depends, status, Request, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError

# models
from models.user import User, user_pydantic
from models.user_schema import CreateUser, CreateUserToken, ChangeUserPassword
from models.user_img import User_Img, user_img_pydantic
from models.user_img_schema import UploadUserImage

# authentication
from auth.authentication import hash_password, token_generator, verify_password, verify_token_email

# email user verification
from auth.email_verification import send_email

load_dotenv()
# file upload local
upload_path = get_directory_path() +  '\\uploads'
# file upload s3 bucket
s3_upload_path = os.getenv("AWS_PPS_STORAGE_URI") + 'uploads'

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(e.g get_token_header)] # from dependencies.py
    responses={404: {"some_description": "Not found"}}
)  # if you put args here this will be pass to all funcs below you can override it by adding it directly to each


@router.get("/", response_model=List[user_pydantic])
async def get_users():
    return await user_pydantic.from_queryset(User.all())


@router.get("/{username}", tags=["Users"], name="Get user", response_model=user_pydantic, responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}})
async def read_user(username: str):
    return await user_pydantic.from_queryset_single(User.get(username=username))

# response_model=userOut_pydantic


@router.get("/verification/", tags=["Users"], name="Verify User", responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}})
async def verify_user(token: str):  # request: Request,
    user = await verify_token_email(token)
    print("user object ", user)
    if user:
        if not user.is_verified:
            user.is_verified = True
            # await User.filter(id=user.id).update()
            await user.save()
            return {"msg": "user successfully verified."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired token.",
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.post("/register", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser) -> dict:
    # if you use user_pydantic_
    # user: userIn_pydantic
    # user_info = user.dict(exclude_unset=True)

    # note: not a good idea to put validations here, e.g for password: password is hashed after this line, its better to check the password field in front end

    user_info = user.dict(exclude_unset=True)

    user_data = await User.create(first_name=user_info['first_name'], last_name=user_info['last_name'], birth_date=user_info['birth_date'], username=user_info['username'], email=user_info['email'], phone=user_info['phone'], password_hash=hash_password(user_info['password_hash'].get_secret_value()))
    # user_obj = await User.create(**user_info)

    new_user = await user_pydantic.from_tortoise_orm(user_data)

    emails = [new_user.email]

    if new_user:
        print("New user: " + new_user.email)
        # for sending email verification
        await send_email(emails, new_user)

    return {'user': new_user, 'msg': "new user created."}

@router.post("/user_add_img", tags=["Users"], status_code=status.HTTP_201_CREATED)
# async def add_user_img(user: str, file: UploadFile = File(...)) -> dict:
async def add_user_img(user: str = Depends(data_checker), file: UploadFile = File(...)):
    # current path to save on local uploads folder but we will save it on s3 bucket later on
    print(user)
    print(file)
    
    # img_info = user_img.dict()
    the_user = await User.get(username=user).values('id')
    username = user

    # to avoiid file name duplicates, lets concatenate datetime and user's name
    now = datetime.now()
    new_image_name = username.split('@')[0] + now.strftime("_%Y%m%d_%H%M%S") + '.' + file.filename.split('.')[-1]
    
    s3_upload_file = s3_upload_path + '/' + new_image_name
    # check if content type is image
    is_file_img = file.content_type.startswith('image')
    

    # upload image to s3 bucket
    upload_image_to_s3(file, new_image_name)
    
    user_img_data = await User_Img.create(user_id=the_user['id'], img_url=s3_upload_file)
    
    new_user_img = await user_img_pydantic.from_tortoise_orm(user_img_data)
    
    if not new_user_img and not is_file_img:
        return {'error_msg': "user image not added."}
    
    # upload_file = upload_path + '\\' + new_image_name
    # image_name = image.split('\\')[-1]
      
    # save to local directory
    # with open(upload_file, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)  
    # time.sleep(2)
    # after inserting renaem the file
    # os.rename(upload_file, upload_path + '\\' + new_image_name)

    return {'file': file.filename, 'msg': "new user image created."}

@router.get("/get_user_credentials/", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def get_user_credentials(username: str) -> dict:
    the_user = await User.get(username=username).values('id')
    
    user_data = object()
    
    # this include the user_img table 
    joined_data = await User_Img.filter(user=the_user['id']).prefetch_related('user').order_by('-created_at').values('img_url', 'user__username', 'user__first_name', 'user__last_name', 'user__birth_date', 'user__email', 'user__phone', 'user__is_verified', 'user__created_at')
        
    # SQL = User_Img.filter(user=the_user['id']).prefetch_related('user').values('img_url', 'user__username', 'user__first_name', 'user__last_name', 'user__birth_date', 'user__email', 'user__phone', 'user__is_verified', 'user__created_at').sql()
    # print(SQL)
    
    
    # if joined data is empty return data without user_img table
    if not joined_data:
        user_only_data = await User.filter(username=username).values('username', 'first_name', 'last_name', 'birth_date', 'email', 'phone', 'is_verified', 'created_at')
        print(user_only_data[0]['username'])
        
    # transform
    user_data = {
        'username': joined_data[0]['user__username'] if joined_data else user_only_data[0]['username'],
        'first_name': joined_data[0]['user__first_name'] if joined_data else user_only_data[0]['first_name'],
        'last_name': joined_data[0]['user__last_name'] if joined_data else user_only_data[0]['last_name'],
        'email': joined_data[0]['user__email'] if joined_data else user_only_data[0]['email'],
        'phone': joined_data[0]['user__phone'] if joined_data else user_only_data[0]['phone'],
        'birth_date': joined_data[0]['user__birth_date'] if joined_data else user_only_data[0]['birth_date'],
        'is_verified': joined_data[0]['user__is_verified'] if joined_data else user_only_data[0]['is_verified'],
        'created_at': joined_data[0]['user__created_at'] if joined_data else user_only_data[0]['created_at'],
        'img_url': joined_data[0]['img_url'] if joined_data else ''        
    }
    
    return user_data

@router.get("/get_user_img/", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def get_user_img(username: str, request: Request) -> dict:
    the_user = await User.get(username=username).values('id')
    # print('user_id', the_user['id'])

    return await user_img_pydantic.from_queryset_single(User_Img.get(user=the_user['id']))
    
    # user_img = await User_Img.filter(user_id=the_user['id']).values('img_url')
    # print("user_img: ", user_img)
    # return {'user_img': user_img, 'msg': "user image."}

    
@router.post("/user_upload_file", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def root(file: UploadFile = File(...)):
    
    if file:
        # file (save to clouse like s3 or other 3rd party)
        upload_file = upload_path + '\\' + file.filename
        with open(upload_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    else:
        return {"filename": file.filename}

@router.post("/login", tags=["Users"], status_code=status.HTTP_200_OK)
async def login_user(request_form: CreateUserToken) -> dict:
    token = await token_generator(request_form.username, request_form.password)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {'token': token, 'email': request_form.username}


@router.put("/change_password", tags=["Users"], status_code=status.HTTP_200_OK)
async def change_password(request_form: ChangeUserPassword) -> dict:
    user = await User.get(username=request_form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    old_password = request_form.old_password.get_secret_value()
    
    if not await verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user.password_hash = hash_password(request_form.new_password.get_secret_value())
    await user.save()

    return {'msg': "your password was successfully changed."}


@router.post("/token", tags=["Users"])
async def generate_token(request_form: CreateUserToken) -> dict:
    # async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()) -> Type[dict]:
    token = await token_generator(request_form.username, request_form.password)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {"access_token": token, "token_type": "bearer"}
