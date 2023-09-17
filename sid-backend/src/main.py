from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.staticfiles import StaticFiles

from src.routes.auth.route import auth_router
from src.routes.blogs.route import blog_router
from src.routes.products.route import product_router
from src.routes.user.route import user_router

app = FastAPI(
    title="Sistem informasi desa API",
    version="1.0",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian"
    }
)

# origins = [
#     "http://localhost",
#     "http://localhost:4321",
#     "http://127.0.0.1",
#     "http://127.0.0.1:4321",
#     "http://0.0.0.0",
#     "http://0.0.0.0:4321",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.mount('/img/blog', StaticFiles(directory="uploads/assets/blogs"), name="blog")
app.mount('/img/product', StaticFiles(directory="uploads/assets/products"), name="product")


app.include_router(auth_router)
app.include_router(blog_router, prefix="/api/blog", tags=["Blog"])
app.include_router(product_router, prefix="/api/product", tags=["Produk desa"])
app.include_router(user_router, prefix="/api/profile", tags=["User"])


@app.get("/")
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": "Sistem Informasi Desa API v1.0"
    })
