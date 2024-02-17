from http import HTTPStatus
from typing import Union, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.repositories.feed import FeedRepository
from src.routes.base import BlogAPIRouter
from src.schemas.post import PostOutSchema
from src.schemas.response import ResponseSchema
from src.services.feed import FeedService
from src.utils.exceptions import CustomApiException


router = BlogAPIRouter(tags=['feed'])

@router.get(
    '/users/{user_id}/feed',
    response_model=Union[List[PostOutSchema], ResponseSchema],
    responses={
        200: {'model': List[PostOutSchema]},
        404: {'model': ResponseSchema},
    },
)
async def get_feed(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для вывода ленты новостей пользователя
    """

    # TODO Добавить пагинацию!!!
    news = await FeedService.get_list(user_id=user_id, session=session)

    if news is False:
        raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail='user not found')

    return news

@router.put(
    '/users/{user_id}/feed/mark-as-read/{post_id}',
    response_model=ResponseSchema,
    responses={
        200: {'model': ResponseSchema},
        404: {'model': ResponseSchema},
    },
)
async def mark_post_as_read(
    user_id: int,
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут, чтобы пометить пост прочитанным
    """

    result = await FeedService.read(user_id=user_id, post_id=post_id, session=session)

    if result is False:
        raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail='user not found')

    return ResponseSchema(message="The post is marked as read")
