from tortoise.contrib.fastapi import register_tortoise
    
def initialize_db(app):
    register_tortoise(
        app,
        db_url='postgres://postgres:admin@localhost:5432/data',
        modules={'models': ['models.user',]},
        generate_schemas=True,
        add_exception_handlers=True
    )
    