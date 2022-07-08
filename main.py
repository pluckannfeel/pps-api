from fastapi import Depends, FastAPI

# api routers
from routers.users import router as userRouter

app = FastAPI(title="PPS API", version="0.1.1", description="Polo Processsing System's Web api built with FAST Api and TortoiseORM")

# initialize app imports
import uvicorn
from db.init import initialize_db


app.include_router(userRouter)

@app.get('/')
def index():
    return {"msg": "hello world! this is the start"}

initialize_db(app)

# if __name__ == "__main__":
    #database
    
    #ASGI 
    # uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")