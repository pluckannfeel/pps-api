import logging
import random
import string
import time
from datetime import datetime

# FastAPI
from tokenize import String
from urllib.request import Request
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
# cors headers
from fastapi.middleware.cors import CORSMiddleware
# api routers
from routers.users import router as userRouter
# database
from db.init import initialize_db

#helpers
from helpers.datetime import get_date_time_now


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
# get root logger
logger = logging.getLogger(__name__)


app = FastAPI(title="PPS API", version="0.1.1",
              description="Polo Processsing System's Web api built with FAST Api and TortoiseORM")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

# static file setup config
app.mount("/static", StaticFiles(directory="static"), name="static")

# db
initialize_db(app)

# ROUTERS
app.include_router(userRouter)

origins = [
    'http://127.0.0.1:8000'
    'http://localhost:8000',
    'http://localhost:3000'
]

# middlewares
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*']
                   )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # writes to log.txt
    file = open('api.log', 'a+')
    
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    
    write_log = f'{get_date_time_now()} request path={request.url.path} rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code} '
    file.write(write_log + '\n')
    
    return response


@app.get('/')
def index() -> str:
    return {"msg": "hello world! this is the start"}

# if __name__ == '__main__':
#     # uvicorn.run(app, host=settings.HOST, port=settings.PORT)
#     initialize_db(app)

# ASGI
# uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
