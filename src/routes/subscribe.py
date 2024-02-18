from http import HTTPStatus

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.base import BlogAPIRouter
from src.schemas.response import ResponseSchema
from src.services.subscribe import SubscribeService
from src.utils.exceptions import CustomApiException


router = BlogAPIRouter(tags=['subscribe'])

@router.post(
    '/users/{user_id}/subscribe/{blog_id}',
    response_model=ResponseSchema,
    responses={
        201: {'model': ResponseSchema},
        404: {'model': ResponseSchema},
        423: {'model': ResponseSchema}
    },
)
async def create_subscribe(
    user_id: int,
    blog_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для подписки на блог
    """

    result = await SubscribeService.create(user_id=user_id, blog_id=blog_id, session=session)

    if result is True:
        return ResponseSchema(message='The subscription has been successfully completed')

    elif 'not found' in result:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail=result
        )

    else:
        raise CustomApiException(
            status_code=HTTPStatus.LOCKED, detail=result
        )

@router.delete(
    '/users/{user_id}/subscribe/{blog_id}',
    response_model=ResponseSchema,
    responses={
        200: {'model': ResponseSchema},
        404: {'model': ResponseSchema},
        423: {'model': ResponseSchema}
    },
)
async def delete_subscribe(
    user_id: int,
    blog_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для удаления подписки на блог
    """

    result = await SubscribeService.delete(user_id=user_id, blog_id=blog_id, session=session)

    if result is True:
        return ResponseSchema(message='Subscription has been cancelled successfully')

    elif 'not found' in result:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail=result
        )

    else:
        raise CustomApiException(
            status_code=HTTPStatus.LOCKED, detail=result
        )
