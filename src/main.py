import pygame
from main_menu import MainMenu


def main():  # the main game
    pygame.init()

    RES = [1280, 720]
    window = pygame.display.set_mode(RES)
    fpsClock = pygame.time.Clock()

    # probably run mainMenu here but im not done with it
    mm = MainMenu(window=window, fpsClock=fpsClock, width=RES[0], height=RES[1])
    MainMenu.run(mm)


if __name__ == "__main__":  # entry point
    main()
