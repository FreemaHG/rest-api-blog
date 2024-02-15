from sqlalchemy import String, Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from src.database import Base
from src.models.blog import Blog


subscriptions = Table(
    'subscriptions',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('blog_id', Integer, ForeignKey('blog.id'))
)

class User(Base):
    """
    Модель для хранения данных о пользователе
    """

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(60), nullable=False, unique=True, index=True)
    blog: Mapped["Blog"] = relationship('Blog', backref=backref('user', uselist=False), cascade='all, delete')
    blogs = relationship('Blog', secondary=subscriptions, backref='followers')
