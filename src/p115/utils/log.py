import logging
import traceback
import sys
import inspect
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


def log_caller(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            frame = inspect.stack()[1]
            caller_name = frame.function
            caller_filename = frame.filename
            caller_lineno = frame.lineno

            args_str = [str(a) for a in args]
            kwargs_str = [f"{k}={v}" for k, v in kwargs.items()]
            all_args = ", ".join(args_str + kwargs_str)

            log_debug(
                f'函数 {func.__name__} 被调用.\n'
                f'\t调用方: {caller_name} (文件: {caller_filename}, 行号: {caller_lineno})\n'
                f'\t参数: {all_args}'
            )
            result = func(*args, **kwargs)
            log_debug(
                f'函数 {func.__name__} 被调用完成.\n'
                f'\t返回: {result}'
            )
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
