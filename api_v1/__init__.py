from fastapi import APIRouter

from .products.views import router_products

router_v1 = APIRouter()
router_v1.include_router(router_products, prefix="/products")
