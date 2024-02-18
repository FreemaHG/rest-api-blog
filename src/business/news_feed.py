from typing import List

from loguru import logger
from sqlalchemy import select, update, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import async_session_maker, get_async_session
from src.models.feed import Feed, users_news_feed
from src.models.post import Post
from src.models.user import subscriptions
from src.repositories.post import PostCrudRepository


class NewsFeedBusiness:
    """
    Бизнес-логика по добавлению, выводу и отметке поста прочитанным в ленте пользователя
    """

    @classmethod
    async def __search_feeds(cls, blog_id: int, session: AsyncSession) -> List[Feed] | None:
        """
        Поиск новостных лент пользователей, подписанных на указанный блог
        :param blog_id: id блога
        :param session: объект асинхронной сессии
        :return: список лент пользователей
        """

        # id подписчиков блога, куда был добавлен пост
        subquery = select(subscriptions.c.user_id).where(subscriptions.c.blog_id == blog_id)
        # id лент для добавления новости
        query = select(Feed).options(joinedload(Feed.news)).filter(Feed.user_id.in_(subquery))

        result = await session.execute(query)
        feeds_list = result.unique().scalars().all()

        return list(feeds_list)

    @classmethod
    async def add_new(cls, blog_id: int, post_id: int) -> None:
        """
        Добавление новости в ленту подписчикам
        :param blog_id: id блога, куда была добавлена новость
        :param post_id: id нового поста
        :return: None
        """
        logger.debug("Запуск процесса обновления лент подписчиков")

        async with async_session_maker() as session:

            post = await PostCrudRepository.get(post_id=post_id, session=session)

            feeds_list = await cls.__search_feeds(blog_id=blog_id, session=session)
            logger.debug(f"Пост №{post.id} требует добавления в {len(feeds_list)} новостные ленты")

            for feed in feeds_list:
                feed.news.append(post)

            await session.commit()
            logger.info(f"Все ленты подписчиков обновлены")

    @classmethod
    async def query_for_get_news(cls, feed: Feed) -> Select:
        """
        Возврат select-запроса на извлечение непрочитанных постов в ленту пользователя (для пагинатора в роуте)
        :param feed: объект ленты
        :return: select-запрос к БД
        """
        subquery = select(users_news_feed.c.post_id)\
            .where(users_news_feed.c.feed_id == feed.id, users_news_feed.c.read == False)

        query = select(Post).where(Post.id.in_(subquery)).order_by(Post.created_at.desc()).limit(500)

        return query

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
