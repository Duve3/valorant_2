import pygame
import constants
from util import createFont, UIPopup, InputField
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
        self.loadingImageALPHA = self.loadingImage.get_alpha()
        self.userInput = False
        self.FONTwaitingForUserInput = createFont(constants.white, 40,
                                                  fontLocation="../assets/CourierPrimeCode-Regular.ttf")
        self.waitingUIRect = None

        # MAIN MENU
        self.FONTtopText = createFont(constants.white, 60, fontLocation="../assets/MonomaniacOne-Regular.ttf")
        self.playSize = 60
        self.playRect = None
        self.PolygonPlayPOINTS = [[0, 0], [50, 80], [250, 80], [300, 0]]
        self.PlayPolygonOffset = (self.display.get_rect().centerx - self.PolygonPlayPOINTS[len(self.PolygonPlayPOINTS) - 1][0] / 2, 0)
        for point in self.PolygonPlayPOINTS:
            point[0] += self.PlayPolygonOffset[0]
            point[1] += self.PlayPolygonOffset[1]

        self.playColor = constants.white
        self.PlayPolygonColor = constants.CustomRed
        self.inPlay = False

        # PLAY MENU
        self.joinRect = None
        self.FONTjoinButton = createFont(constants.white, 40, fontLocation="../assets/CourierPrimeCode-Regular.ttf")
        self.joinColorRect = constants.CustomRed
        self.joinColor = constants.white
        self.joinText = "JOIN"
        self.joinPadw = 160
        self.joinPadh = 40
        self.joinPadx = 80
        self.joinPady = 20
        self.customJoinRect = None
        self.joining = False
        self.InfoPopup = JoinPopup((self.display.get_rect().centerx - 300, 200), (600, 300))

    def run(self):
        while True:
            self.fpsClock.tick(60)
            allEvents = pygame.event.get()
            if self.InfoPopup.enabled:
                self.InfoPopup.IF.handleEvents(allEvents)
            for event in allEvents:
                if event.type == pygame.QUIT:
                    sys.exit()  # exit but better

                elif self.userInput is False and event.type == pygame.KEYDOWN or self.userInput is False and event.type == pygame.MOUSEBUTTONDOWN:  # detect player input
                    self.userInput = True

                elif event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    if self.userInput:
                        if self.playRect is not None:
                            if self.playRect.collidepoint(mx, my) and self.inPlay is False:
                                self.playColor = constants.lightBlue
                                self.playSize = 70
                            else:
                                self.playColor = constants.white
                                self.playSize = 60

                    if self.inPlay:
                        if self.customJoinRect is not None and self.joining is False:
                            if self.customJoinRect.collidepoint(mx, my):
                                self.joinColorRect = constants.CustomRed.lighten(50)
                            else:
                                self.joinColorRect = constants.CustomRed

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if self.userInput:

                        if self.playRect.collidepoint(mx, my):
                            if self.inPlay is False:
                                self.inPlay = True

                    if self.inPlay:
                        if self.customJoinRect is not None:
                            if self.customJoinRect.collidepoint(mx, my) and self.joining is False:
                                self.InfoPopup.enabled = True
                                self.joining = True
                                self.joinText = "JOINING"
                                self.joinColorRect = constants.CustomRed.darken(50)
                            elif self.InfoPopup is False:
                                self.InfoPopup.enabled = False
                                self.joining = False
                                self.joinText = "JOIN"

            if self.userInput:
                if self.loadingImageALPHA > 0:
                    self.loadingImageALPHA -= 3
                    self.loadingImage.set_alpha(self.loadingImageALPHA)
            else:
                self.waitingUIRect = self.FONTwaitingForUserInput.get_rect("Click anywhere to begin", size=40)
                self.waitingUIRect.centerx = self.display.get_rect().centerx
                self.waitingUIRect.y = 650

            if self.userInput:
                self.playRect = self.FONTtopText.get_rect("PLAY", size=self.playSize)
                self.playRect.centerx = self.display.get_rect().centerx
                self.playRect.y = 20

            if self.inPlay:
                self.playColor = constants.white
                self.PlayPolygonColor = constants.gray
                self.playSize = 70
                self.playRect = self.FONTtopText.get_rect("PLAY", size=self.playSize)
                self.playRect.centerx = self.display.get_rect().centerx
                self.playRect.y = 20

                self.joinRect = self.FONTjoinButton.get_rect(self.joinText, size=40)
                self.joinRect.centerx = self.display.get_rect().centerx
                self.joinRect.y = 650

            # RENDERING
            if self.userInput and self.loadingImageALPHA < 1:
                self.display.fill(constants.black)
            else:
                self.display.fill(constants.logoColor)

            if self.inPlay:
                self.display.fill(constants.logoColor)

            loadingImgRect = self.loadingImage.get_rect()
            loadingImgRect.centerx = self.display.get_rect().centerx
            self.display.blit(self.loadingImage, loadingImgRect)

            if not self.userInput:
                self.FONTwaitingForUserInput.render_to(self.display, self.waitingUIRect, "Click anywhere to begin")

            if self.userInput:
                pygame.draw.polygon(self.display, self.PlayPolygonColor, self.PolygonPlayPOINTS)
                self.FONTtopText.render_to(self.display, self.playRect, "PLAY", fgcolor=self.playColor,
                                           size=self.playSize)

                if self.inPlay:
                    self.InfoPopup.draw(screen=self.display, redrawElements=True)
                    if not self.joining:
                        self.customJoinRect = pygame.Rect(self.joinRect.x - self.joinPadx,
                                                          self.joinRect.y - self.joinPady,
                                                          self.joinRect.width + self.joinPadw,
                                                          self.joinRect.height + self.joinPadh)

                    pygame.draw.rect(self.display, self.joinColorRect, self.customJoinRect)
                    self.FONTjoinButton.render_to(self.display, self.joinRect, self.joinText, fgcolor=self.joinColor,
                                                  size=40)

            pygame.display.flip()


class JoinPopup(UIPopup):
    def __init__(self, pos, size):
        super().__init__(pos=pos, size=size)
        font = createFont(constants.white, 40, fontLocation="../assets/CourierPrimeCode-Regular.ttf")
        self.IF = InputField((size[0] // 2 - 263, 60), (525, 40), constants.gray, (175, 175, 175), font, charLimit=20, surfaceOffset=pos, placeHolderText="Username")

    def placeElements(self):
        self.surface.fill(constants.black)
        FONTtext = createFont(constants.white, 40, fontLocation="../assets/CourierPrimeCode-Regular.ttf")
        FONTtext.render_to(self.surface, (self.surface.get_rect().centerx - FONTtext.get_rect("Enter Username: ", size=40).centerx, 20), "Enter Username: ")
        self.IF.draw(self.surface)
