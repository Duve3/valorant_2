import pygame
import constants
from util import createFont, InputField, BetterFont
import sys


class DisclaimerMenu:
    """
    Disclaimer Menu
    """

    def __init__(self, window: pygame.Surface, fpsClock: pygame.time.Clock, width: int, height: int):
        self.res = (width, height)
        self.screen: pygame.Surface = window
        self.fpsClock: pygame.time.Clock = fpsClock

        self.userInput = False
        with open("disclaimer.txt", "r") as df:
            self.TEXT_Disclaimer = df.read()
        self.FONT_Disclaimer = BetterFont(constants.white, 20, "../assets/CourierPrimeCode-Regular.ttf")
        self.FONT_Top = BetterFont(constants.white, 40, "../assets/MonomaniacOne-Regular.ttf")

    def run(self):
        while True:
            self.fpsClock.tick(60)
            allEvents = pygame.event.get()
            for event in allEvents:
                if event.type == pygame.QUIT:
                    sys.exit()  # exit but better

                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.userInput = True
            # logic
            if self.userInput:
                return

            # rendering
            self.screen.fill(constants.black)
            self.FONT_Top.render_to(self.screen, (self.FONT_Top.get_center(self.screen, "DISCLAIMER:", x=True).x, 5), "DISCLAIMER:")
            self.FONT_Disclaimer.multiline_render_to(self.screen, (10, 40), self.TEXT_Disclaimer)
            self.FONT_Top.render_to(self.screen, (self.FONT_Top.get_center(self.screen, "PRESS ANY BUTTON TO CONTINUE", x=True).x, 680), "PRESS ANY BUTTON TO CONTINUE")

            pygame.display.flip()
