import os
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from slugify import slugify
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_session
from src.lib.image import check_file_size, check_content_type, save_image
from src.models import Article, User
from src.routes.auth.dependencies import get_current_user
from src.routes.blogs.service import get_all_article, get_article_by_slug, total_article, article_update, \
    create_new_article, article_search

blog_router = APIRouter()


@blog_router.get("")
async def get_articles(
        session: AsyncSession = Depends(get_session),
        page: int = 1
):
    per_page: int = 7
    skip: int = (page - 1) * per_page

    articles = await get_all_article(session, per_page, skip)
    total = await total_article(session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Operation success",
            "data": jsonable_encoder(articles),
            "pagination": {
                "page": page,
                "per_page": len(articles),
                "total_pages": total,
                "next": f"/api/blog?page={page + 1}",
                "previous": None if page <= 1 else f"/api/blog?page={page - 1}"
            }
        }
    )


@blog_router.post("", description="create new article")
async def create_article(
        title: Annotated[str, Form()],
        content: Annotated[str, Form()],
        cover: UploadFile,
        session: AsyncSession = Depends(get_session),
        current_user=Depends(get_current_user)
):
    article = await get_article_by_slug(slug=slugify(title), session=session)

    if article:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "article already exists"})

    if not check_file_size(cover.file.tell()):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "file to large"})

    if not check_content_type(cover.content_type):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "invalid file type"})

    await save_image(cover, destination='uploads/assets/blogs/')

    try:
        await create_new_article(title=title, content=content, cover=cover.filename, session=session, user=current_user)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Operation success"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
            "message": "something went wrong"
        })


@blog_router.get("/search")
async def search_article(q: Optional[str] = None, session: AsyncSession = Depends(get_session)):
    articles = await article_search(q, session)

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": f"Result for `{q}`",
        "data": jsonable_encoder(articles)
    })


@blog_router.get('/{slug}')
@cache(expire=60)
async def get_article(
        slug: str,
        session: AsyncSession = Depends(get_session),
):
    try:
        article = await get_article_by_slug(slug, session)

        if not article:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": "article not found"
                }
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Operation success",
                "data": jsonable_encoder(article)
            }
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "something went wrong"
            }
        )


@blog_router.put("/{slug}")
async def update_article(
        title: Annotated[str, Form()],
        content: Annotated[str, Form()],
        slug: str, cover: Optional[UploadFile] = None,
        session: AsyncSession = Depends(get_session),
        current_user=Depends(get_current_user)
):
    article = await get_article_by_slug(slug, session)

    if not article:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "article not found"
            }
        )

    if cover:
        if not check_file_size(cover.file.tell()):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "file to large"})

        if not check_content_type(cover.content_type):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "invalid file type"})

        os.remove(article.image)

    cover_path = await save_image(cover) if cover else None

    try:
        await article_update(title=title, content=content, cover=cover_path, session=session, article=article)

        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Operation success"
        })
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "something went wrong"
            }
        )


@blog_router.delete("/{slug}")
async def delete_article(slug: str, session: AsyncSession = Depends(get_session),
                         current_user=Depends(get_current_user)):
    article = await get_article_by_slug(slug, session)

    if not article:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "article not found"
            }
        )

    os.remove(article.image)

    await session.delete(article)
    await session.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Delete Operation successfully"
        }
    )
