import pygame
from main_menu import MainMenu
import ctypes



def main():  # the main game
    # setting the logo for the game
    myappid = u'alterragames.valorant2d.testing.main'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    pygame.init()

    RES = [1280, 720]
    ico = pygame.image.load('../assets/V2DLOGOv2.png')
    pygame.display.set_icon(ico)
    pygame.display.set_caption("Valorant_2(d)")
    window = pygame.display.set_mode(RES)
    fpsClock = pygame.time.Clock()
    mm = MainMenu(window=window, fpsClock=fpsClock, width=RES[0], height=RES[1])


    MainMenu.run(mm)


if __name__ == "__main__":  # entry point
    main()
