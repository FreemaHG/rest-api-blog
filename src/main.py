from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.urls import register_routers
from src.utils.exceptions import CustomApiException, custom_api_exception_handler


app = FastAPI(title='Blog API', debug=True)

# Регистрация роутов
register_routers(app)

# Добавляем API в пагинатор
add_pagination(app)

# Регистрация кастомного исключения
app.add_exception_handler(CustomApiException, custom_api_exception_handler)
