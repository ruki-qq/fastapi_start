from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: Annotated[str, MinLen(1), MaxLen(30)]
    description: str
    price: int


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductCreate):
    pass

class ProductUpdatePartial(ProductCreate):
    name: Annotated[str, MinLen(1), MaxLen(30)] | None = None
    description: str | None = None
    price: int | None = None

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
