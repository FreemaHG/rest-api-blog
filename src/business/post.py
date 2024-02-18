from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.feed import users_news_feed


class PostBusiness:
    """
    Бизнес-логика по выводу последних 5 непрочитанных постов в ленте и пометке поста прочитанным
    """

    @classmethod
    async def mark_as_read(cls, feed_id: int, post_id: int, session: AsyncSession) -> None:
        """
        Отметить пост прочитанным
        :param feed_id: id ленты новостей
        :param post_id: id поста
        :param session: объект асинхронной сессии
        :return: None
        """

        query = update(users_news_feed)\
            .where(users_news_feed.c.feed_id == feed_id, users_news_feed.c.post_id == post_id)\
            .values(read=True)

        await session.execute(query)
        await session.commit()
