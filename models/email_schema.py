from typing import List
from pydantic import BaseModel, EmailStr
from typing import List


class VerificationEmail(BaseModel):
    email: List[EmailStr]
