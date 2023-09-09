import time
from threading import Thread

def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = [None]
            exception = [None]

            def target():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = Thread(target=target)
            thread.start()
            thread.join(timeout=seconds)

            if thread.is_alive():
                thread.join()  # Clean up the thread
                raise TimeoutError(f'Timed out after {seconds} seconds')
            if exception[0] is not None:
                raise exception[0]

            return res[0]

        return wrapper
    return decorator


def retry_with_timeout(max_retries=3, timeout_s=5, wait_time=1):
    def decorator(func):
        def wrapper(*args, **kwargs):

            @timeout(timeout_s)
            def timeout_aware_call():
                return func(*args, **kwargs)

            retries = 0
            while retries < max_retries:
                try:
                    return timeout_aware_call()
                except TimeoutError as e:
                    print(f"Retry {retries + 1}/{max_retries} - Error: {e}")
                    retries += 1
                    time.sleep(wait_time)
            raise Exception("Function execution failed after multiple retries")
        return wrapper
    return decorator