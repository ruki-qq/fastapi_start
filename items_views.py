from fastapi import APIRouter
from pydantic import PositiveInt

router_items = APIRouter(prefix="/items")


@router_items.get("")
async def items():
    return ["item1", "item2"]


@router_items.get("/latest")
async def get_latest_item():
    return {"item": {"id": 0, "name": "last"}}


@router_items.get("/{item_id}")
async def get_item(item_id: PositiveInt):
    return {"id": item_id}
