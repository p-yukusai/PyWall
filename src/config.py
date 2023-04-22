import pathlib
import sys
import os
import configparser
import time


config = configparser.ConfigParser()
pyWall_Ini = "\\PyWall\\Config.ini"
PyWall = "\\PyWall"


def documentFolder():
    # From a kind soul on StackOverflow #
    import ctypes.wintypes
    GET_PERSONAL = 5  # My Documents #
    GET_CURRENT = 0  # Get current value, not default #
    doc = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, GET_PERSONAL, None, GET_CURRENT, doc)
    document_folder = doc.value
    return document_folder


# Yes, I know, I know, this is just about the laziest way to get the working folder, but I had to write it down #
# somewhere to get the context menu to work, so that's that :P #

def scriptFolder():
    path = os.getcwd()
    if path is not str:
        try:
            path = sys._MEIPASS
        except AttributeError:
            path = os.path.abspath(".")
    document_folder = documentFolder()
    if pathlib.Path.is_file(pathlib.Path(document_folder + PyWall + "\\Executable.txt")):
        with open(document_folder + PyWall + "\\Executable.txt", 'r') as exe:
            executable = exe.read()
            if executable == os.getcwd():
                pass
            else:
                with open(document_folder + PyWall + "\\Executable.txt", 'w') as e:
                    e.write(os.getcwd())
    else:
        with open(document_folder + PyWall + "\\Executable.txt", 'w') as exe:
            exe.write(os.getcwd())


def config_read():
    document_folder = documentFolder()
    config_file = document_folder + pyWall_Ini
    return str(config_file)


def configFile():
    document_folder = documentFolder()
    if os.path.exists(document_folder + pyWall_Ini):
        return str(document_folder + pyWall_Ini)
    else:
        makeDefault()
        return str(document_folder + pyWall_Ini)


default_config = {
    "FILETYPE": {
        "accepted_types": ".exe",
        "blacklisted_names": "",
        "recursive": "True"
    },
    "GUI": {
        "advanced_mode": "False",
        "stylesheet": "dark_red.xml",
        "first_run": "True"
    },
    "DEBUG": {
        "create_logs": "False",
        "create_exception_logs": "True",
        "version": "v1.7.2",
        "shell": "False"
    }
}


def default(default_file=None):
    document_folder = documentFolder()
    config_file = document_folder + pyWall_Ini
    if default_file is None:
        default_file = default_config
    for x in default_file.keys():  # Add default sections
        if not config.has_section(x):
            config.add_section(x)
        for y in default_file[x]:  # Add default values
            if not config.has_option(x, y):
                config.set(x, y, default_file.get(x, y)[y])

    with open(config_file, 'w') as configfile:
        config.write(configfile)


def makeDefault():
    try:
        document_folder = documentFolder()
        config_folder = document_folder + PyWall
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
        default()
    except FileNotFoundError:
        document_folder = "C:\\Users\\Public\\Documents" # This should be available on every Windows install
        config_folder = document_folder + PyWall
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
        default()

def getConfig(Section, Variable, *extra_args):  # Basically a more robust version of the basic read_ini
    config.read(configFile())
    if extra_args:
        try:
            indexValue = ''.join(extra_args)
            value = config[Section][Variable]
            List = value.split(', ')
            if "len" in extra_args:
                return len(List)
            return List[int(indexValue)]
        except KeyError:
            print("Invalid query")
            return False

    try:
        if config.has_option(Section, Variable):
            return config[Section][Variable]
    except AttributeError:  # High likelihood of the config file is just being written
        time.sleep(0.1)
        config.read(configFile())
        try:
            if config.has_option(Section, Variable):
                return config[Section][Variable]
        except AttributeError:  # High likelihood of the query item being tampered by the user
            try:
                default()
                config.read(configFile())
                if config.has_option(Section, Variable):
                    return config[Section][Variable]
            except AttributeError as err:  # I have no idea at this point...
                print(err)
                raise "git gud"


def modifyConfig(Section, Variable, Value):
    document_folder = documentFolder()
    config_file = document_folder + pyWall_Ini
    config.read(configFile())
    if config.has_option(Section, Variable):
        config.set(Section, Variable, Value)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
            print("Variable modified")
    else:
        print(f"Unable to set {Value}")


def appendConfig(Section, Variable, Value: list):
    document_folder = documentFolder()
    config_file = document_folder + pyWall_Ini
    parser = configparser.SafeConfigParser()
    parser.read(configFile())
    beforeParse = getConfig(Section, Variable)
    current = parser.get(Section, Variable)
    if parser.has_option(Section, Variable):
        if "," in current:
            allValues = current.split(", ")
        else:
            allValues = [current]

        for x in Value:
            for z in allValues:
                if x == z:
                    from src.logger import actionLogger
                    actionLogger(f'Value "{x}" already in list, skipping...')
                    return False

            if "," not in str(current) and str(allValues) == "['']":
                allValues = [x]
            else:
                allValues.append(x)
        # Strip might be unnecessary now, but I don't wanna take it away due to a bug that happened while debugging ;w;#
        allValues = [x.strip() for x in allValues]
        allValues = ", ".join(allValues)
        parser.set(Section, Variable, allValues)
        with open(config_file, 'w') as f:
            parser.write(f)
            return True
    else:
        return False


def removeConfig(Section, Variable, Value: list):
    document_folder = documentFolder()
    config_file = document_folder + pyWall_Ini
    parser = configparser.SafeConfigParser()
    parser.read(configFile())
    beforeParse = parser.get(Section, Variable)
    if parser.has_option(Section, Variable):
        current = parser.get(Section, Variable)
        if current == "":
            return False
        for x in Value:
            skip = False
            if x.strip() not in current and len(Value) == 1:
                return False
            elif x.strip() not in current:
                from src.logger import actionLogger
                actionLogger(f'Value "{x}" not found in current variable, skipping...')
                skip = True
            if not skip:
                if "," in current:
                    allValues = current.split(", ")
                else:
                    allValues = [current]
                for z in allValues:
                    if z == x.strip():
                        allValues.remove(z)
            allValues = [x.strip() for x in allValues]
            allValues = ", ".join(allValues)
            parser.set(Section, Variable, allValues)
            current = parser.get(Section, Variable)
        if current == beforeParse:
            return False

        with open(config_file, 'w') as f:
            parser.write(f)
            return True
    else:
        return False


def configExists():
    document_folder = documentFolder()
    if os.path.exists(document_folder + pyWall_Ini):
        return True
    else:
        return False


def validateConfig(default_file=None):
    if default_file is None:
        default_file = default_config
    from src.logger import actionLogger
    if configExists():
        try:
            config.read(configFile())
        except configparser.ParsingError:
            default()
            time.sleep(0.1)
        actionLogger("-" * 50)
        for x in range(len(default_file.keys())):
            section = list(default_file.keys())[x]
            for option in default_file[section]:
                if config.has_option(section, option):
                    actionLogger(f'"{option}" validated')
                else:
                    actionLogger(f'Check failed for "{option}"')
                    actionLogger("-" * 50)
                    default()
        actionLogger("-" * 50)
        actionLogger("Updating version")
        modifyConfig("DEBUG", "version", default_file.get("DEBUG", "version")["version"])
        actionLogger("-" * 50)
        return True
    else:
        default()
