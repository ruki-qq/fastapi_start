from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None] = mapped_column(Text)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}), (user={self.user!r})"

    def __repr__(self):
        return str(self)
