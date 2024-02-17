from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.blog import Blog


class BlogRepository:
    """
    Создание блога
    """

    @classmethod
    async def create(cls, user_id: int, session: AsyncSession) -> None:
        """
        Создание блога пользователя
        :param user_id: id автора блога
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """

        query = insert(Blog).values(user_id=user_id)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def get(cls, blog_id: int, session: AsyncSession) -> Blog | None:
        """
        Создание блога пользователя
        :param blog_id: id блога
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект блога, если найден, иначе None
        """

        query = (
            select(Blog)
            .options(joinedload(Blog.posts))
            .where(Blog.id == blog_id)
        )
        result = await session.execute(query)
        blog = result.unique().scalar_one_or_none()

        return blog
