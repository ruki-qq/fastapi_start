from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from core.models import Order, OrderProductAssociation


class Product(Base):
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="products",
    # )
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
