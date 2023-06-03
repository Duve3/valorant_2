import pygame
from main_menu import MainMenu


def main():  # the main game
    pygame.init()

    RES = [500, 500]
    window = pygame.display.set_mode(RES)
    fpsClock = pygame.time.Clock()

    # probably run mainMenu here but im not done with it
    mm = MainMenu(window=window, fpsClock=fpsClock)
    MainMenu.run(mm)


if __name__ == "__main__":  # entry point
    main()
