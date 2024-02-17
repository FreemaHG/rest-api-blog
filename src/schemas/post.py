from datetime import datetime

from pydantic import Field, field_validator

from src.schemas.base import BaseOutSchema, OptionalBaseSchema


class PostInSchema(OptionalBaseSchema):
    """
    Схема для добавления нового поста
    """

    title: str = Field(max_length=80)
    text: str = Field(max_length=140)


# Схема для обновления поста (patch-запрос, поля не обязательные)
PostInOptionalSchema = PostInSchema.all_optional('PostInOptionalSchema')


class PostOutSchema(BaseOutSchema, PostInSchema):
    """
    Схема для вывода поста
    """

    # blog_id: int
    created_at: str

    @field_validator('created_at', mode='before')
    def serialize_created_at(cls, post_datetime: datetime):
        """
        Возвращаем дату и время создания поста в нужном формате
        """
        formatted_datetime = post_datetime.strftime("%d-%m-%Y %H:%M:%S")

        return formatted_datetime
