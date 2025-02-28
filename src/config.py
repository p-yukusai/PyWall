"""
Module for handling configuration settings for PyWall.
"""

import pathlib
import sys
import os
import configparser
import ctypes.wintypes
from src.logger import actionLogger

PYWALL_INI = "\\PyWall\\Config.ini"
PYWALL = "\\PyWall"

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
        "version": "v1.7.3",
        "shell": "False"
    }
}

def document_folder():
    """
    Get the path to the user's document folder.
    """
    CSIDL_PERSONAL = 5  # My Documents
    SHGFP_TYPE_CURRENT = 0  # Get current value, not default
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

def script_folder():
    """
    Get the path to the script folder.
    """
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(".")

def config_file():
    """
    Get the configuration file path.
    """
    document_folder_path = document_folder()
    config_path = os.path.join(document_folder_path, PYWALL_INI)
    if os.path.exists(config_path):
        return config_path
    make_default()
    return config_path

def make_default():
    """
    Create the default configuration.
    """
    document_folder_path = document_folder()
    config_folder = os.path.join(document_folder_path, PYWALL)
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    config_path = os.path.join(config_folder, "Config.ini")
    config = configparser.ConfigParser()
    for section, options in default_config.items():
        config.add_section(section)
        for option, value in options.items():
            config.set(section, option, value)
    with open(config_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    actionLogger("Default configuration created")

def get_config(section, variable, *extra_args):
    """
    Get a configuration value.
    """
    config = configparser.ConfigParser()
    config.read(config_file())
    if extra_args:
        index_value = ''.join(extra_args)
        value = config[section][variable]
        value_list = value.split(', ')
        return value_list[int(index_value)]
    return config[section][variable]

def modify_config(section, variable, value):
    """
    Modify a configuration value.
    """
    config = configparser.ConfigParser()
    config.read(config_file())
    if config.has_option(section, variable):
        config.set(section, variable, value)
        with open(config_file(), 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        actionLogger(f"Variable '{variable}' modified in section '{section}'")
    else:
        actionLogger(f"Variable '{variable}' not found in section '{section}'")

def append_config(section, variable, value: list):
    """
    Append a value to a configuration list.
    """
    config = configparser.ConfigParser()
    config.read(config_file())
    if config.has_option(section, variable):
        current = config.get(section, variable)
        all_values = current.split(", ") if "," in current else [current]
        for x in value:
            if x not in all_values:
                all_values.append(x)
        all_values = ", ".join(all_values)
        config.set(section, variable, all_values)
        with open(config_file(), 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        actionLogger(f"Values '{value}' appended to variable '{variable}' in section '{section}'")
        return True
    return False

def remove_config(section, variable, value: list):
    """
    Remove a value from a configuration list.
    """
    config = configparser.ConfigParser()
    config.read(config_file())
    if config.has_option(section, variable):
        current = config.get(section, variable)
        all_values = current.split(", ") if "," in current else [current]
        for x in value:
            if x in all_values:
                all_values.remove(x)
        all_values = ", ".join(all_values)
        config.set(section, variable, all_values)
        with open(config_file(), 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        actionLogger(f"Values '{value}' removed from variable '{variable}' in section '{section}'")
        return True
    return False

def config_exists():
    """
    Check if the configuration file exists.
    """
    return os.path.exists(config_file())

def validate_config(default_file=None):
    """
    Validate the configuration file.
    """
    if default_file is None:
        default_file = default_config
    if config_exists():
        config = configparser.ConfigParser()
        try:
            config.read(config_file())
        except configparser.ParsingError:
            make_default()
    parser = configparser.ConfigParser()
    parser.read(config_file())
    current = parser.get(section, variable)
    if parser.has_option(section, variable):
        if "," in current:
            all_values = current.split(", ")
        else:
            all_values = [current]

        for x in value:
            for z in all_values:
                if x == z:
                    actionLogger(f'Value "{x}" already in list, skipping...')
                    return False

            if "," not in str(current) and str(all_values) == "['']":
                all_values = [x]
            else:
                all_values.append(x)
        # Strip might be unnecessary now, but I don't wanna take it away due to a bug that happened while debugging ;w;#
        all_values = [x.strip() for x in all_values]
        all_values = ", ".join(all_values)
        parser.set(section, variable, all_values)
        with open(config_file, 'w', encoding='utf-8') as f:
            parser.write(f)
            return True
    return False
        if "," in current:
            allValues = current.split(", ")
def remove_config(section, variable, value: list):
    """
    Remove a value from a configuration list.
    """
    document_folder = document_folder()
    config_file = document_folder + PYWALL_INI
    parser = configparser.ConfigParser()
    parser.read(config_file())
    before_parse = parser.get(section, variable)
    if parser.has_option(section, variable):
        current = parser.get(section, variable)
        if current == "":
            return False
        for x in value:
            skip = False
            if x.strip() not in current and len(value) == 1:
                return False
            if x.strip() not in current:
                actionLogger(f'Value "{x}" not found in current variable, skipping...')
                skip = True
            if not skip:
                if "," in current:
                    all_values = current.split(", ")
                else:
                    all_values = [current]
                for z in all_values:
                    if z == x.strip():
                        all_values.remove(z)
            all_values = [x.strip() for x in all_values]
            all_values = ", ".join(all_values)
            parser.set(section, variable, all_values)
            current = parser.get(section, variable)
        if current == before_parse:
            return False

        with open(config_file, 'w', encoding='utf-8') as f:
            parser.write(f)
            return True
    return False
                return False
def config_exists():
    """
    Check if the configuration file exists.
    """
    document_folder = document_folder()
    return os.path.exists(document_folder + PYWALL_INI)
                    allValues = current.split(", ")
                else:
def validate_config(default_file=None):
    """
    Validate the configuration file.
    """
    if default_file is None:
        default_file = default_config
    if config_exists():
        try:
            config.read(config_file())
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
        modify_config("DEBUG", "version", default_file.get("DEBUG", "version")["version"])
        actionLogger("-" * 50)
        return True
    default()
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
