from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base
from .m2m import UsersCities

if TYPE_CHECKING:
    from .user import User


class City(Base):
    """
    Mодель города

    ## Attrs
        - id: int - идентификатор города
        - name: str - название города
        - users: List[User] - пользователи
            которые сделали запрос погоды в данном городе
    """

    __tablename__ = "city"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="responsed_cities",
        secondary=UsersCities.__table__,
    )

    def __repr__(self):
        return f"{self.name}"
