"""
Loads the settings INI file into a variable that can then be imported.
"""
import configparser

SETTINGS = configparser.ConfigParser()
SETTINGS.read("settings.ini")

GENERAL = SETTINGS["GENERAL"]
