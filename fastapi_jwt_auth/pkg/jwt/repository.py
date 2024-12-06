import jwt
from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status

from fastapi_jwt_auth.pkg.jwt.jwt_settings import SECRET_KEY, ALGORITHM, oauth2_scheme

from fastapi_jwt_auth.pkg.db.models import User

class JWT_Repository:

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):

        '''Creates access token'''

        to_encode = data.copy()

        if expires_delta:

            expire = datetime.utcnow() + expires_delta
        else:

            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encoded_access_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_access_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):

        '''Creates refresh token'''

        to_encode = data.copy()

        if expires_delta:

            expire = datetime.utcnow() + expires_delta

        else:

            expire = datetime.utcnow() + timedelta(days=1)

        to_encode.update({"exp": expire})

        encoded_refresh_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_refresh_jwt

    @staticmethod
    def verify_token(token: str):

        '''Validate refresh/access tokens'''

        try:

            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

            return payload

        except jwt.ExpiredSignatureError:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        except jwt.PyJWKError:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
