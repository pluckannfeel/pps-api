from tortoise.contrib.fastapi import register_tortoise
    
def initialize_db(app):
    register_tortoise(
        app,
        db_url='postgres://postgres:admin@localhost:5432/data',
        modules={
            'models': [
                'models.user', 
                'models.user_img',
                'models.company',
                'models.company_img',
                'models.application',
                'models.application_prospect',
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True
    )
    print('db initialized')
    