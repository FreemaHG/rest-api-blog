from fastapi import FastAPI, Query
from fastapi_pagination import add_pagination, Page

from src.urls import register_routers
from src.utils.exceptions import CustomApiException, custom_api_exception_handler

app = FastAPI(title='Blog API', debug=True)

# Регистрация роутов
register_routers(app)

# Добавляем API в пагинатор
add_pagination(app)

# По умолчанию пагинация по 10 записей, максимум 500 записей
Page = Page.with_custom_options(
    size=Query(10, ge=1, le=500),
)

# Регистрация кастомного исключения
app.add_exception_handler(CustomApiException, custom_api_exception_handler)
