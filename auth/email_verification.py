from typing import List
from dotenv import dotenv_values
from models.email_schema import VerificationEmail
from models.user import User
import jwt
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status

# uuid json serialize
import json
from helpers.user import UUIDEncoder

# pydantic schema


# config_credentials
env_credentials = dotenv_values('.env')

email_configuration = ConnectionConfig(
    MAIL_USERNAME="pps.api2022@gmail.com",
    MAIL_PASSWORD="Sivrajnallim96",
    MAIL_FROM="pps.api2022@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# find other mail service = gmail is strict
async def send_email(email: List, userInstance: User):
    token_data = {
        "id": json.dumps(userInstance.id, cls=UUIDEncoder),
        "username": userInstance.username or userInstance.email
    }

    token = jwt.encode(token_data, env_credentials["SECRET_KEY"])

    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
            </head>
            <body>
                <div style = "display: flex; align-items: center; justify-content:
                                center; flex-direction: column">
                    <h3> Account Verificcation </h3>
                    <br>
                    <p> Thank you, please click on link </p>
                    <a href="http://localhost:8000/verification/?token={token}">Verify</a>
                </div>
            </body>
        </html>
    """

    message = MessageSchema(
        subject="Verify User Registration",
        recipients=email,
        body=template,
        subtype="html",
    )
    
    fastmail = FastMail(email_configuration)
    await fastmail.send_message(message=message)
    
    return
    
