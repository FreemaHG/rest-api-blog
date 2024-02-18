from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.blog import BlogRepository
from src.repositories.subscribe import SubscribeRepository
from src.repositories.user import UserCrudRepository


class SubscribeService:
    """
    Подписка и отписка на блоги
    """

    __USER_NOT_FOUND = 'User not found'
    __BLOG_NOT_FOUND = 'Blog not found'

    @classmethod
    async def create(cls, user_id: int, blog_id: int, session: AsyncSession) -> str | bool:
        """
        Подписка на блог
        :param user_id: id пользователя
        :param blog_id: id блога
        :param session: объект асинхронной сессии
        :return: сообщение об ошибке, иначе True
        """

        user = await UserCrudRepository.get(user_id=user_id, session=session)
        blog = await BlogRepository.get(blog_id=blog_id, session=session)

        if not user:
            return cls.__USER_NOT_FOUND

        elif not blog:
            return cls.__BLOG_NOT_FOUND

        elif user.blog.id == blog_id:
            return 'you can\'t subscribe to your blog'

        elif blog in user.blogs:
            return 'The subscription has already been issued'

        else:
            await SubscribeRepository.create(user=user, blog=blog, session=session)

            return True

    @classmethod
    async def delete(cls, user_id: int, blog_id: int, session: AsyncSession) -> str | bool:
        """
        Описка от блога
        :param user_id: id пользователя
        :param blog_id: id блога
        :param session: объект асинхронной сессии
        :return: сообщение об ошибке, иначе True
        """

        user = await UserCrudRepository.get(user_id=user_id, session=session)
        blog = await BlogRepository.get(blog_id=blog_id, session=session)

        if not user:
            return cls.__USER_NOT_FOUND

        elif not blog:
            return cls.__BLOG_NOT_FOUND

        elif user.blog.id == blog_id:
            return 'You cannot unsubscribe from your blog'

        elif blog not in user.blogs:
            return 'The subscription has not been issued'

        else:
            await SubscribeRepository.delete(user=user, blog=blog, session=session)

            return True
