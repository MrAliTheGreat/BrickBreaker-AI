import math
import pygame


class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = -1
        self.isMoving = False

    def updateBall(self, new_x, new_y, new_angle, new_isMoving):
        self.x = new_x
        self.y = new_y
        self.angle = new_angle
        self.isMoving = new_isMoving

    def startMoving(self, new_angle):
        self.angle = new_angle 
        self.isMoving = True     



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

textFont = pygame.font.SysFont("Comic Sans MS", 20)

SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600
FPS = 30
MOVE_SPEED = 5
INDICATOR_LENGTH = 150

screen = pygame.display.set_mode( [SCREEN_WIDTH, SCREEN_HEIGHT] )

running = True
initialMovement = False; drawIndicatorFlag = True; detectMouseClickFlag = True
balls = [Ball(x = SCREEN_WIDTH // 2, y = 590)]
ball_starting_point_x = SCREEN_WIDTH // 2
cyclesPast = 0
score = 1; numBallsInPlay = 1

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN and detectMouseClickFlag):
            starting_ball_missing = True; drawIndicatorFlag = False; detectMouseClickFlag = False
            starting_angle = calculateAngle(
                start_x = ball_starting_point_x,
                start_y = 590,
                end_x = pygame.mouse.get_pos()[0],
                end_y = pygame.mouse.get_pos()[1]
            )            
            balls[0].startMoving(starting_angle)
            initialMovement = True
            score += 1


    screen.fill( (0, 0, 0) )

    areBallsMoving = False; cyclesPast += 1
    for ball in balls:
        if(ball.isMoving):
            new_isMoving = True
            new_x, new_y, new_angle = moveBall(
                current_x = ball.x,
                current_y = ball.y,
                moveAngle = ball.angle
            )
            if(new_angle == -1):
                if(starting_ball_missing):
                    ball_starting_point_x = ball.x
                    starting_ball_missing = False
                new_x = ball_starting_point_x; new_y = 590; new_isMoving = False
                initialMovement = False

            areBallsMoving = True      
            ball.updateBall(
                new_x = new_x,
                new_y = new_y,
                new_angle = new_angle,
                new_isMoving = new_isMoving
            )


    for ball in balls:
        pygame.draw.circle(
            surface = screen,
            color = pygame.Color("#FDA172"),
            center = (ball.x, ball.y),
            radius = 5
        )
    

    if(initialMovement and cyclesPast % 5 == 0):
        cyclesPast = 0
        if(numBallsInPlay < score - 1):
            newBall = Ball(
                x = ball_starting_point_x,
                y = 590
            )
            newBall.startMoving(starting_angle)
            balls.append(newBall)
            numBallsInPlay += 1
    

    if(not areBallsMoving):
        numBallsInPlay = 1
        initialMovement = False; drawIndicatorFlag = True; detectMouseClickFlag = True
        balls.clear()
        balls = [Ball(x = ball_starting_point_x, y = 590)]


    if(drawIndicatorFlag):
        indicatorAngle = calculateAngle(
            start_x = ball_starting_point_x,
            start_y = 590,
            end_x = pygame.mouse.get_pos()[0],
            end_y = pygame.mouse.get_pos()[1]
        )
        
        pygame.draw.line(
            surface = screen,
            color = pygame.Color("#FFFFFF"),
            start_pos = (
                ball_starting_point_x + 7 * math.cos(indicatorAngle),
                590 - 7 * math.sin(indicatorAngle)
            ),
            end_pos = (
                ball_starting_point_x + (7 + INDICATOR_LENGTH) * math.cos(indicatorAngle),
                590 - (7 + INDICATOR_LENGTH) * math.sin(indicatorAngle)
            ),
            width = 2
        )


    if(areBallsMoving):
        displayScore = score - 1
    else:
        displayScore = score    
    scoreText = textFont.render(f"Score: {displayScore}", True, pygame.Color("#FFFFFF")) # text, antialias, color
    screen.blit(source = scoreText, dest = (10, 10))
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()