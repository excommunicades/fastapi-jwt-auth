from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from fastapi import HTTPException

from fastapi_jwt_auth.pkg.db.database import engine 

def register_startup_event(app):
    @app.on_event("startup")
    async def startup():
        print('Checking database connection...')

        try:

            with engine.connect() as connection:

                connection.execute(text('SELECT 1'))

            print("Database connection successful")

        except OperationalError:

            raise HTTPException(status_code=500, detail="Database connection failed")
