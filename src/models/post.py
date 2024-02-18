import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Post(Base):
    """
    Модель для хранения данных о записях блога
    """

    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    text: Mapped[str] = mapped_column(String(140))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    blog_id: Mapped[int] = mapped_column(ForeignKey("blog.id"))
    feeds = relationship('Feed', secondary='users_news_feed', back_populates='news')
