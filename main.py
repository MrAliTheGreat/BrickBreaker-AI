import math
import pygame


def applyAngleRestriction(angle):
    if(radian2degree(angle) >= 170):
        return degree2radian(170)
    if(radian2degree(angle) <= 10):
        return degree2radian(10)
    return angle

def calculateAngle(start_x, start_y, end_x, end_y):
    if(end_x == start_x):
        return math.pi / 2
    if(end_y >= start_y):
        if(end_x < start_x):
            return applyAngleRestriction(math.pi)
        else:
            return applyAngleRestriction(0)
      
    angle = math.atan((end_y - start_y) / (end_x - start_x))
    if(angle <= 0):
        return applyAngleRestriction(abs(angle))

    return applyAngleRestriction(math.pi - angle)

def radian2degree(radian):
    return radian * 180 / math.pi

def degree2radian(degree):
    return degree * math.pi / 180

def moveBall(current_x, current_y, moveAngle):
    if((current_x >= SCREEN_WIDTH or current_x <= 0) and (current_y <= 0)):
        moveAngle = math.pi + moveAngle        
    elif(current_x >= SCREEN_WIDTH or current_x <= 0):
        moveAngle = math.pi - moveAngle
    elif(current_y <= 0):
        moveAngle = 2 * math.pi - moveAngle
    elif(current_y >= SCREEN_HEIGHT):
        moveAngle = -1

    return current_x + MOVE_SPEED * math.cos(moveAngle), current_y - MOVE_SPEED * math.sin(moveAngle), moveAngle


pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600
FPS = 30
MOVE_SPEED = 5
INDICATOR_LENGTH = 150
BALL_X = SCREEN_WIDTH // 2; BALL_Y = 590


screen = pygame.display.set_mode( [SCREEN_WIDTH, SCREEN_HEIGHT] )
running = True
moveBallFlag = False; drawIndicatorFlag = True; detectMouseClickFlag = True

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN and detectMouseClickFlag):
            moveBallFlag = True; drawIndicatorFlag = False; detectMouseClickFlag = False
            moveAngle = calculateAngle(
                start_x = BALL_X,
                start_y = BALL_Y,
                end_x = pygame.mouse.get_pos()[0],
                end_y = pygame.mouse.get_pos()[1]
            )


    screen.fill( (0, 0, 0) )

    if(moveBallFlag):
        BALL_X, BALL_Y, moveAngle = moveBall(
            current_x = BALL_X,
            current_y = BALL_Y,
            moveAngle = moveAngle
        )
        if(moveAngle == -1):
            moveBallFlag = False; drawIndicatorFlag = True; detectMouseClickFlag = True
            BALL_Y = 590

    pygame.draw.circle(
        surface = screen,
        color = pygame.Color("#FDA172"),
        center = (BALL_X, BALL_Y),
        radius = 5
    )
    
    if(drawIndicatorFlag):
        indicatorAngle = calculateAngle(
            start_x = BALL_X,
            start_y = BALL_Y,
            end_x = pygame.mouse.get_pos()[0],
            end_y = pygame.mouse.get_pos()[1]
        )
        
        pygame.draw.line(
            surface = screen,
            color = pygame.Color("#FFFFFF"),
            start_pos = (
                BALL_X + 7 * math.cos(indicatorAngle),
                BALL_Y - 7 * math.sin(indicatorAngle)
            ),
            end_pos = (
                BALL_X + (7 + INDICATOR_LENGTH) * math.cos(indicatorAngle),
                BALL_Y - (7 + INDICATOR_LENGTH) * math.sin(indicatorAngle)
            ),
            width = 2
        )

    # Update the screen
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()