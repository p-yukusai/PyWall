from os.path import exists
from src.config import getConfig
import logging

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

action_logger = setup_logger('action_logger', 'action.log')
exception_logger = setup_logger('exception_logger', 'exception.log', level=logging.ERROR)

def actionLogger(actionLogged):
    try:
        print(str(actionLogged))
    except UnicodeError:
        print(str(actionLogged).encode("utf8"))
    try:
        if getConfig("DEBUG", "create_logs") == "True":
            action_logger.info(actionLogged)
    except Exception as Argument:
        print("Something went really wrong, due to this incident no logs have been created, see full traceback: "
              f"{Argument}")
    print("Action logged successfully")

def logException(Argument, *Critical):
    if Argument == "bypass":
        number = 0
        logNameBool = exists(f"errorLogCritical{number}.log")
        while logNameBool:
            number += 1
            logNameBool = exists(f"errorLogCritical{number}.log")
        logName = f"errorLogCritical{number}.log"
        logging.basicConfig(filename=logName, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        logging.exception(f'Runtime error is "{Critical}", see full traceback bellow: \n ', exc_info=True)
        actionLogger(f'Exception logged, runtime error is "{Critical}"')
        raise Exception(Critical)

    try:
        if getConfig("DEBUG", "create_exception_logs") == "True":
            number = 0
            logNameBool = exists(f"errorLog{number}.log")
            while logNameBool:
                number += 1
                logNameBool = exists(f"errorLog{number}.log")

            logName = f"errorLog{number}.log"
            logging.basicConfig(filename=logName, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
            logging.exception(f'Runtime error is "{Argument}", see full traceback bellow: \n ', exc_info=True)
            actionLogger(f'Exception logged, runtime error is "{Argument}"')
        else:
            pass
    except Exception as Critical:
        logException("bypass", Critical)
    print("Exception logged successfully")
