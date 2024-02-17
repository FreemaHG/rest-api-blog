from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.feed import Feed


class FeedRepository:
    """
    Создание ленты новостей для пользователя
    """

    @classmethod
    async def create(cls, user_id: int, session: AsyncSession) -> None:
        """
        Создание ленты новостей пользователя
        :param user_id: id пользователя
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """

        query = insert(Feed).values(user_id=user_id)

        await session.execute(query)
        await session.commit()

    @classmethod
    async def get(cls, user_id: int, session: AsyncSession) -> Feed | None:
        """
        Вывод ленты новостей пользователя
        :param user_id: id пользователя
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект ленты новостей, None, если не найдено
        """

        query = select(Feed).where(Feed.user_id == user_id)

        result = await session.execute(query)
        feed = result.unique().scalar_one_or_none()

        return feed
