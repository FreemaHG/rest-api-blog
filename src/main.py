from fastapi import FastAPI

from src.urls import register_routers
from src.utils.exceptions import CustomApiException, custom_api_exception_handler

app = FastAPI(title='Blog API', debug=True)

register_routers(app)

app.add_exception_handler(CustomApiException, custom_api_exception_handler)
