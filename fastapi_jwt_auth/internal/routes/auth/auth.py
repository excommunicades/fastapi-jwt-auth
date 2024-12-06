from passlib.context import CryptContext

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/api/v1',
    tags=['Identity Management']
)

from fastapi_jwt_auth.pkg.db.repositories import UserManagementRepository
from fastapi_jwt_auth.pkg.db.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from fastapi_jwt_auth.internal.routes.auth.schemas import (
    RegisterUserSchema,
    LoginUserSchema
)

def get_user_service(db: Session = Depends(get_db)) -> UserManagementRepository:

    return UserManagementRepository(db)

@router.post('/register')
def registration(User: RegisterUserSchema, userRepository: UserManagementRepository = Depends(get_user_service)):

    try:

        userRepository.register(nickname=User.nickname, email=User.email, password=User.password)

        return JSONResponse(
                    status_code=201,
                    content={
                        "message": "You were registered successfully!"
                    })

    except HTTPException as e:

        return JSONResponse(
                    status_code=e.status_code,
                    content={
                        "error": e.detail
                    })

@router.post('/login')
def login(User: LoginUserSchema, userRepository: UserManagementRepository = Depends(get_user_service)):

    try:

        return userRepository.login(nickname_or_email=User.nickname_or_email, password=User.password)

    except HTTPException as e:

        return JSONResponse(
                    status_code=e.status_code,
                    content={
                        "error": e.detail
                    })






@router.post('/token')
def refresh_token():

    pass