import bcrypt

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

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

    def login(self, nickname_or_email: str, password: str) -> JSONResponse:

        """User login logic"""

        try:

            user = self.db.query(User).filter_by(nickname=nickname_or_email).first()

            if not user:

                user = self.db.query(User).filter_by(email=nickname_or_email).first()


                if not user: raise HTTPException(detail='User does not exist.')

        except:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User does not exist.')

        
        if isinstance(user.password_hash, str):

            password_hash_bytes = bytes.fromhex(user.password_hash[2:])

        else:

            password_hash_bytes = user.password_hash

        if not bcrypt.checkpw(password.encode('utf-8'), password_hash_bytes):

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong password.')

        access_token = self.jwt_repository.create_access_token(data={"sub": user.nickname})

        return JSONResponse(
                    status_code=200,
                    content={
                        "token": {
                                "access_token": access_token,
                                "token_type": "bearer"
                                },
                        "user": {
                            "id": user.id,
                            "nickname": user.nickname,
                            "email": user.email
                            }
                        }
                    )
