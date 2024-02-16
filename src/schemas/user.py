from typing import List

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.base import BaseOutSchema, OptionalBaseSchema


# from src.schemas.blog import BlogOutSchema


class UserInSchema(OptionalBaseSchema):
    """
    Схема для добавления нового пользователя
    """

    username: str = Field(max_length=60)


# Схема для обновления пользователя (patch-запрос, поля не обязательные)
UserInOptionalSchema = UserInSchema.all_optional('UserInOptionalSchema')


class UserOutSchema(BaseOutSchema, UserInSchema):
    """
    Схема для вывода данных о пользователе
    """

    pass


class UserOutWithBlogsSchema(UserOutSchema):
    """
    Схема для вывода данных о пользователе с его подписками на блоги
    """

    # blogs: List[BlogOutSchema]
    blogs: List[BaseOutSchema]
