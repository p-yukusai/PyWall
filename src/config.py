import pathlib
import sys
import os
import configparser

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
        pass
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


# Sections #
sections = ["FILETYPE", "GUI", "DEBUG"]
# File #
sets_file = ["accepted_types", "blacklisted_names", "recursive"]
set_default_file = [".exe", "", "True"]
# Gui #
sets_gui = ["advanced_mode", "stylesheet", "first_run"]
set_default_gui = ["False", "dark_red.xml", "True"]
# Debug #
sets_debug = ["create_logs", "create_exception_logs", "version", "shell"]
set_default_debug = ["False", "True", "v.1.3", "False"]
# All sets #
sets = [sets_file, sets_gui, sets_debug]
sets_default = [set_default_file, set_default_gui, set_default_debug]


def default():
    document_folder = documentFolder()
    config_file = document_folder + pyWall_Ini
    value_int = 0
    # This was coded making heavy use of sleep deprivation ( •̀ ω •́ )y #
    for x in sections:
        if not config.has_section(x):
            config.add_section(x)
    for x in range(len(sections)):
        sec = sections[x]
        for se in sets[x]:
            if config.has_option(sec, se):  # Sec(tions), Se(ts) #
                if len(sets_default[x]) > value_int:
                    value_int += 1
                if len(sets_default[x]) == value_int:
                    value_int = 0
            if not config.has_option(sec, se):
                config.set(sec, se, sets_default[x][value_int])
                if len(sets_default[x]) > value_int:
                    value_int += 1
                if len(sets_default[x]) == value_int:
                    value_int = 0
    # Write to Config.ini #
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def makeDefault():
    document_folder = documentFolder()
    config_folder = document_folder + PyWall
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    default()


def getConfig(Section, Variable, *Index: str):  # Index is a string now, what a weird world we live in (つ ◕_◕ )つ #
    config.read(configFile())
    if Section == '?':
        print(sections)
    if Variable == '?':
        sect = sections.index(Section)
        print(sets[sect])
    if Index:
        # It do be that way ┑(￣Д ￣)┍ #
        try:
            indexValue = ''.join(Index)
            value = config[Section][Variable]
            List = value.split(', ')
            if "len" in Index:
                return len(List)
            return List[int(indexValue)]
        except KeyError:
            print("-" * 50)
            print(sections)
            print("-" * 50)
            print(sets)
            print("-" * 50)
            print("だめだね、だめよ、だめなのよ")  # あんたが、好きで好きすぎて　#
            return False

    if config.has_option(Section, Variable):
        return config[Section][Variable]
    else:
        if Section or Variable == "?":
            return False
        else:
            # Reminders are important y'know! #
            print('Either the Section or the Variable does not exist, if you need a reminder put a "?" on either.')
        return False


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


def validateConfig():
    from src.logger import actionLogger
    document_folder = documentFolder()
    if os.path.exists(document_folder + pyWall_Ini):
        config.read(configFile())
        print("-" * 50)
        for x in range(len(sections)):
            sec = sections[x]
            for se in sets[x]:
                if config.has_option(sec, se):
                    actionLogger(f'"{se}" validated')
                else:
                    actionLogger(f'Check failed for "{se}"')
                    print("-" * 50)
                    return False
        print("-" * 50)
        actionLogger("Updating version")
        modifyConfig("DEBUG", "version", set_default_debug[2])
        print("-" * 50)
        return True
    else:
        try:
            makeDefault()
        except Exception as Argument:
            from src.logger import logException
            logException(Argument)
            return False
