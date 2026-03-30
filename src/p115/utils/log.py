import logging
import traceback
import sys
from functools import wraps


logging.basicConfig(
    filename = 'data/app.log',
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    encoding = 'utf-8',
    filemode = 'w'
)


def log_info(msg):
    logging.info(msg)


def log_debug(msg):
    logging.debug(msg)


def log_error(msg):
    logging.error(msg)


def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log_debug(f'Function name: {func.__name__}')
            log_debug(f'Function {func.__name__} params: args={args} kwargs={kwargs}')
            result = func(*args, **kwargs)
            log_debug(f'Function {func.__name__} result: {result}')
            return result
        except Exception as e:
            exec_type, exec_value, exec_traceback = sys.exc_info()
            log_error(f'Exception caught in {func.__name__}: {e}')
            log_error(f'Exception type: {exec_type}')
            log_error(f'Exception value: {exec_value}')
            log_traceback = ''.join(traceback.format_tb(exec_traceback))
            log_error(f'Exception traceback: {log_traceback}')
            return None

    return wrapper
