from datetime import timedelta
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth.pkg.jwt.repository import JWT_Repository
from fastapi_jwt_auth.pkg.db.repositories import UserManagementRepository
from fastapi_jwt_auth.pkg.db.database import get_db

from fastapi_jwt_auth.internal.routes.auth.schemas import (
    RegisterUserSchema,
    LoginUserSchema,
    RefreshTokenSchema,
    SecureEndpointSchemas
)

from fastapi_jwt_auth.internal.routes.auth.services import (
    check_token
)


router = APIRouter(
    prefix='/api/v1',
    tags=['Identity Management']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_service(db: Session = Depends(get_db)) -> UserManagementRepository:

    return UserManagementRepository(db)

@router.post('/register')
def registration(User: RegisterUserSchema, userRepository: UserManagementRepository = Depends(get_user_service)):

    '''Endpoint for User registration'''

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

    '''Endpoint for User loginning'''

    try:

        return userRepository.login(nickname_or_email=User.nickname_or_email, password=User.password)

    except HTTPException as e:

        return JSONResponse(
                    status_code=e.status_code,
                    content={
                        "error": e.detail
                    })

@router.post('/token')
def refresh_token(refresh_data: RefreshTokenSchema, jwt_repository: JWT_Repository = Depends(JWT_Repository)):

    access_token = jwt_repository.create_access_token(
                                    data={"sub": check_token(
                                                    repository=jwt_repository,
                                                    token=refresh_data,
                                                    token_type='refresh')},
                                    expires_delta=timedelta(minutes=15))

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": access_token,
                "token_type": "bearer"
            })


@router.post('/secure-endpoint')
def secure_endpoint(token: SecureEndpointSchemas, jwt_repository: JWT_Repository = Depends(JWT_Repository)):

    '''Security endpoint for check user's authorization by token'''

    check_token(
            repository=jwt_repository,
            token=token,
            token_type='access')

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "You have a correct token!"
            })
