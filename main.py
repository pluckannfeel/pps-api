#FastAPI
from lib2to3.pgen2 import token
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
# cors headers
from fastapi.middleware.cors import CORSMiddleware
# api routers
from routers.users import router as userRouter
#database
from db.init import initialize_db


app = FastAPI(title="PPS API", version="0.1.1",
              description="Polo Processsing System's Web api built with FAST Api and TortoiseORM")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

#static file setup config
app.mount("/static", StaticFiles(directory="static"), name="static")

#ROUTERS
app.include_router(userRouter)

origins = [
    'http://localhost:8000'
]

# middlewares
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*']
                   )


@app.get('/')
def index() -> str:
    return {"msg": "hello world! this is the start"}


initialize_db(app)

# if __name__ == "__main__":
# database

# ASGI
# uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
