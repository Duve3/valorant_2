import pygame.freetype
from constants import courierFont
import constants


def createFont(color, size, *, fontLocation=courierFont):
    font = pygame.freetype.Font(fontLocation)
    font.size = size
    font.fgcolor = color  # NOQA:TYPO
    return font


class UIPopup:
    def __init__(self, pos, size):
        self.x = pos[0]
        self.y = pos[1]
        self.enabled = False
        self.surface = pygame.Surface(size=(size[0], size[1]))

    def resetSurface(self, givenSize=None):
        newSize = self.surface.get_size() if givenSize is None else givenSize
        self.surface = pygame.Surface(size=newSize)  # recreate surface

    def placeElements(self):  # the function for placing items
        self.surface.fill(constants.white)  # placeholder

    def draw(self, screen: pygame.Surface, redrawElements: bool = False):
        if self.enabled:
            if redrawElements:
                self.placeElements()
            screen.blit(self.surface, (self.x, self.y))


class InputField:
    def __init__(self, pos, size, charLimit: int = 20, font=createFont(constants.gray, 40, fontLocation="CourierPrimeCode-Regular.ttf")):
        self.x = pos[0]
        self.y = pos[1]
        self.active = False
        self.rect = pygame.Rect(pos, size)
        self.text = ""
        self.charLimit = charLimit
        self.font = font

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            elif event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    self.text = self.text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    self.text += event.unicode
