import asyncio
import contextlib
from typing import Callable, TypeVar
import functools


F = TypeVar("F", bound=Callable)


class AsyncioHandler:
    """
    Celery와 함께 사용하기 위한 Asyncio 이벤트 루프 핸들러
    prefork 모드 및 python 3.12 이상에서 사용할 수 있게 설계됨.
    """

    _loop_list: list[asyncio.events.AbstractEventLoop] = []

    @classmethod
    @contextlib.contextmanager
    def get_event_loop(cls):
        if len(cls._loop_list) < 1:
            cls._loop_list.append(asyncio.new_event_loop())
            asyncio.set_event_loop(cls._loop_list[0])

        loop = cls._loop_list[0]

        try:
            yield loop
        finally:
            pass

    @classmethod
    def close_event_loop(cls) -> None:
        """
        현재 이벤트 루프에서 모든 태스크를 취소하고 이벤트 루프를 닫는다.
        워커가 종료될 때 호출
        """
        if not cls._loop_list:
            return

        with cls.get_event_loop() as event_loop:
            pending_tasks = asyncio.all_tasks(event_loop)
            for task in pending_tasks:
                task.cancel()
            event_loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
            event_loop.run_until_complete(event_loop.shutdown_asyncgens())
            event_loop.close()

        cls._loop_list.clear()

    @classmethod
    def async_to_sync(cls, function: F) -> F:
        """
        비동기 함수를 동기 함수로 변환하는 데코레이터
        """

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = None
            with cls.get_event_loop() as event_loop:
                result = event_loop.run_until_complete(function(*args, **kwargs))
            return result

        return wrapper
