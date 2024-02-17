from fastapi import FastAPI

from src.routes.user import router as user_routes
from src.routes.subscribe import router as subscribe_router
from src.routes.post import router as post_router


def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов для API
    """

    app.include_router(user_routes)
    app.include_router(subscribe_router)
    app.include_router(post_router)

    return app