import logging
import pygame_wrapper as pgw
import os


PlayerListSTART = "!PLAYERLISTSTART"
PlayerListEND = "!PLAYERLISTEND"
PlayerSTART = "!PLAYERSTART"
PlayerEND = "!PLAYEREND"
DisconnectMSG = "!!!Disconnect"
DisconnectRES = "Disconnected"
encoding = "utf-8"


def setupLogger(logger: logging.Logger, level: int = logging.DEBUG):
    logFormatter = logging.Formatter(
        "%(levelname)s (%(asctime)s) - %(name)s: %(message)s (Line: %(lineno)d [%(filename)s])",
        "%m/%d %H:%M:%S")

    
    if not os.path.exists("./logs/"):
        os.mkdir("./logs")
    
    if not os.path.exists("./logs/console.log"):
        # basically just making the file
        with open("./logs/console.log", "x"):
            pass
    
    fileHandler = logging.FileHandler("{0}/{1}.log".format("./logs", "console"))
    fileHandler.setFormatter(logFormatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)

    logger.level = level
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger


black = pgw.Color(0, 0, 0)
white = pgw.Color(255, 255, 255)
red = pgw.Color(255, 0, 0)
green = pgw.Color(0, 255, 0)
blue = pgw.Color(0, 0, 255)
