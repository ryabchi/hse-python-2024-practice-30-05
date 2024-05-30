import functools

time_pointer = 1

def cache(max_size, time_to_live):
    
    
    
    def cache_decorator(func):    
        cache = {}
        
        def delete_from_cache():
            to_delete = []
            for key in cache.keys():
                if time_pointer - cache[key][1] >= time_to_live:
                    to_delete.append(key)
                    
            
            if (len(to_delete) != 0):
                for key in to_delete:
                    cache.pop(key)
                print("Из кеша удалены устаревшие результаты")
        
        functools.wraps(func)
        def wrapper(*args, **kwargs):
            global time_pointer
            key = args + tuple((kwargs.items()))
            
            if key in cache:
                print("Возвращено значение из кэша")
                time_pointer += 1
                result = cache[key][0]
                delete_from_cache()
                return result
            
            result = func(*args, **kwargs)
            
            if (len(cache) == max_size):
                print("Кэш очищен, так как достигнут максимальный размер")
                cache.clear()
                
            delete_from_cache()
            cache[key] = (result, time_pointer)
            
            print("Значение помещено в кэш")
            time_pointer += 1
            return result
        
        return wrapper
    
    return cache_decorator