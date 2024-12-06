import bcrypt

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException, status

from fastapi_jwt_auth.pkg.db.models import (
    User,
)
from fastapi_jwt_auth.pkg.jwt.repository import JWT_Repository

class UserManagementRepository:

    def __init__(self, db: Session):

        self.db = db
        self.jwt_repository = JWT_Repository()

    def register(self, nickname: str, email: str, password: str) -> User:

        """Create user logic with unique nickname, email, and password encryption"""

        if self.db.query(User).filter_by(email=email).first():

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

        if self.db.query(User).filter_by(nickname=nickname).first():

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Nickname already registered')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(nickname=nickname, email=email, password_hash=hashed_password)

        self.db.add(new_user)
        self.db.commit()

        return new_user

    def login(self, nickname: str, password: str) -> User:

        """Product returning logic"""

        user = self.db.query(User).filter_by(nickname=nickname).first()

        if not user:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist.')

        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong password.')

        access_token = self.jwt_repository.create_access_token(data={"sub": user.nickname})

        return {"access_token": access_token, "token_type": "bearer"}
