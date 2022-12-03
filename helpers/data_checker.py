from fastapi import FastAPI, status, Form, UploadFile, File, Depends, Request
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# models = {"user", user, "applicant", applicant}

class DataChecker:
    def __init__(self, user: str):
        self.user = user

    def __call__(self, data: str = Form(...)):
        try:
            # model = models[self.name].parse_raw(data)
            payload = self.user.parse_raw(data)
        except ValidationError as e:
            raise HTTPException(
                detail=jsonable_encoder(e.errors()),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return payload