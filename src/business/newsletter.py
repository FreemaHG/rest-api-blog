from typing import List

from loguru import logger

from src.models.feed import Feed
from src.models.post import Post
from src.models.user import User


class Newsletter:
    """
    Рассылка последних новостей пользователям
    """

    __COUNT_NEWS = 5

    @classmethod
    async def __send(cls, recipient: User, news: Post) -> None:
        """
        Отправка получателю последних новостей
        :param recipient: получатель
        :param news: список новостей
        :return: None
        """
        news_to_send = list(reversed(news[:cls.__COUNT_NEWS]))

        logger.debug(f"Пользователь №{recipient.id} получил последних новостей: {len(news_to_send)}")

    @classmethod
    async def mailing(cls, mailing_list: List[Feed]) -> None:
        """
        Рассылка последних новостей из ленты
        :param mailing_list: список лент для рассылки новостей их пользователям
        :return: None
        """

        for recipients_feed in mailing_list:
            await cls.__send(recipient=recipients_feed.user, news=recipients_feed.news)
