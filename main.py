import pygame

pygame.init()

WIDTH = 800; HEIGHT = 600
screen = pygame.display.set_mode( [WIDTH, HEIGHT] )


def isGameClosed():
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            return True
    return False    



while(True):
    if(isGameClosed()):
        break

    screen.fill( (0, 0, 0) )

    # Update the screen
    pygame.display.flip()

pygame.quit()