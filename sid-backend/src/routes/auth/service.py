from datetime import timedelta, datetime

from jose import jwt
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.routes.auth.schema import UserInput
from src.config import Settings
from src.lib.hash import Hash
from src.models import User


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    return user


async def create_new_user(session: AsyncSession, user_input: UserInput):
    password_hash = Hash().get_password_hash(user_input.password)
    new_user = User(
        username=user_input.username,
        email=user_input.email,
        password=password_hash
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def create_access_token(settings: Settings, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
