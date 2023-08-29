import pygame
import pygame_wrapper as pgw
from main_menu import MainMenu
from disclaimer_menu import DisclaimerMenu
import ctypes
import sys
import os


def main(prod: bool = False):  # the main game
    # setting the logo for the game
    myappid = u'alterra.games.valorant2d.testing'  # arbitrary string
    if os.name != "posix":
        # might say "code is unreachable" because your not on windows, as this only works on windows
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) 

    pygame.init()
    if not getattr(pygame, "IS_CE", False):
        print("FAILED TO FIND PYGAME-CE INSTALL, SOME FEATURES MAY NOT WORK CORRECTLY!\nINSTALL PYGAME-CE WITH 'pip uninstall pygame' AND 'pip install pygame-ce'")
        print("The reason pygame-ce is required because it is superior in most cases with better updates, its docs can be found at https://pyga.me/docs/")
        if prod:
            print("For safety reasons the game will now close")
            sys.exit()
        else:
            print("The game will not close, not prod environment")
    
    if not getattr(pgw, "GameType", False):
        print("dude why are you emulating pgw?")
        if prod:
            print("closing game because pgw is a required asset")
            sys.exit()
        else:
            print("yeah im not closing it but my guy why are you running debugging mode and emulating it???")


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
