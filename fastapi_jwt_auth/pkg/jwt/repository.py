import jwt
from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status

from fastapi_jwt_auth.pkg.jwt.jwt_settings import SECRET_KEY, ALGORITHM, oauth2_scheme

class JWT_Repository:

    def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):

        to_encode = data.copy()

        if expires_delta:

            expire = datetime.utcnow() + expires_delta
        else:

            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def verify_token(token: str):

        try:

            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

            return payload

        except jwt.ExpiredSignatureError:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        except jwt.PyJWKError:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


    def get_current_user(token: str = Depends(oauth2_scheme)):

        payload = verify_token(token)

        nickname: str = payload.get("sub")

        if nickname is None:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        return User(nickname=nickname)
