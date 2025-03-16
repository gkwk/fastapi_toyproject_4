import time
from celery import Celery
from celery.signals import worker_shutdown

from app_celery_worker.configurations.configuration import get_settings
from app_celery_worker.services.celery_async_queue_test import celery_async_queue_test
from app_database_redis.instance import redis_handler_async
from commons.core.asyncio_handler import AsyncioHandler

celery_worker_app = Celery(__name__, broker=get_settings().CELERY_BROKER_PATH_URL)


@worker_shutdown.connect
def shutdown_process(**kwargs):
    with AsyncioHandler.get_event_loop() as event_loop:
        event_loop.run_until_complete(redis_handler_async.close())
    print("SHUTDOWN : Redis Connection")
    AsyncioHandler.close_event_loop()
    print("SHUTDOWN : Event Loop")


@celery_worker_app.task(name=get_settings().CELERY_ASYNC_QUEUE_TEST_TASK_NAME)
@AsyncioHandler.async_to_sync
async def process_celery_task(task_id: int, number_of_task: int, sleep_time: float):
    try:
        counter = time.time()

        print(await celery_async_queue_test(task_id=task_id, number_of_task=number_of_task, sleep_time=sleep_time))

        print(time.time() - counter)
    except Exception as e:
        print(e)
    finally:
        pass
