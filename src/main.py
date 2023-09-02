import pygame
import pygame_wrapper as pgw
from pygame_wrapper.logging import setupLogging
from main_menu import MainMenu
from disclaimer_menu import DisclaimerMenu
import ctypes
import sys
import os
import logging


def main(logger: logging.Logger, prod: bool = False):  # the main game
    logger.debug("exc main started")
    # setting the logo for the game
    org = "alterragames"
    game = "valorant2d"
    myappid = u'alterragames.valorant2d.testing'  # arbitrary string
    if os.name != "posix":
        # might say "code is unreachable" because your not on windows, as this only works on windows
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) 

    logger.debug("initing + checking attrs")
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

    logger.debug("defining vars, setting icon + caption, and making menus")
    RES = [1280, 720]
    usepath = pygame.system.get_pref_path(org, game)
    # TODO: convert all files to use the pref path using either pygame (system.get_pref_path) or platformdir (probably better) but using pygame would lower the amount of libraries
    ico = pygame.image.load('../assets/V2DLOGOv2.png')
    pygame.display.set_icon(ico)
    pygame.display.set_caption("Valorant_2(d)")
    window = pygame.display.set_mode(RES)
    fpsClock = pygame.time.Clock()
    mm = MainMenu(window=window, fpsClock=fpsClock, logger=logger)
    dm = DisclaimerMenu(window=window, fpsClock=fpsClock, logger=logger)

    logger.debug("running menus")
    dm.run()
    mm.userInput = True
    mm.run()

    logger.debug("main exc finished")


if __name__ == "__main__":  # entry point (might have to change when exe is made)
    logger = setupLogging("v2d-thread-main")
    main(logger, prod=False)
