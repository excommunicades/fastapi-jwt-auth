import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()

engine = create_engine(str(SQLALCHEMY_DATABASE_URL))

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():

    '''Function to session require'''

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
