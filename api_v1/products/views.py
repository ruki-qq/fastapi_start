from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from api_v1.products.schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)
from api_v1.products.dependencies import product_by_id
from core.models import db_helper

router_products = APIRouter(tags=["products"])


@router_products.get("", response_model=list[Product])
async def get_products_view(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router_products.post(
    "",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_view(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router_products.get("/{product_id}", response_model=Product)
async def get_product_view(product: Product = Depends(product_by_id)):
    return product


@router_products.put("/{product_id}", response_model=Product)
async def update_product_view(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update
    )


@router_products.patch("/{product_id}", response_model=Product)
async def update_product_partial_view(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )


@router_products.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_view(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
