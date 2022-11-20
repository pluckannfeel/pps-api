from datetime import date
from pydantic import BaseModel, root_validator

import json

class UploadUserImage(BaseModel):
    username: str = None
    
    
    # these two class methods right here, transforms the validator data to json format is needed to accept during the request
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    @root_validator(pre=True)
    def image_info_validator(cls, values):
        # check values if there is one null
        for value in values:
            if len(values.get(value)) == 0:
                raise ValueError('Form has an empty field.')
        
        return values