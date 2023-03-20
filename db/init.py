from tortoise.contrib.fastapi import register_tortoise
import os
from dotenv import load_dotenv

load_dotenv()

db_uri = os.environ['DB_URI']
    
def initialize_db(app):
    register_tortoise(
        app,
        # db_url='postgres://postgres:admin@localhost:5432/data',
        db_url=db_uri,
        modules={
            'models': [
                'models.user', 
                'models.user_img',
                'models.company',
                'models.company_img',
                'models.application',
                'models.contract'
                # 'models.application_prospect',
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True
    )
    print('db initialized')
    