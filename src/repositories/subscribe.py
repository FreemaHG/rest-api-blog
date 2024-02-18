from sqlalchemy.ext.asyncio import AsyncSession

from src.models.blog import Blog
from src.models.user import User


class SubscribeRepository:
    """
    Создание и удаление подписки на блог
    """

    @classmethod
    async def create(cls, user: User, blog: Blog, session: AsyncSession) -> None:
        """
        Подписка на блог
        :param user: объект пользователя
        :param blog: объект блога
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        user.blogs.append(blog)
        await session.commit()

    @classmethod
    async def delete(cls, user: User, blog: Blog, session: AsyncSession) -> None:
        """
        Удаление подписки на блог
        :param user: объект пользователя
        :param blog: объект блога
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        user.blogs.remove(blog)
        await session.commit()
