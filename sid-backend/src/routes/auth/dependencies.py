from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from starlette import status

from src.routes.auth.oauth import oauth2_scheme
from src.routes.auth.schema import TokenData
from src.routes.auth.service import get_user_by_username
from src.config import Settings, get_settings
from src.database import get_session


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           settings: Annotated[Settings, Depends(get_settings)], session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(session=session, username=token_data.username)

    if user is None:
        raise credentials_exception

    return jsonable_encoder(user)



