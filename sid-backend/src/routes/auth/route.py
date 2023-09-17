from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings, get_settings
from src.database import get_session
from src.lib.hash import Hash
from src.routes.auth.schema import UserInput, Token
from src.routes.auth.service import get_user_by_email, get_user_by_username, create_new_user, create_access_token

auth_router = APIRouter()


@auth_router.post("/register", tags=["Authentication"])
async def register(user_input: UserInput, session: AsyncSession = Depends(get_session)):
    # check user if already in database
    user_email = await get_user_by_email(session, email=user_input.email)
    user_username = await get_user_by_username(session, username=user_input.username)

    if user_username or user_email:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": "user already registered"
            }
        )

    try:
        await create_new_user(session, user_input)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Operation Success"
            }
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
            "message": "something went wrong"
        })


@auth_router.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_session)],
        settings: Annotated[Settings, Depends(get_settings)]
):
    user = await get_user_by_username(session=session, username=form_data.username)

    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect username or password"},
            headers={"WWW-Authenticate": "Bearer"}
        )

    # check user password
    check_password = Hash().verify_password(form_data.password, user.password)

    if not check_password:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect username or password"},
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = await create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
        settings=settings
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"access_token": access_token, "token_type": "bearer"}
    )
