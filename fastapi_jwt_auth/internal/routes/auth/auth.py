from datetime import timedelta
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status
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
    LoginUserSchema,
    RefreshTokenSchema,
    SecureEndpointSchemas
)

from fastapi_jwt_auth.pkg.jwt.repository import JWT_Repository

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
def refresh_token(refresh_data: RefreshTokenSchema, jwt_repository: JWT_Repository = Depends(JWT_Repository)):

    try:

        payload = jwt_repository.verify_token(refresh_data.refresh_token)

        nickname = payload.get('sub')

        if not nickname:

            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid refresh token.')

    except HTTPException as e:

        raise e

    except Exception:

        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid refresh token.')

    access_token = jwt_repository.create_access_token(
                                    data={"sub": nickname},
                                    expires_delta=timedelta(minutes=15))

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": access_token,
                "token_type": "bearer"
            })


@router.post('/secure-endpoint')
def secure_endpoint(token: SecureEndpointSchemas, jwt_repository: JWT_Repository = Depends(JWT_Repository)):

    try:

        payload = jwt_repository.verify_token(token.access_token)

        nickname = payload.get('sub')

        if not nickname:

            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid access token.')

    except HTTPException as e:

        raise e

    except Exception:

        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid access token.')

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "You have a correct token!"
            })
