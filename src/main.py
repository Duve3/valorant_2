import pygame
from main_menu import MainMenu
from disclaimer_menu import DisclaimerMenu
import ctypes
import sys


def main(prod: bool = False):  # the main game
    # setting the logo for the game
    myappid = u'alterra.games.valorant2d.testing'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    pygame.init()
    if not getattr(pygame, "IS_CE", False):
        print("FAILED TO FIND PYGAME-CE INSTALL, SOME FEATURES MAY NOT WORK CORRECTLY!\nINSTALL PYGAME-CE WITH 'pip uninstall pygame' AND 'pip install pygame-ce'")
        print("The reason pygame-ce is required because it is superior in most cases with better updates, its docs can be found at https://pyga.me/docs/")
        if prod:
            print("For safety reasons the game will now close")
            sys.exit()
        else:
            print("The game will not close due to this not be a PROD environment")

    RES = [1280, 720]
    ico = pygame.image.load('../assets/V2DLOGOv2.png')
    pygame.display.set_icon(ico)
    pygame.display.set_caption("Valorant_2(d)")
    window = pygame.display.set_mode(RES)
    fpsClock = pygame.time.Clock()
    mm = MainMenu(window=window, fpsClock=fpsClock, width=RES[0], height=RES[1])
    dm = DisclaimerMenu(window=window, fpsClock=fpsClock, width=RES[0], height=RES[1])

    dm.run()
    mm.userInput = True
    mm.run()


if __name__ == "__main__":  # entry point
    main(prod=False)
