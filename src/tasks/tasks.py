import asyncio

from celery import Celery
from celery.schedules import crontab

from src.business.news_feed import NewsFeedBusiness
from src.config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_USER
from src.services.feed import FeedService


celery = Celery('tasks', broker=f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672')
celery.conf.enable_utc = False
celery.conf.timezone = 'Europe/London'


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Рассылка новостей
    """

    sender.add_periodic_task(
        crontab(hour=12, minute=00),
        sending_out_latest_news.s(),
        name='Get last 5 posts from news feed'
    )

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

@celery.task
def sending_out_latest_news():
    """
    Получить 5 последних постов из новостной ленты
    """
    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        FeedService.get_last_news()
    )
