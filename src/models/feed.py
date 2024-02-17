from sqlalchemy import ForeignKey, Table, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


users_news_feed = Table(
    'users_news_feed',
    Base.metadata,
    Column('feed_id', Integer, ForeignKey('feed.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
    Column("read", Boolean, default=False),
)

class Feed(Base):
    """
    Модель для хранения данных о ленте новостей пользователя
    """

    __tablename__ = 'feed'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    news = relationship('Post', secondary=users_news_feed)
