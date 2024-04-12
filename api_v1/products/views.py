from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from api_v1.products.schemas import Product, ProductCreate
from core.models import db_helper

router_products = APIRouter(tags=["products"])


@router_products.get("", response_model=list[Product])
async def get_products_view(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_products(session=session)


@router_products.post("", response_model=Product)
async def create_product_view(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router_products.get(
    "/{product_id}",
)
async def get_product_view(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    product = await crud.get_product(session=session, product_id=product_id)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found.",
    )
