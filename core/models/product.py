from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
