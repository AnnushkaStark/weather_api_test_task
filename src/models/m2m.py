from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from databases.database import Base


class UsersCities(Base):
    """
    m2m Модель Города пользователя

    ## Attrs:
        -city_id: int - идентификатор города
        - user_id: int -идентификатор пользователя
    """

    __tablename__ = "users_cities"
    __table_args__ = (
        UniqueConstraint("city_id", "user_id", name="uix_city_user"),
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
