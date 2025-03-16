import asyncio
from typing import Callable, Awaitable, TypeVar

from app_database_redis.instance import redis_handler_async


T = TypeVar("T")


async def celery_async_queue_test(task_id: int, number_of_task: int, sleep_time: float) -> list:
    asyncio_queue: asyncio.Queue[tuple[int, Callable[[], Awaitable[T]]]] = asyncio.Queue()
    asyncio_queue_results: dict[int, int | None] = {i: None for i in range(number_of_task)}

    for index in asyncio_queue_results:
        await asyncio_queue.put(index)

    dispatcher = asyncio.create_task(
        continuous_dispatcher(
            task_id=task_id,
            asyncio_queue=asyncio_queue,
            asyncio_queue_results=asyncio_queue_results,
            sleep_time=sleep_time,
        )
    )

    monitor_task = asyncio.create_task(_monitor_cancellation(task_id=task_id))

    done, pending = await asyncio.wait(
        [asyncio.gather(asyncio_queue.join()), monitor_task], return_when=asyncio.FIRST_COMPLETED
    )

    await _cancel_task(dispatcher)

    await _clear_queue(asyncio_queue)

    if monitor_task in done:
        for task in pending:
            task.cancel()

        await asyncio.gather(*pending, return_exceptions=True)
        return asyncio_queue_results

    await _cancel_task(monitor_task)

    return asyncio_queue_results


async def _cancel_task(task: asyncio.Task):
    if not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


async def _clear_queue(queue: asyncio.Queue):
    while not queue.empty():
        try:
            queue.get_nowait()
            queue.task_done()
        except asyncio.QueueEmpty:
            break


async def continuous_dispatcher(
    task_id: int,
    asyncio_queue: asyncio.Queue[int],
    asyncio_queue_results: dict[int, int],
    sleep_time: float,
) -> None:
    try:
        while True:
            try:
                print(f"{task_id} : {asyncio_queue.qsize()}")

                queue_task_index = asyncio_queue.get_nowait()

                asyncio.create_task(
                    worker(
                        queue_task_index=queue_task_index,
                        asyncio_queue_results=asyncio_queue_results,
                        sleep_time=sleep_time,
                    )
                )

            except asyncio.QueueEmpty as e:
                print(f"{task_id} : {asyncio_queue.qsize()} / In Progress")
                await asyncio.sleep(10)
                continue

            except Exception as e:
                print(e)
                raise Exception()
    except Exception as e:
        print(e)


async def worker(
    queue_task_index: int,
    asyncio_queue_results: dict[int, int],
    sleep_time: float,
) -> None:
    try:
        asyncio.sleep(sleep_time)
        asyncio_queue_results[queue_task_index] = queue_task_index

    except Exception as e:
        pass

    finally:
        pass


async def _monitor_cancellation(task_id: int) -> bool:
    check_interval = 5

    while True:
        if await redis_handler_async.exist(f"celery_task_cancelled:{task_id}"):
            await redis_handler_async.delete(f"celery_task_cancelled:{task_id}")
            print(f"Cancellation requested : task_id - {task_id}")
            return True

        await asyncio.sleep(check_interval)
