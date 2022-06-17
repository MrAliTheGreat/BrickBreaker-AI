import math
import pygame
from sympy import degree


def calculateAngle(start_x, start_y, end_x, end_y):
    if(end_x == start_x):
        return math.pi / 2
      
    angle = math.atan((end_y - start_y) / (end_x - start_x))
    if(angle <= 0):
        return abs(angle)

    return math.pi - angle



pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600
FPS = 30
MOVE_SPEED = 5


screen = pygame.display.set_mode( [SCREEN_WIDTH, SCREEN_HEIGHT] )
running = True
moveBall = False; drawIndicator = True; detectMouseClick = True

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN and detectMouseClick):
            moveBall = True; drawIndicator = False; detectMouseClick = False
            angle = calculateAngle(
                start_x = BALL_X,
                start_y = BALL_Y,
                end_x = pygame.mouse.get_pos()[0],
                end_y = pygame.mouse.get_pos()[1]
            )


    screen.fill( (0, 0, 0) )

    if(moveBall):
        if((BALL_X >= SCREEN_WIDTH or BALL_X <= 0) and (BALL_Y >= SCREEN_HEIGHT or BALL_Y <= 0)):
            angle = math.pi + angle        
        elif(BALL_X >= SCREEN_WIDTH or BALL_X <= 0):
            angle = math.pi - angle
        elif(BALL_Y >= SCREEN_HEIGHT or BALL_Y <= 0):
            angle = 2 * math.pi - angle

        BALL_X += MOVE_SPEED * math.cos(angle)
        BALL_Y -= MOVE_SPEED * math.sin(angle)

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