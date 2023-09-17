from fastapi.encoders import jsonable_encoder
from slugify import slugify
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Article, User


async def get_all_article(session: AsyncSession, per_page: int, skip: int):
    results = await session.execute(select(Article, User).join(User).offset(skip).limit(per_page).order_by(Article.publication_date.desc()))

    articles = []

    for article, user in results:
        temp = jsonable_encoder(article)
        temp["author"] = jsonable_encoder(user)

        articles.append(temp)

    return articles


async def create_new_article(title: str, content: str, cover: str, session: AsyncSession, user: User):
    current_user = User(**user)
    new_article = Article(
        title=title.lower(),
        slug=slugify(title),
        content=content,
        image=cover,
        user_id=current_user.dict().get("id")
    )

    session.add(new_article)
    await session.commit()
    await session.refresh(new_article)

    return new_article


async def get_article_by_slug(slug: str, session: AsyncSession) -> Article:
    try:
        query = await session.execute(select(Article, User).where(Article.slug == slug).join(User))
        row = jsonable_encoder(query.fetchone())

        article = row["Article"]
        article["author"] = row["User"]

        return article
    except Exception as e:
        return None


async def article_update(title: str, content: str, cover: str | None, session: AsyncSession, article: Article) -> Article:
    article.title = title
    article.content = content
    article.slug = slugify(title)
    if cover:
        article.image = cover

    session.add(article)
    await session.commit()
    await session.refresh(article)

    return article


async def total_article(session: AsyncSession) -> int:
    result = await session.execute(select(Article))
    total = len(result.scalars().all())
    return total


async def article_search(q: str, session: AsyncSession):
    result = await session.execute(select(Article).where(Article.title.like(f"%{q}%")))
    articles = result.scalars().all()
    return articles
