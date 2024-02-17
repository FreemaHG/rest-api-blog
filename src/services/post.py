from typing import List

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.news_feed import NewsFeedBusiness
from src.models.post import Post
from src.repositories.blog import BlogRepository
from src.repositories.post import PostCrudRepository, PostListRepository
from src.schemas.post import PostInSchema, PostInOptionalSchema


class PostService:
    """
    Создание, вывод, обновление и удаление постов
    """

    @classmethod
    async def create(cls, blog_id: int, new_post: PostInSchema, session: AsyncSession) -> Post:
        """
        Создание нового поста
        :param blog_id: id блога
        :param new_post: данные нового поста
        :param session: объект асинхронной сессии
        :return: новый пост
        """

        post = await PostCrudRepository.create(blog_id=blog_id, new_post=new_post, session=session)

        # TODO Вынести в фон через Celery
        await NewsFeedBusiness.add_new(blog_id=blog_id, post=post, session=session)

        return post

    @classmethod
    async def get(cls, post_id: int, session: AsyncSession) -> Post | None:
        """
        Возврат поста по id
        :param post_id: id поста
        :param session: объект асинхронной сессии
        :return: объект поста, если найден, иначе None
        """

        post = await PostCrudRepository.get(post_id=post_id, session=session)

        return post

    @classmethod
    async def update(cls, post_id: int, data: PostInOptionalSchema, session: AsyncSession) -> Post | None:
        """
        Обновление поста
        :param post_id: id поста
        :param data: новые данные поста
        :param session: объект асинхронной сессии
        :return: обновленный пост
        """

        updated_post = await PostCrudRepository.update(post_id=post_id, data=data, session=session)

        return updated_post

    @classmethod
    async def delete(cls, post_id: int, session: AsyncSession) -> bool:
        """
        Удаление поста по id
        :param post_id: id поста
        :param session: объект асинхронной сессии
        :return: True, если удален, иначе False
        """

        delete_post = await PostCrudRepository.get(post_id=post_id, session=session)

        if delete_post:
            await PostCrudRepository.delete(delete_post=delete_post, session=session)
            return True

        logger.error('Пост не найдено!')
        return False


class PostListService:
    """
    Вывод списка постов
    """

    @classmethod
    async def get_list(cls, blog_id: int, session: AsyncSession) -> List[Post] | bool:
        """
        Возврат списка постов в блоге
        :param blog_id: id блога
        :param session: объект асинхронной сессии
        :return: список постов иначе False, если блог не найден
        """
        blog = await BlogRepository.get(blog_id=blog_id, session=session)

        if not blog:
            return False

        posts = await PostListRepository.get_list(blog_id=blog.id, session=session)

        return posts
