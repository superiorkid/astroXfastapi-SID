from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_session
from src.models import User
from src.routes.auth.dependencies import get_current_user
from src.routes.auth.service import get_user_by_username

user_router = APIRouter()


@user_router.get("")
async def get_current_user_information(
        current_user: User = Depends(get_current_user)
):
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": "Operation success",
        "your information": current_user
    })


@user_router.get("/{username}")
@cache(expire=60)
async def get_user_information(username: str, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_username(session, username)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Operation success",
            "user information": jsonable_encoder(user)
        }
    )




