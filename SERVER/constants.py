import logging


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

    fileHandler = logging.FileHandler("{0}/{1}.log".format("./logs", "console"))
    fileHandler.setFormatter(logFormatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)

    logger.level = level
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger
