import pygame
import constants
from util import createFont


class MainMenu:
    """
    Main Menu
    """

    def __init__(self, window: pygame.Surface, fpsClock: pygame.time.Clock, width: int, height: int):
        self.res = (width, height)
        self.display: pygame.Surface = window
        self.fpsClock: pygame.time.Clock = fpsClock
        self.testRectangle = pygame.Rect(15, 15, 50, 50)

        # LOADING SCREEN:
        self.loadingImage = pygame.image.load("../assets/valorantLoading.png").convert_alpha()
        self.loadingImage = pygame.transform.smoothscale(self.loadingImage, [width, height])
        self.loadingImageALPHA = self.loadingImage.get_alpha()
        self.userInput = False
        self.FONTwaitingForUserInput = createFont(constants.white, 40, fontLocation="../assets/CourierPrimeCode-Regular.ttf")

    def run(self):
        while True:
            self.fpsClock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # exit but better

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # detect player input
                    self.userInput = True

            self.display.fill(constants.black)

            self.display.blit(self.loadingImage, [0, 0])
            if self.userInput:
                if self.loadingImageALPHA > 0:
                    self.loadingImageALPHA -= 2
                    self.loadingImage.set_alpha(self.loadingImageALPHA)
            else:
                self.FONTwaitingForUserInput.render_to(self.display, [self.res[0]//2 - 250, 50], "Waiting for User Input...")


            pygame.display.flip()

