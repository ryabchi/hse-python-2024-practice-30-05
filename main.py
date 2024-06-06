from functools import wraps
from typing import Any, Callable, List
import time
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class StorageObject:
    def __init__(self, value: Any, start_time: float) -> None:
        self.value = value
        self.start_time = start_time


"""
TASK 1 & 2
"""


def cache(cache_size: int = 1) -> Callable:
    def cache_decorator(func: Callable) -> Callable:
        storage: dict[str, StorageObject] = {}

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = func.__name__ + str((*args, *(kwargs.values())))

            if key in storage:
                storage_val = storage[key].value
                logging.info(f"Retrieving from cache: {storage_val}")
                return storage_val

            if len(storage) == cache_size:
                key_for_delete = next(iter(storage))
                del storage[key_for_delete]

            logging.info("Computing result")
            result = func(*args, **kwargs)

            storage[key] = StorageObject(result, time.time())

            return result

        return wrapper

    return cache_decorator


"""
TASK 3
"""


def cache_with_time(cache_time: int = 1) -> Callable:
    def cache_with_time_decorator(func: Callable) -> Callable:
        storage: dict[str, StorageObject] = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            while storage:
                storage_obj = next(iter(storage.items()))
                if current_time - storage_obj[1].start_time <= cache_time:
                    break
                del storage[storage_obj[0]]

            key = f"{func.__name__}{args}{kwargs}"
            if key in storage:
                storage_val = storage[key].value
                logging.info(f"Retrieving from cache: {storage_val}")
                return storage_val

            logging.info("Computing result")
            result = func(*args, **kwargs)

            storage[key] = StorageObject(result, current_time)

            return result

        return wrapper

    return cache_with_time_decorator


@cache()
def some_sum_func(a: List[int], b: List[int]) -> None:
    return a + b


@cache_with_time()
def some_reverse_func(a: List[int], b: List[int]) -> None:
    return (a + b)[::-1]


print(some_sum_func([1], [2]))
print(some_sum_func([1], [2]))
print(some_sum_func([2], [3]))
print(some_sum_func([1], [2]))

print(some_reverse_func([1], [2]))
print(some_reverse_func([1], [2]))
print(some_reverse_func([2], [3]))
time.sleep(2)
print(some_reverse_func([1], [2]))
