from loguru import logger
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.news_feed import NewsFeedBusiness
from src.business.newsletter import Newsletter
from src.business.post import PostBusiness
from src.repositories.feed import FeedRepository, FeedListRepository


class FeedService:
    """
    Вывод новостей в ленту пользователя
    """

    @classmethod
    async def get_list(cls, user_id: int, session: AsyncSession) -> Select | bool:
        """
        Вывод новостей пользователя в ленту
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: новости ленты
        """

        feed = await FeedRepository.get(user_id=user_id, session=session)

        if not feed:
            return False

        query = await NewsFeedBusiness.query_for_get_news(feed=feed)

        return query

    @classmethod
    async def get_last_news(cls) -> None:
        """
        Рассылка пользователям последних новостей из ленты
        :return: None
        """

        mailing_list = await FeedListRepository.get_list()

        if mailing_list:
            await Newsletter.mailing(mailing_list=mailing_list)
        else:
            logger.warning("Нет пользователей для рассылки")

    @classmethod
    async def read(cls,  user_id: int, post_id: int, session: AsyncSession) -> bool:
        """
        Отметить пост в ленте пользователя прочитанным
        :param user_id: id пользователя
        :param post_id: id поста
        :param session: объект асинхронной сессии
        :return: True при отметке прочитанным, иначе False
        """

        feed = await FeedRepository.get(user_id=user_id, session=session)

        if not feed:
            return False

        await PostBusiness.mark_as_read(feed_id=feed.id, post_id=post_id, session=session)

        return True
