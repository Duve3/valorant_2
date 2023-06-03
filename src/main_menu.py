import pygame


class MainMenu:
    """
    Main Menu
    """

    def __init__(self, window: pygame.Surface, fpsClock: pygame.time.Clock):
        self.display: pygame.Surface = window
        self.fpsClock: pygame.time.Clock = fpsClock

    def run(self):
        while True:
            self.fpsClock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # exit but better

            pygame.draw.rect(self.display, )

            pygame.display.flip()

