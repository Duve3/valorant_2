import pygame
import pygame_wrapper as pgw
from pygame_wrapper import Font
import logging
import constants
import sys


class DisclaimerMenu(pgw.MenuType):
    """
    Disclaimer Menu
    """

    def __init__(self, window: pygame.Surface, fpsClock: pygame.time.Clock, logger: logging.Logger):
        super().__init__(window, fpsClock)

        self.userInput = False
        with open("disclaimer.txt", "r") as df:
            self.TEXT_Disclaimer = df.read()
        self.FONT_Disclaimer = Font("../assets/CourierPrimeCode-Regular.ttf", 20, constants.white)
        self.FONT_Top = Font("../assets/MonomaniacOne-Regular.ttf", 40, constants.white)

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
