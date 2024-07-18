from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base
from .m2m import UsersCities

if TYPE_CHECKING:
    from .city import City


class User(Base):
    """
    Mодель пользователя

    ## Attrs:
        - id: int - идентификатор пользователя
        - usename: str - юзернейм пользователя
        - password: str - хэш пароля пользователя
        - responsed_cities: List[City] - города
            по которым пользователь делал запрос
    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    responsed_cities: Mapped[List["City"]] = relationship(
        "City",
        secondary=UsersCities.__table__,
        back_populates="users",
    )

    def __repr__(self):
        return f"{self.username} {self.email}"
