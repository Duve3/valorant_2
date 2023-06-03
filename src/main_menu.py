import pygame
import constants
from util import createFont
import sys


class MainMenu:
    """
    Main Menu
    """

    def __init__(self, window: pygame.Surface, fpsClock: pygame.time.Clock, width: int, height: int):
        self.res = (width, height)
        self.display: pygame.Surface = window
        self.fpsClock: pygame.time.Clock = fpsClock

        # LOADING SCREEN:
        self.loadingImage = pygame.image.load("../assets/valorantLoading.png").convert_alpha()
        #self.loadingImage = pygame.transform.smoothscale(self.loadingImage, [width, height])
        self.loadingImageALPHA = self.loadingImage.get_alpha()
        self.userInput = False
        self.FONTwaitingForUserInput = createFont(constants.white, 40, fontLocation="../assets/CourierPrimeCode-Regular.ttf")
        self.waitingUIRect = None

        # MAIN MENU
        self.FONTtopText = createFont(constants.white, 60, fontLocation="../assets/MonomaniacOne-Regular.ttf")
        self.playSize = 60
        self.playRect = None
        self.playColor = constants.white
        self.inPlay = False  # TODO: inPlay is not being set when mouse click on play menu

    def run(self):
        while True:
            self.fpsClock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # exit but better

                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # detect player input
                    self.userInput = True

                elif event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    if self.userInput:
                        if self.playRect is not None:
                            if self.playRect.collidepoint(mx, my):
                                self.playColor = constants.lightBlue
                                self.playSize = 70
                            else:
                                self.playColor = constants.white
                                self.playSize = 60

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if self.userInput:
                        if self.playRect.collidepoint(mx, my):
                            if self.inPlay is False:
                                self.inPlay = True


            if self.userInput and self.loadingImageALPHA < 1:
                self.display.fill(constants.black)
            else:
                self.display.fill(constants.logoColor)

            if self.userInput:
                if self.loadingImageALPHA > 0:
                    self.loadingImageALPHA -= 2
                    self.loadingImage.set_alpha(self.loadingImageALPHA)
            else:
                self.waitingUIRect = self.FONTwaitingForUserInput.get_rect("Waiting for User Input...", size=40)
                self.waitingUIRect.centerx = self.display.get_rect().centerx
                self.waitingUIRect.y = 50
                self.FONTwaitingForUserInput.render_to(self.display, self.waitingUIRect, "Waiting for User Input...")

            if self.userInput:
                self.playRect = self.FONTtopText.get_rect("PLAY", size=self.playSize)
                self.playRect.centerx = self.display.get_rect().centerx
                self.playRect.y = 30


            if self.inPlay:
                self.playColor = constants.gray


            # RENDERING
            loadingImgRect = self.loadingImage.get_rect()
            loadingImgRect.centerx = self.display.get_rect().centerx
            self.display.blit(self.loadingImage, loadingImgRect)

            if not self.userInput:
                self.FONTwaitingForUserInput.render_to(self.display, self.waitingUIRect, "Waiting for User Input...")

            if self.userInput:
                self.FONTtopText.render_to(self.display, self.playRect, "PLAY", fgcolor=self.playColor,
                                           size=self.playSize)

            pygame.display.flip()

            print(f"{self.inPlay = }")
