from fastapi import APIRouter


class BlogAPIRouter(APIRouter):
    """
    Базовый URL и версия API для блога
    """

    def __init__(self, *args, **kwargs):
        self.prefix = '/api/v1'
        super().__init__(*args, **kwargs, prefix=self.prefix)
