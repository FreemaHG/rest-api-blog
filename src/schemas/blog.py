from typing import List

from pydantic import BaseModel, ConfigDict

from src.schemas.base import BaseOutSchema
from src.schemas.post import PostOutSchema
from src.schemas.user import UserOutSchema


# TODO Используется базовая схема
# class BlogOutSchema(BaseModel):
#     """
#     Схема для вывода данных о блоге
#     """
#     id: int
#
#     model_config = ConfigDict(from_attributes=True)


class BlogOutWithPostsSchema(BaseOutSchema):
    """
    Схема для вывода блога с постами
    """

    posts: List[PostOutSchema]


class BlogOutWithFollowersSchema(BaseOutSchema):
    """
    Схема для вывода блога с подписчиками
    """

    followers: List[UserOutSchema]


class BlogOutWithPostsAndFollowersSchema(BlogOutWithPostsSchema, BlogOutWithFollowersSchema):
    """
    Схема для вывода блога с постами и подписчиками
    """

    pass
