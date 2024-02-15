from typing import List

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.base import BaseOutSchema
# from src.schemas.blog import BlogOutSchema


class UserInSchema(BaseModel):
    """
    Схема для добавления нового пользователя
    """

    username: str = Field(max_length=60)

    model_config = ConfigDict(from_attributes=True)


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
