from fastapi import APIRouter

from users.crud import create_user
from users.schemas import CreateUser

router_users = APIRouter(prefix="/users")


@router_users.post("")
async def create_user_view(user: CreateUser):
    return await create_user(user)
