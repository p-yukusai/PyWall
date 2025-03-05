"""Basic logging utilities for PyWall."""

import logging
from os.path import exists


def action_logger(action_logged):
    """Log an action to console and optionally to a file"""
    try:
        print(str(action_logged))
    except UnicodeError:
        print(str(action_logged).encode("utf8"))


def log_exception(argument, *critical):
    """Log an exception based on its criticality"""
    if argument == "bypass":
        log_critical_exception(critical)
    else:
        log_standard_exception(critical)


def log_critical_exception(critical):
    """Log a critical exception that will raise an error after logging"""
    number = 0
    log_name_bool = exists(f"errorLogCritical{number}.log")
    while log_name_bool:
        number += 1
        log_name_bool = exists(f"errorLogCritical{number}.log")

    log_name = f"errorLogCritical{number}.log"
    logging.basicConfig(filename=log_name, filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.exception(
        f'Runtime error is "{critical}", see full traceback below: \n ', exc_info=True)
    action_logger(f'Exception logged, runtime error is "{critical}"')
    raise Exception(critical)


def log_standard_exception(critical):
    """Log a standard exception without raising"""
    try:
        number = 0
        log_name_bool = exists(f"errorLog{number}.log")
        while log_name_bool:
            number += 1
            log_name_bool = exists(f"errorLog{number}.log")

        log_name = f"errorLog{number}.log"
        logging.basicConfig(filename=log_name, filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s')
        logging.exception(
            f'Runtime error is "{critical}", see full traceback below: \n ', exc_info=True)
        action_logger(f'Exception logged, runtime error is "{critical}"')
    except Exception as e:
        action_logger(f'Failed to log exception: {e}')


def enable_logging(enable: bool):
    """Enable or disable logging at the root level"""
    if enable:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.disable(logging.CRITICAL)
