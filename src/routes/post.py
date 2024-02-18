from http import HTTPStatus
from typing import Union, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.base import BlogAPIRouter
from src.schemas.post import PostOutSchema, PostInSchema, PostInOptionalSchema
from src.schemas.response import ResponseSchema
from src.services.post import PostService, PostListService
from src.utils.exceptions import CustomApiException


router = BlogAPIRouter(tags=['post'])

@router.get(
    '/users/{user_id}/blogs/{blog_id}/posts',
    response_model=Union[List[PostOutSchema], ResponseSchema],
    responses={
        200: {'model': List[PostOutSchema]},
        404: {'model': ResponseSchema},
    },
)
async def get_posts_list(
    blog_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для вывода всех постов в блоге пользователя
    """

    posts = await PostListService.get_list(blog_id=blog_id, session=session)

    if posts is False:
        raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail='blog not found')

    return posts


@router.post(
    '/users/{user_id}/blogs/{blog_id}/posts',
    response_model=Union[PostOutSchema, ResponseSchema],
    responses={
        201: {'model': PostOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def create_post(
    blog_id: int,
    new_post: PostInSchema,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для добавления нового поста
    """

    post = await PostService.create(blog_id=blog_id, new_post=new_post, session=session)

    return post


@router.get(
    '/users/{user_id}/blogs/{blog_id}/posts/{post_id}',
    response_model=Union[PostOutSchema, ResponseSchema],
    responses={
        200: {'model': PostOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для вывода поста
    """

    post = await PostService.get(post_id=post_id, session=session)

    if not post:
        raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail='post not found')

    return post


@router.patch(
    '/users/{user_id}/blogs/{blog_id}/posts/{post_id}',
    response_model=Union[PostOutSchema, ResponseSchema],
    responses={
        200: {'model': PostOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def update_post(
    post_id: int,
    data: PostInOptionalSchema,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для обновления поста
    """

    updated_post = await PostService.update(
        post_id=post_id,
        data=data,
        session = session
    )

    if not updated_post:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='post not found'
        )

    return updated_post

@router.delete(
    '/users/{user_id}/blogs/{blog_id}/posts/{post_id}',
    response_model=ResponseSchema,
    responses={
        200: {'model': ResponseSchema},
        404: {'model': ResponseSchema},
    },
)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Роут для удаления поста
    """

    result = await PostService.delete(post_id=post_id, session=session)

    if not result:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='post not found'
        )

    return ResponseSchema(message='The post has been deleted')
