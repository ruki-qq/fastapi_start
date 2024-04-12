from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.models import Base, db_helper
from items_views import router_items
from users.views import router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_items, tags=["items"])
app.include_router(router_users, tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/hello")
async def hello(name: str = "Weol"):
    name = name.strip().title()
    return {"message": f"Hello {name}"}


@app.post("/calc/add")
async def add(a: int, b: int):
    return {"result": a + b}
