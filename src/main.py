import pygame
from main_menu import MainMenu
from disclaimer_menu import DisclaimerMenu
import ctypes


def main():  # the main game
    # setting the logo for the game
    myappid = u'alterra.games.valorant2d.testing'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    pygame.init()

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
    main()
