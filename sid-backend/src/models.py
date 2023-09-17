from datetime import datetime
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    username: str = Field(min_length=3, unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str = Field(min_length=6)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    articles: List["Article"] = Relationship(back_populates="user")
    products: List["Product"] = Relationship(back_populates="user")


class Article(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    title: str = Field(min_length=5, max_length=255)
    slug: str = Field(unique=True, index=True)
    content: str = Field(nullable=False)
    image: str = Field(nullable=False)
    publication_date: datetime = Field(default=datetime.utcnow(), nullable=False)
    last_modified: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="articles")


class Product(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    slug: str = Field(unique=True, index=True)
    price: float = Field(nullable=False)
    stock: int = Field(nullable=False)
    image: str = Field(nullable=False)
    description: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="products")
