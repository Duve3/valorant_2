import pygame
from button import Button

pygame.init()
lockinscreen = pygame.display.set_mode([400, 400])
agents = ["jett"]
buttons = []
for x in agents:
    button = Button("Blue", 20, 20, 20, 20, x)
    buttons.append(button)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # also tabbed in the following code because it seems like it should be tabbed in (using event.type)
        mouse = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(lockinscreen)
            if button.isOver(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                pass  # someone just left this empty so im turning it into a pass

    pygame.display.flip()

pygame.quit()
  
  
  
  
  
  
