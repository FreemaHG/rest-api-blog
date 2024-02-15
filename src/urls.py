from fastapi import FastAPI

from src.routes.user import router as user_routes


def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов для API
    """

    app.include_router(user_routes)

    return app