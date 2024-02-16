from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.user import UserCrudRepository
from src.schemas.user import UserInSchema, UserInOptionalSchema


class UserService:
    """
    Создание, вывод, обновление и удаление пользователей
    """

    @classmethod
    async def create(cls, new_user: UserInSchema, session: AsyncSession) -> User:
        """
        Создание пользователя, блога и персональной ленты
        :param new_user: данные нового пользователя
        :param session: объект асинхронной сессии
        :return: новый пользователь
        """
        user = await UserCrudRepository.create(new_user=new_user, session=session)

        # TODO Обернуть в одну транзакцию!!!
        # TODO Создать блог
        # TODO Создать персональную ленту

        return user

    @classmethod
    async def get(cls, user_id: int, session: AsyncSession) -> User | None:
        """
        Возврат пользователя по id
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: объект пользователя, если найден, иначе None
        """

        user = await UserCrudRepository.get(user_id=user_id, session=session)

        return user

    @classmethod
    async def update(cls, user_id: int, data: UserInOptionalSchema, session: AsyncSession) -> User | None:
        """
        Обновление пользователя
        :param user_id: id пользователя
        :param data: новые данные пользователя
        :param session: объект асинхронной сессии
        :return: обновленный пользователь
        """

        updated_user = await UserCrudRepository.update(user_id=user_id, data=data, session=session)

        return updated_user

    @classmethod
    async def delete(cls, user_id: int, session: AsyncSession) -> bool:
        """
        Удаление пользователя по id
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: True, если удален, иначе False
        """

        delete_user = await UserCrudRepository.get(user_id=user_id, session=session)

        if delete_user:
            await UserCrudRepository.delete(delete_user=delete_user, session=session)

            return True

        logger.error('Меню не найдено!')
        return False
