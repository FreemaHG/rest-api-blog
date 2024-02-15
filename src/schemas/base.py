from pydantic import BaseModel, ConfigDict


class BaseOutSchema(BaseModel):
    """
    Базовая схема для вывода записей
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
