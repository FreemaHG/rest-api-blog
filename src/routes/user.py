from http import HTTPStatus
from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.base import BlogAPIRouter
from src.schemas.response import ResponseSchema
from src.schemas.user import UserInSchema, UserOutSchema, UserInOptionalSchema
from src.services.user import UserService
from src.utils.exceptions import CustomApiException

router = BlogAPIRouter(tags=['user'])


@router.post(
    '/users',
    response_model=UserOutSchema,
    responses={
        201: {'model': UserOutSchema},
    },
    status_code=201,
)
async def create_user(
    new_user: UserInSchema,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для добавления нового пользователя
    """

    user = await UserService.create(new_user=new_user, session=session)

    return user

@router.get(
    '/users/{user_id}',
    response_model=Union[UserOutSchema, ResponseSchema],
    responses={
        200: {'model': UserOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода пользователя по id
    """

    user = await UserService.get(user_id=user_id, session=session)

    if not user:
        raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail='user not found')

    return user

@router.patch(
    '/{user_id}',
    response_model=Union[UserOutSchema, ResponseSchema],
    responses={
        200: {'model': UserOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def update_user(
    user_id: int,
    data: UserInOptionalSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для обновления пользователя по id
    """

    updated_user = await UserService.update(
        user_id=user_id,
        data=data,
        session=session
    )

    if not updated_user:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='user not found'
        )

    return updated_user

@router.delete(
    '/{userid}',
    response_model=ResponseSchema,
    responses={
        200: {'model': ResponseSchema},
        404: {'model': ResponseSchema},
    },
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для удаления пользователя по id
    """

    result = await UserService.delete(user_id=user_id, session=session)

    if not result:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='user not found'
        )

    return ResponseSchema(message='The user has been deleted')
