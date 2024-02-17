from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.post import Post
from src.schemas.post import PostInSchema, PostInOptionalSchema


class PostCrudRepository:
    """
    CRUD операции для постов
    """

    @classmethod
    async def create(cls, blog_id: int, new_post: PostInSchema, session: AsyncSession) -> Post:
        """
        Создание нового поста
        :param blog_id: id блога для добавления поста
        :param new_post: данные нового поста
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект нового поста
        """

        query = insert(Post).values(
            title=new_post.title,
            text=new_post.text,
            blog_id=blog_id
        ).returning(Post)

        result = await session.execute(query)
        await session.commit()

        return result.scalar()

    @classmethod
    async def get(cls, post_id: int, session: AsyncSession) -> Post | None:
        """
        Возврат поста по id
        :param post_id: id поста
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект поста, если найден, иначе None
        """

        query = select(Post).where(Post.id == post_id)

        result = await session.execute(query)
        user = result.unique().scalar_one_or_none()

        return user

    @classmethod
    async def update(cls, post_id: int, data: PostInOptionalSchema, session: AsyncSession) -> Post | None:
        """
        Обновление поста по id
        :param post_id: id поста
        :param data: новые данные поста
        :param session: объект асинхронной сессии для запросов к БД
        :return: обновленный объект поста, если найден, иначе None
        """

        query = update(Post).where(Post.id == post_id).values(data.model_dump(exclude_unset=True)).returning(Post)

        result = await session.execute(query)
        await session.commit()

        updated_user = result.scalar()

        return updated_user

    @classmethod
    async def delete(cls, delete_post: Post, session: AsyncSession) -> None:
        """
        Удаление поста
        :param delete_post: удаляемый пост
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """

        await session.delete(delete_post)
        await session.commit()


class PostListRepository:
    """
    Операции над списками постов
    """

    @classmethod
    async def get_list(cls, blog_id: int, session: AsyncSession) -> List[Post] | None:
        """
        Вывод списка постов по id блога
        :param blog_id: id блога
        :param session: объект асинхронной сессии для запросов к БД
        :return: список постов иначе None
        """

        query = select(Post).where(Post.blog_id == blog_id)

        result = await session.execute(query)
        posts = result.unique().scalars().all()

        return list(posts)
