
from sqlalchemy import update, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.user import User
from src.schemas.user import UserInSchema, UserInOptionalSchema


class UserCrudRepository:
    """
    CRUD операции для пользователя
    """

    @classmethod
    async def create(cls, new_user: UserInSchema, session: AsyncSession) -> User:
        """
        Создание нового пользователя
        :param new_user: данные нового пользователя
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект нового пользователя
        """

        query = insert(User).values(username=new_user.username).returning(User)
        result = await session.execute(query)
        await session.commit()

        return result.scalar()

    @classmethod
    async def get(cls, user_id: int, session: AsyncSession) -> User | None:
        """
        Возврат пользователя по id
        :param user_id: id пользователя
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект пользователя, если найден, иначе None
        """

        query = (
            select(User)
            .options(joinedload(User.blogs))
            .options(joinedload(User.blog))
            .where(User.id == user_id)
        )
        result = await session.execute(query)
        user = result.unique().scalar_one_or_none()

        return user

    @classmethod
    async def update(cls, user_id: int, data: UserInOptionalSchema, session: AsyncSession) -> User | None:
        """
        Обновление пользователя по id
        :param user_id: id пользователя
        :param data: новые данные пользователя
        :param session: объект асинхронной сессии для запросов к БД
        :return: обновленный объект пользователя, если найден, иначе None
        """

        query = (
            update(User)
            .where(User.id == user_id)
            .values(data.model_dump(exclude_unset=True))
            .returning(User)
        )
        result = await session.execute(query)
        await session.commit()

        return result.scalar()

    @classmethod
    async def delete(cls, delete_user: User, session: AsyncSession) -> None:
        """
        Удаление пользователя
        :param delete_user: удаляемый пользователь
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """

        await session.delete(delete_user)
        await session.commit()
