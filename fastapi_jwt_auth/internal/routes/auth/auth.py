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

def get_product_service(db: Session = Depends(get_db)) -> UserManagementRepository:

    return UserManagementRepository(db)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from fastapi_jwt_auth.internal.routes.auth.schemas import (
    RegisterUserSchema
)


@router.post('/register')
def registration(User: RegisterUserSchema, userRepository: UserManagementRepository = Depends(get_product_service)):

    try:

        new_user = userRepository.register(nickname=User.nickname, email=User.email, password=User.password)

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
def login():

    pass

@router.post('/token')
def refresh_token():

    pass