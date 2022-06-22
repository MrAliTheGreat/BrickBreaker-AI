import math
import pygame
from random import randint


class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = -1
        self.isMoving = False
        self.radius = 5
        self.color = pygame.Color("#FDA172")

    def startMoving(self, new_angle):
        self.angle = new_angle 
        self.isMoving = True

    def drawBall(self, screen):
        pygame.draw.circle(
            surface = screen,
            color = self.color,
            center = (self.x, self.y),
            radius = self.radius
        )

    def detectCollision(self, block):
        blockNearestPointToBall_x = self.x; blockNearestPointToBall_y = self.y
        collisionSide = ""; x_collision = False; y_collision = False 
        
        if(self.x <= block.x):
            blockNearestPointToBall_x = block.x
            collisionSide = "Left"; x_collision = True
        elif(self.x >= block.x + block.width):
            blockNearestPointToBall_x = block.x + block.width
            collisionSide = "Right"; x_collision = True

        if(self.y <= block.y):
            blockNearestPointToBall_y = block.y
            collisionSide = "Top"; y_collision = True
        elif(self.y >= block.y + block.height):
            blockNearestPointToBall_y = block.y + block.height
            collisionSide = "Bottom"; y_collision = True

        if(math.sqrt( (blockNearestPointToBall_x - self.x) ** 2 + (blockNearestPointToBall_y - self.y) ** 2 ) > self.radius):
            return None
        if(x_collision and y_collision):
            return "Corner"
        return collisionSide

    def moveBall(self, isStartingBallMissing, ball_starting_point_x, blocks):
        self.isMoving = True

        if((self.x >= SCREEN_WIDTH or self.x <= 0) and (self.y <= 0)):
            self.angle = math.pi + self.angle
        elif(self.x >= SCREEN_WIDTH or self.x <= 0):
            self.angle = math.pi - self.angle
        elif(self.y <= 0):
            self.angle = 2 * math.pi - self.angle
        elif(self.y >= SCREEN_HEIGHT):
            self.angle = -1
        else:
            pass

        for block in blocks:
            collisionSide = self.detectCollision(block)
            if(collisionSide):
                if(collisionSide == "Right" or collisionSide == "Left"):
                    self.angle = math.pi - self.angle
                elif(collisionSide == "Bottom" or collisionSide == "Top"):
                    self.angle = 2 * math.pi - self.angle
                else:
                    self.angle = math.pi + self.angle
                
                block.value -= 1

        if(self.angle == -1):
            if(isStartingBallMissing):
                self.y = 590; self.isMoving = False
                isStartingBallMissing = False
                return isStartingBallMissing, self.x
            
            self.x = ball_starting_point_x; self.y = 590; self.isMoving = False
            return isStartingBallMissing, None

        self.x += MOVE_SPEED * math.cos(self.angle); self.y -= MOVE_SPEED * math.sin(self.angle)
        return isStartingBallMissing, None

class Block():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 30
        self.color = pygame.Color("#CAFEA7")
        self.value = value
        self.valueFont = pygame.font.SysFont("Comic Sans MS", 20)

    def drawBlock(self, screen):
        pygame.draw.rect(
            surface = screen,
            color = self.color,
            rect = (self.x, self.y, self.width, self.height)
        )
        valueText = self.valueFont.render(f"{self.value}", True, pygame.Color("#000000"))
        value_x = self.x + self.width // 2 - valueText.get_rect().width // 2
        value_y = self.y + self.height // 2 - valueText.get_rect().height // 2
        screen.blit(source = valueText, dest = (value_x, value_y))        

    def moveBlockDown(self):
        distanceToNextVerticalBlock = 33
        self.y += distanceToNextVerticalBlock





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

def generateNewRowOfBlocks(score):
    distanceToNextHorizontalBlock = 79    
    generatedBlocks = []
    numBlocks = randint(1, 10)
    for _ in range(numBlocks):
        generatedBlocks.append(
            Block(
                x = STARTING_BLOCK_X + randint(0, 9) * distanceToNextHorizontalBlock,
                y = STARTING_BLOCK_Y,
                value = score
            )
        )
    return generatedBlocks

def moveExistingBlocksDown(blocks):
    for block in blocks:
        block.moveBlockDown()


def drawBalls(screen, balls):
    for ball in balls:
        ball.drawBall(screen)

def drawBlocks(screen, blocks):
    for block in blocks:
        if(block.value <= 0):
            blocks.remove(block)
        else:
            block.drawBlock(screen)



pygame.init()
clock = pygame.time.Clock()

textFont = pygame.font.SysFont("Comic Sans MS", 20)

SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600
FPS = 30
MOVE_SPEED = 5
INDICATOR_LENGTH = 150
STARTING_BLOCK_X = 10; STARTING_BLOCK_Y = 50

screen = pygame.display.set_mode( [SCREEN_WIDTH, SCREEN_HEIGHT] )

running = True
drawIndicatorFlag = True; detectMouseClickFlag = True
generateNewRowOfBlocksFlag = True; generateNewRowOfBlocksHelperFlag = False
balls = [Ball(x = SCREEN_WIDTH // 2, y = 590)]; blocks = []
ball_starting_point_x = SCREEN_WIDTH // 2
cyclesPast = 0
score = 1; numBallsInPlay = 1

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN and detectMouseClickFlag):
            cyclesPast = 0
            isStartingBallMissing = True; drawIndicatorFlag = False; detectMouseClickFlag = False
            starting_angle = calculateAngle(
                start_x = ball_starting_point_x,
                start_y = 590,
                end_x = pygame.mouse.get_pos()[0],
                end_y = pygame.mouse.get_pos()[1]
            )            
            balls[0].startMoving(starting_angle)
            generateNewRowOfBlocksHelperFlag = True
            score += 1


    screen.fill( (0, 0, 0) )

    areBallsMoving = False; cyclesPast += 1
    for ball in balls:
        if(ball.isMoving):
            areBallsMoving = True
            isStartingBallMissing, returned_x = ball.moveBall(isStartingBallMissing, ball_starting_point_x, blocks)
            if(returned_x):
                ball_starting_point_x = returned_x

    if(generateNewRowOfBlocksFlag):
        moveExistingBlocksDown(blocks)
        blocks.extend(generateNewRowOfBlocks(score))
        generateNewRowOfBlocksFlag = False
    
    drawBalls(screen, balls)
    drawBlocks(screen, blocks)

    if(cyclesPast % 5 == 0):
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
        if(generateNewRowOfBlocksHelperFlag):
            generateNewRowOfBlocksFlag = True; generateNewRowOfBlocksHelperFlag = False
        
        numBallsInPlay = 1
        drawIndicatorFlag = True; detectMouseClickFlag = True
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