import asyncio

from celery import Celery

from src.business.news_feed import NewsFeedBusiness
from src.config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_USER


celery = Celery('tasks', broker=f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672')

@celery.task
def update_news_feeds(blog_id: int, post_id: int) -> None:
    """
    Обновление новостных лент пользователей, подписанных на блог
    :param blog_id: id блога
    :param post_id: id нового поста
    :return: None
    """

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        NewsFeedBusiness.add_new(blog_id=blog_id, post_id=post_id)
    )
