from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """
    Cхема для возврата сообщения с ответом
    """

    message: str
