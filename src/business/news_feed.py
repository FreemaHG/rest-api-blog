from typing import List

from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.feed import Feed, users_news_feed
from src.models.post import Post
from src.models.user import subscriptions


class NewsFeedBusiness:
    """
    Бизнес-логика по добавлению, выводу и отметке поста прочитанным в ленте пользователя
    """

    @classmethod
    async def add_new(cls, blog_id: int, post: Post, session: AsyncSession) -> None:
        """
        Добавление новости в ленту подписчикам
        :param blog_id: id блога, куда была добавлена новость
        :param post: новый пост
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug("Запуск процесса обновления лент подписчиков")

        # id подписчиков блога, куда был добавлен пост
        subquery = select(subscriptions.c.user_id).where(subscriptions.c.blog_id==blog_id)
        # id лент для добавления новости
        query = select(Feed).options(joinedload(Feed.news)).filter(Feed.user_id.in_(subquery))

        result = await session.execute(query)
        feeds_list = result.unique().scalars().all()
        logger.debug(f"Пост №{post.id} требует добавления в {len(feeds_list)} лент")

        for feed in feeds_list:
            feed.news.append(post)

            # TODO Проверить!!!
            # Ограничение в 500 записей в ленте пользователя
            if len(feed.news) > 500:
                feed.news = feed.news[:500]

        await session.commit()
        logger.info(f"Все ленты подписчиков обновлены")

    @classmethod
    async def get_news(cls, feed: Feed, session: AsyncSession) -> List[Post] | None:
        """
        Вывод непрочитанных постов в ленту пользователя
        :param feed: объект ленты
        :param session: объект асинхронной сессии
        :return: список непрочитанных постов
        """
        subquery = select(users_news_feed.c.post_id)\
            .where(users_news_feed.c.feed_id == feed.id, users_news_feed.c.read == False)

        query = select(Post).where(Post.id.in_(subquery))

        result = await session.execute(query)
        posts = result.unique().scalars().all()

        return list(posts)

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
