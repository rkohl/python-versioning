import time
from functools import wraps


def taskDuration(func):
  """
    A decorator to measure the execution time of a function.
    Prints the function name and its execution time in seconds.
  """

  @wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.perf_counter()  # Use perf_counter() for better precision
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(
        f"'{func.__name__}' function took {duration:.4f} seconds to execute.")
    return result

  return wrapper
