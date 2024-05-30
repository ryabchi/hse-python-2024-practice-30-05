import time

STORAGE = {}


class StorageObject:
    def __init__(self, value, saved_at):
        self.value = value
        self.saved_at = saved_at


def cache(cache_size: int = 5):
    def cache_decorator(func):
        def wrapper(*args, **kwargs):
            print('----')
            key = func.__name__ + str((*args, *(kwargs.values())))

            value = STORAGE.get(key)
            if isinstance(value, StorageObject):
                print('Get from storage')
                return value.value

            if cache_size == len(STORAGE):
                key_for_delete = next(iter(STORAGE))
                del STORAGE[key_for_delete]

            print(f'Call function {func.__name__}')
            result = func(*args, **kwargs)
            STORAGE[key] = StorageObject(value=result, saved_at=time.time())
            print('----')
            return result

        return wrapper

    return cache_decorator


@cache()
def sum(a: list[int], b: list[int]) -> list[int]:
    return a + b


@cache()
def mult(a: list[int], b: list[int]) -> list[int]:
    return (a + b)[::-1]


print(sum([1], [2]))
print(mult([1], [2]))
print(sum([1], [2]))
