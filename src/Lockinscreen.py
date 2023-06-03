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

    mouse = pygame.mouse.get_pos()
    for button in buttons:
        button.draw(lockinscreen)
        if button.isOver(mouse) and event.type == pygame.MOUSEBUTTONDOWN:

    pygame.display.flip()

pygame.quit()
  
  
  
  
  
  
