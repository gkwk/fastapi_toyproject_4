from celery import Celery
from celery.signals import worker_shutdown

from app_celery_beat.configurations.configuration import get_settings
from app_database_redis.instance import redis_handler_async
from commons.core.asyncio_handler import AsyncioHandler


celery_beat_worker_app = Celery(__name__, broker=get_settings().CELERY_BROKER_PATH_URL)


celery_beat_worker_app.conf.beat_schedule = {
    get_settings().CELERY_BEAT_TEST_TASK_NAME: {
        "task": get_settings().CELERY_BEAT_TEST_TASK_NAME,
        "schedule": 5,
        "args": (),
    },
}

celery_beat_worker_app.conf.task_routes = {
    get_settings().CELERY_BEAT_TEST_TASK_NAME: {"queue": get_settings().CELERY_BEAT_QUEUE_NAME},
}


@worker_shutdown.connect
def shutdown_process(**kwargs):
    with AsyncioHandler.get_event_loop() as event_loop:
        event_loop.run_until_complete(redis_handler_async.close())
    print("SHUTDOWN : Redis Connection")
    AsyncioHandler.close_event_loop()
    print("SHUTDOWN : Event Loop")


@celery_beat_worker_app.task(
    name=get_settings().CELERY_BEAT_TEST_TASK_NAME, queue=get_settings().CELERY_BEAT_QUEUE_NAME
)
@AsyncioHandler.async_to_sync
async def oscillator():
    await redis_handler_async.oscillator()
    print("oscillating...")
