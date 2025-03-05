"""Logging module for PyWall."""

import logging
import os
from src.logging_utils import (
    action_logger,
    log_exception,
    log_critical_exception,
    log_standard_exception,
    enable_logging
)
from src.config import get_config


def exists(file):
    """Check if a file exists"""
    return os.path.exists(file)


# Re-export with original names for backward compatibility
actionLogger = action_logger
logException = log_exception
logCriticalException = log_critical_exception
logStandardException = log_standard_exception
enableLogging = enable_logging


def actionLogger(actionLogged):
    """Log an action to console and optionally to a file"""
    # This ought to fix all errors caused by not unicode characters...hopefully #
    try:
        print(str(actionLogged))
    except UnicodeError:
        print(str(actionLogged).encode("utf8"))

    try:
        if get_config("DEBUG", "create_logs") == "True":
            with open('logger.log', 'a') as log:
                log.write(actionLogged + '\n')
    except Exception as Argument:
        print(
            "Something went really wrong, due to this incident no logs have been created, see full traceback: "
            f"{Argument}"
        )


def logException(Argument, *Critical):
    """Log an exception based on its criticality"""
    if Argument == "bypass":
        logCriticalException(Critical)
    else:
        logStandardException(Critical)


def logCriticalException(Critical):
    """Log a critical exception that will raise an error after logging"""
    number = 0
    logNameBool = exists(f"errorLogCritical{number}.log")
    while logNameBool:
        number += 1
        logNameBool = exists(f"errorLogCritical{number}.log")

    logName = f"errorLogCritical{number}.log"
    logging.basicConfig(filename=logName, filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.exception(
        f'Runtime error is "{Critical}", see full traceback below: \n ', exc_info=True)
    actionLogger(f'Exception logged, runtime error is "{Critical}"')
    raise Exception(Critical)


def logStandardException(Critical):
    """Log a standard exception without raising"""
    try:
        if get_config("DEBUG", "create_exception_logs") == "True":
            number = 0
            logNameBool = exists(f"errorLog{number}.log")
            while logNameBool:
                number += 1
                logNameBool = exists(f"errorLog{number}.log")

            logName = f"errorLog{number}.log"
            logging.basicConfig(filename=logName, filemode='w',
                                format='%(name)s - %(levelname)s - %(message)s')
            logging.exception(
                f'Runtime error is "{Critical}", see full traceback below: \n ', exc_info=True)
            actionLogger(f'Exception logged, runtime error is "{Critical}"')
    except Exception as e:
        actionLogger(f'Failed to log exception: {e}')


def enableLogging(enable: bool):
    """Enable or disable logging at the root level"""
    if enable:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.disable(logging.CRITICAL)
