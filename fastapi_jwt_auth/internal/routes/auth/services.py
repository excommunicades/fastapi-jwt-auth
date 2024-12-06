from fastapi import HTTPException, status

def check_token(repository, token, token_type):

    '''Checks refresh/access token'''

    if token_type == 'refresh':

        try:

            payload = repository.verify_token(token.refresh_token)

            nickname = payload.get('sub')

            if not nickname:

                raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Invalid refresh token.')

            return nickname

        except HTTPException as e:

            raise e

        except Exception:

            raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Invalid refresh token.')

    else:

        try:

            payload = repository.verify_token(token.access_token)

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
