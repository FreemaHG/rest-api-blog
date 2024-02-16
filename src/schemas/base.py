from pydantic import BaseModel, ConfigDict, create_model


class BaseOutSchema(BaseModel):
    """
    Базовая схема для вывода записей
    """

    id: int

    model_config = ConfigDict(from_attributes=True)


class OptionalBaseSchema(BaseModel):
    """
    Базовая схема для частичного обновления записей
    """

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def all_optional(cls, name: str):
        """
        Создает новую модель с теми же полями, но все необязательные.
        Использование: SomeOptionalModel = SomeModel.all_optional('SomeOptionalModel')
        """
        return create_model(
            name,
            __base__=cls,
            **{name: (info.annotation, None) for name, info in cls.model_fields.items()}
        )

