#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Package Utilities Module

"""
import datetime
import logging
import logging.config
import functools
import operator
import os
import re
import time
from typing import Any, Dict, List, Tuple, Union
import warnings

import matplotlib.pyplot as plt
import numpy as np

from butterfly.pkg_globals import FONT_SIZE, PACKAGE_ROOT
from butterfly.exceptions import InputError


def logger_setup(file_path: Union[None, str] = None,
                 logger_name: str = 'package') -> logging.Logger:
    """
    Configure logger with console and file handlers.

    :param file_path: if supplied the path will be appended by a timestamp \
        and ".log" else the default name of "info.log" will be saved in the \
        location of the caller.
    :param logger_name: name to be assigned to logger
    """
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': ('%(levelname)s - %(name)s -> Line: %(lineno)d <- '
                           '%(message)s'),
            },
            'file': {
                'format': ('%(asctime)s - %(levelname)s - %(module)s.py -> '
                           'Line: %(lineno)d <- %(message)s'),
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'WARNING',
                'formatter': 'console',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'encoding': 'utf8',
                'level': 'DEBUG',
                'filename': 'info.log',
                'formatter': 'file',
                'mode': 'w',
            },
        },
        'loggers': {
            'package': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
    if file_path:
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        file_path = f'{file_path}_{time_stamp}.log'
        nested_set(config, ['handlers', 'file', 'filename'], file_path)
    logging.config.dictConfig(config)
    return logging.getLogger(logger_name)


def matplotlib_defaults():
    """Set matplotlib default values."""
    params = {
        'axes.labelsize': FONT_SIZE['label'],
        'axes.titlesize': FONT_SIZE['title'],
        'figure.titlesize': FONT_SIZE['super_title'],
        'patch.edgecolor': 'black',
        'patch.force_edgecolor': True,
    }
    plt.rcParams.update(params)


def nested_get(nested_dict: Dict[Any, Any], key_path: List[Any]) -> Any:
    """
    Retrieve value from a nested dictionary.

    :param nested_dict: nested dictionary
    :param key_path: list of key levels with the final entry being the target
    """
    return functools.reduce(operator.getitem, key_path, nested_dict)


def nested_set(nested_dict: Dict[Any, Any], key_path: List[Any], value: Any):
    """
    Set object of nested dictionary.

    :param nested_dict: nested dictionary
    :param key_path: list of key levels with the final entry being the target
    :param value: new value of the target key in `key_path`
    """
    nested_get(nested_dict, key_path[:-1])[key_path[-1]] = value


def progress_str(n: int, total: int,
                 msg: Union[None, str] = 'Progress') -> str:
    """
    Generate progress percentage message.

    :param n: number of current item
    :param total: total number of items
    :param msg: message to prepend to progress percentage
    """
    if total == 0:
        raise ZeroDivisionError('Parameter `total` may not be equal to zero.')
    if n > total:
        raise InputError(
            expression='n > total',
            message='Current item value `n` must be less than total.')
    progress_msg = f'\r{msg}: {n / total: .1%}'
    return progress_msg if n < total else progress_msg + '\n\n'


def project_vars():
    """Load project specific environment variables."""
    with open(PACKAGE_ROOT / 'envfile', 'r') as f:
        txt = f.read()
    env_vars = re.findall(r'export\s(.*)=(.*)', txt)
    for name, value in env_vars:
        os.environ[name] = value


def rle(arr: Union[List[Any], np.ndarray]) \
        -> Union[Tuple[np.ndarray, ...], Tuple[None, ...]]:
    """
    Run Length Encode provided array.

    :param arr: array to be encoded
    :return: Start Indices for code, Length of code, Value of code
    """
    arr = np.array(arr) if not isinstance(arr, np.ndarray) else arr
    vec = arr.flatten() if arr.ndim > 1 else arr
    n = vec.size
    if n == 0:
        return None, None, None
    switch_idx = np.nonzero(vec[1:] != vec[:-1])[0] + 1
    ids = np.r_[0, switch_idx]
    lengths = np.diff(np.r_[ids, n])
    return ids, lengths, vec[ids]


def status(status_logger: logging.Logger):
    """
    Decorator to issue logging statements and time function execution.

    :param status_logger: name of logger to record status output
    """

    def status_decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            status_logger.info(f'Initiated: {name}')
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            status_logger.info(f'Completed: {name} -> {end - start:0.3g}s')
            return result

        return wrapper
    return status_decorator


def warning_format():
    """
    Set warning output message format.

    ..note:: For new formats add helper functions then update the \
        `warnings.formatwarning` call.
    """

    def message_only(message, category, filename, lineno, line=''):
        return f'{message}\n'

    warnings.formatwarning = message_only


if __name__ == '__main__':
    pass
