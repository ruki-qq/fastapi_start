from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_v1 import router_v1
from core.settings import settings
from users.views import router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
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
