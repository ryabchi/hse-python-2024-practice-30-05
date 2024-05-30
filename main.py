import time


class Result:
    def __init__(self, value, saved_at):
        self.value = value
        self.saved_at = saved_at


def cache(time_to_live: int = 5):
    def cache_decorator(func):
        results = {}

        def wrapper(*args, **kwargs):
            print('----------------')

            while len(results) > 0:
                key_oldest = next(iter(results))
                if time.time() - results[key_oldest].saved_at > time_to_live:
                    print(f'Remove old result with key {key_oldest}')
                    del results[key_oldest]
                else:
                    break

            key = str((*args, *(kwargs.values())))
            print(f'Key: {key}')
            value = results.get(key)
            if isinstance(value, Result):
                print('Get from storage')
                return value.value

            print('Call function')
            result = func(*args, **kwargs)
            results[key] = Result(result, time.time())
            return result
        return wrapper
    return cache_decorator


@cache(3)
def sum(a: list[int], b: list[int]):
    if len(a) == 0 or len(b) == 0:
        return None
    return a + b


print(sum([2], [3]))
time.sleep(2)
print(sum([1], [3]))
time.sleep(2)
print(sum([2], [3]))
print(sum([1], [3]))
