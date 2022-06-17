import math
import pygame
from sympy import degree


pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600
FPS = 30
MOVE_SPEED = 5


screen = pygame.display.set_mode( [SCREEN_WIDTH, SCREEN_HEIGHT] )
running = True
moveBall = False; drawIndicator = True

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            drawIndicator = False
            moveBall = True

            if(pygame.mouse.get_pos()[0] == BALL_X):
                moveDegree = math.pi / 2
            else:
                moveDegree = math.atan((pygame.mouse.get_pos()[1] - BALL_Y) / (pygame.mouse.get_pos()[0] - BALL_X))
                if(moveDegree <= 0):
                    moveDegree = abs(moveDegree)
                else:
                    moveDegree = math.pi - moveDegree


    screen.fill( (0, 0, 0) )

    if(moveBall):
        BALL_X += MOVE_SPEED * math.cos(moveDegree)
        BALL_Y -= MOVE_SPEED * math.sin(moveDegree)
        print(f"moveDegree: {moveDegree * 180 / math.pi}")
        print(f"Ball --> x: {BALL_X}, y: {BALL_Y}")

    else:
        BALL_X = SCREEN_WIDTH // 2; BALL_Y = 590

    pygame.draw.circle(
        surface = screen,
        color = pygame.Color("#FDA172"),
        center = (BALL_X, BALL_Y),
        radius = 5
    )
    
    if(drawIndicator):
        pygame.draw.line(
            surface = screen,
            color = pygame.Color("#FFFFFF"),
            start_pos = (BALL_X, BALL_Y - 7),
            end_pos = pygame.mouse.get_pos(),
            width = 2
        )

    # Update the screen
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()