from sqlalchemy import Column, Integer, String

from fastapi_jwt_auth.pkg.db.database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    nickname = Column(String, unique=True, index=True)

    email = Column(String, unique=True, index=True)

    password_hash = Column(String)
