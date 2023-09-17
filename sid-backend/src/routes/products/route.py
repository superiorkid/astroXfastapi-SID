import os
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache
from slugify import slugify
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.database import get_session
from src.lib.image import check_file_size, check_content_type, save_image
from src.routes.auth.dependencies import get_current_user
from src.routes.products.service import get_all_products, total_product, get_product_by_id, get_product_by_slug, \
    create_new_product, product_update, product_search

product_router = APIRouter()


@product_router.get('')
async def get_products(
        session: AsyncSession = Depends(get_session),
        page: int = 1
):
    per_page: int = 15
    skip: int = (page - 1) * per_page

    # get articles
    products = await get_all_products(per_page, session, skip)
    total = await total_product(session)

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": "Operation success",
        "data": jsonable_encoder(products),
        "pagination": {
            "page": page,
            "per_page": len(products),
            "total_pages": total,
            "next": f"/api/product?page={page + 1}",
            "previous": None if page <= 1 else f"/api/product?page={page - 1}"
        }
    })


@product_router.post('')
async def create_product(
        name: Annotated[str, Form()],
        price: Annotated[float, Form()],
        stock: Annotated[int, Form()],
        description: Annotated[str, Form()],
        image: UploadFile,
        session: AsyncSession = Depends(get_session),
        current_user=Depends(get_current_user)
):
    product = await get_product_by_slug(slug=slugify(name), session=session)

    if product:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
            "message": "product already exists."
        })

    if not check_file_size(image.file.tell()):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": 'File to large'
        })

    if not check_content_type(image.content_type):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "invalid file type"})

    await save_image(image, destination="uploads/assets/products/")

    try:
        filename: str = image.filename
        await create_new_product(description, filename, name, price, stock, session, user=current_user)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Operation success"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
            "message": "something went wrong"
        })


@product_router.get("/search")
async def search_product(q: Optional[str] = None, session: AsyncSession = Depends(get_session)):
    products = await product_search(q, session)

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": f"Search result for `{q}`",
        "data": jsonable_encoder(products)
    })


@product_router.get('/{id}')
@cache(expire=60)
async def get_product(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    product = await get_product_by_id(id, session)

    if not product:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": "article not found"
        })

    return product


@product_router.put('/{slug}')
async def update_product(
        slug: str,
        name: Optional[str] = Form(None),
        price: Optional[float] = Form(None),
        stock: Optional[int] = Form(None),
        description: Optional[str] = Form(None),
        image: Optional[UploadFile] = None,
        session: AsyncSession = Depends(get_session),
        current_user=Depends(get_current_user)
):
    product = await get_product_by_slug(slug, session)

    if not product:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": "product not found"
        })

    if image:
        if not check_file_size(image.file.tell()):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "file to large"})

        if not check_content_type(image.content_type):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "invalid file type"})

        os.remove(product.image)

    image_path = await save_image(image) if image else None

    try:
        await product_update(description, image_path, name, price, product, session, stock)

        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Operation success"
        })
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
                "message": "something went wrong"
            }
        )


@product_router.delete('/{slug}')
async def delete_product(slug: str, session: AsyncSession = Depends(get_session),
                         current_user=Depends(get_current_user)):
    product = await get_product_by_slug(slug, session)

    if not product:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": "product not found"
        })

    os.remove(product.image)

    await session.delete(product)
    await session.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "delete operation successfully"
        }
    )
