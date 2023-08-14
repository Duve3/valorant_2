from pygame import Color
import logging


class __CustomColor(Color):
    def __init__(self, colorTuple, a=255):  # accepts type list too
        Color.__init__(self, colorTuple[0], colorTuple[1], colorTuple[2], a)
        self.color = colorTuple

    def darken(self, offset: int) -> list:
        darkColor = [0, 0, 0]  # [0] * 3
        for i, c in enumerate(self.color):
            nc = c - offset
            darkColor[i] = nc if nc >= 0 else 0

        return darkColor

    def lighten(self, offset: int) -> list:
        lighterColor = [0, 0, 0]  # [0] * 3
        for i, c in enumerate(self.color):
            nc = c + offset
            lighterColor[i] = nc if nc <= 255 else 255

        return lighterColor


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
grayRed = (150, 0, 0)
green = (0, 255, 0)
grayGreen = (0, 150, 0)
lightBlue = (0, 175, 255)
blue = (0, 0, 255)
gray = (150, 150, 150)
whiteGray = (200, 200, 200)
yellow = (255, 255, 0)
orange = (255, 150, 0)

logoColor = (15, 25, 35)
CustomRed = __CustomColor((255, 70, 82))

colorList = [white, black, red, grayRed, green, grayGreen, blue, gray, whiteGray, yellow, orange]

courierFont = "CourierPrimeCode-Regular.ttf"


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
