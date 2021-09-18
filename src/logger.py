from os.path import exists
from src.config import getConfig
import logging


def actionLogger(actionLogged):
    print(actionLogged)
    try:
        if getConfig("DEBUG", "create_logs") == "True":
            with open('logger.log', 'a') as log:
                log.write(actionLogged + '\n')
    except Exception as Argument:
        print("Something went really wrong, due to this incident no logs have been created, see full traceback: "
              f"{Argument}")


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
