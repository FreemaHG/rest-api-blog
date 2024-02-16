from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.post import Post


class Blog(Base):
    """
    Модель для хранения данных о блоге пользователя
    """

    __tablename__ = 'blog'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    posts: Mapped[List["Post"]] = relationship(backref='blog', cascade='all, delete-orphan')
