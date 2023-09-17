from slugify import slugify
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Product, User


async def get_all_products(per_page: int, session: AsyncSession, skip: int):
    result = await session.execute(select(Product).offset(skip).limit(per_page).order_by(Product.created_at.desc()))
    products = result.scalars().all()
    return products


async def total_product(session):
    result = await session.execute(select(Product))
    total = len(result.scalars().all())
    return total


async def get_product_by_id(id: int, session: AsyncSession):
    result = await session.execute(select(Product).where(Product.id == id))
    product = result.scalars().first()
    return product


async def get_product_by_slug(slug: str, session: AsyncSession) -> Product:
    result = await session.execute(select(Product).where(Product.slug == slug))
    product = result.scalars().first()

    return product


async def create_new_product(
        description: str,
        filename: str,
        name: str,
        price: float,
        stock: int,
        session: AsyncSession,
        user=User
):
    current_user = Product(**user)
    new_product = Product(
        name=name,
        slug=slugify(name),
        price=price,
        stock=stock,
        image=filename,
        description=description,
        user_id=current_user.dict().get("id")
    )

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


async def product_update(
        description: str,
        image_path: str,
        name: str,
        price: float,
        product: Product,
        session: AsyncSession,
        stock: int
):
    product.name = name
    product.slug = slugify(name)
    product.price = price
    product.stock = stock
    product.description = description
    product.image = image_path

    session.add(product)
    await session.commit()
    await session.refresh(product)

    return product


async def product_search(q: str, session: AsyncSession):
    result = await session.execute(select(Product).where(Product.name.like(f"%{q}%")))
    products = result.scalars().all()
    return products
