import math
from time import sleep
import pygame
from random import randint

import utils
import Constants
from Ball import Ball
from Block import Block


def generateNewRowOfBlocks(score):
    distanceToNextHorizontalBlock = 79    
    generatedBlocks = []; idxs = set()
    numBlocks = randint(1, 10)
    for _ in range(numBlocks):
        blockIdx = randint(0, 9)
        while(blockIdx in idxs):
            blockIdx = randint(0, 9)
        idxs.add(blockIdx)
        
        generatedBlocks.append(
            Block(
                x = Constants.STARTING_BLOCK_X + blockIdx * distanceToNextHorizontalBlock,
                y = Constants.STARTING_BLOCK_Y,
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

def checkGameStatus(blocks):
    for block in blocks:
        if(block.y + block.height >= Constants.STARTING_BLOCK_Y + Constants.NUM_LEVELS * 33 - 10):
            return False
    return True

pygame.init()
clock = pygame.time.Clock()

textFont = pygame.font.SysFont("Comic Sans MS", 20)

screen = pygame.display.set_mode( [Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT] )

running = True; lost = True
drawIndicatorFlag = True; detectMouseClickFlag = True
generateNewRowOfBlocksFlag = True; generateNewRowOfBlocksHelperFlag = False; areBallsMoving = False
balls = [Ball(x = Constants.SCREEN_WIDTH // 2, y = 590)]; blocks = []
ball_starting_point_x = Constants.SCREEN_WIDTH // 2
cyclesPast = 0
score = 1; numBallsInPlay = 1

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False; lost = False
        elif(event.type == pygame.MOUSEBUTTONDOWN and detectMouseClickFlag and not Constants.AI):
            cyclesPast = 0
            isStartingBallMissing = True; drawIndicatorFlag = False; detectMouseClickFlag = False
            starting_angle = utils.calculateAngle(
                start_x = ball_starting_point_x,
                start_y = 590,
                end_x = pygame.mouse.get_pos()[0],
                end_y = pygame.mouse.get_pos()[1]
            )            
            balls[0].startMoving(starting_angle)
            generateNewRowOfBlocksHelperFlag = True
            score += 1

    if(Constants.AI and not areBallsMoving):
        cyclesPast = 0
        starting_angle = utils.degree2radian(50)          
        balls[0].startMoving(starting_angle)
        isStartingBallMissing = True; generateNewRowOfBlocksHelperFlag = True
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
        running = checkGameStatus(blocks)
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


    if(drawIndicatorFlag and not Constants.AI):
        indicatorAngle = utils.calculateAngle(
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
                ball_starting_point_x + (7 + Constants.INDICATOR_LENGTH) * math.cos(indicatorAngle),
                590 - (7 + Constants.INDICATOR_LENGTH) * math.sin(indicatorAngle)
            ),
            width = 2
        )


    if(areBallsMoving):
        displayScore = score - 1
    else:
        displayScore = score    
    
    scoreText = textFont.render(f"Score: {displayScore}", True, pygame.Color("#FFFFFF")) # text, antialias, color
    screen.blit(source = scoreText, dest = (10, 10))
    pygame.draw.line(
        surface = screen,
        color = pygame.Color("#FFFFFF"),
        start_pos = (
            0,
            Constants.STARTING_BLOCK_Y + Constants.NUM_LEVELS * 33
        ),
        end_pos = (
            Constants.SCREEN_WIDTH,
            Constants.STARTING_BLOCK_Y + Constants.NUM_LEVELS * 33
        ),
        width = 5
    )    
    pygame.display.flip()
    
    clock.tick(Constants.FPS)


if(lost):
    endFont = pygame.font.SysFont("Comic Sans MS", 175)
    endText = endFont.render(f"You Lost!", True, pygame.Color("#FFFFFF"))
    messageWidth, messageHeight = endText.get_size()
    pygame.draw.rect(
        surface = screen,
        color = pygame.Color("#DE0A26"),
        rect = (
            Constants.SCREEN_WIDTH // 2 - messageWidth // 2,
            Constants.SCREEN_HEIGHT // 2 - messageHeight // 2,
            messageWidth,
            messageHeight
        )
    )
    screen.blit(source = endText, dest = (Constants.SCREEN_WIDTH // 2 - messageWidth // 2, Constants.SCREEN_HEIGHT // 2 - messageHeight // 2))
    pygame.display.flip()
    sleep(2)
pygame.quit()