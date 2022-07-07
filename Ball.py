import pygame
import math
import Constants

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

    def correctAngle(self):
        if(self.angle):
            while(self.angle > 2 * math.pi):
                self.angle -= 2 * math.pi
            
            while(self.angle < 0):
                self.angle += 2 * math.pi

    def determineSideOfEntry(self, block):
        if(
            (
                self.x >= block.x + Constants.MOVE_SPEED and
                self.x <= block.x + block.width - Constants.MOVE_SPEED and
                self.y >= block.y and
                self.y <= block.y + Constants.MOVE_SPEED
            ) or
            (
                self.y < self.x - block.x + block.y and
                self.x < block.x + Constants.MOVE_SPEED and
                self.y > block.y
            ) or
            (
                self.y < -self.x + block.x + block.y + block.width and
                self.x > block.x + block.width - Constants.MOVE_SPEED and
                self.y > block.y
            )
        ):
            return "Top"
        
        if(
            (
                self.x >= block.x and
                self.x <= block.x + Constants.MOVE_SPEED and
                self.y >= block.y + Constants.MOVE_SPEED and
                self.y <= block.y + block.height - Constants.MOVE_SPEED
            ) or
            (
                self.y > self.x - block.x + block.y and
                self.x > block.x and
                self.y < block.y + Constants.MOVE_SPEED
            ) or
            (
                self.y < -self.x + block.x + block.y + block.height and
                self.x > block.x and
                self.y > block.y + block.height - Constants.MOVE_SPEED
            )            
        ):
            return "Left"
        
        if(
            (
                self.x >= block.x + Constants.MOVE_SPEED and
                self.x <= block.x + block.width - Constants.MOVE_SPEED and
                self.y >= block.y + block.height - Constants.MOVE_SPEED and
                self.y <= block.y + block.height
            ) or
            (
                self.y > -self.x + block.x + block.y + block.height and
                self.x < block.x + Constants.MOVE_SPEED and
                self.y < block.y + block.height
            ) or
            (
                self.y > self.x - block.x + block.y - block.width + block.height and
                self.x > block.x + block.width - Constants.MOVE_SPEED and
                self.y < block.y + block.height
            )            
        ):
            return "Bottom"
        
        if(
            (
                self.x >= block.x + block.width - Constants.MOVE_SPEED and
                self.x <= block.x + block.width and
                self.y >= block.y + Constants.MOVE_SPEED and
                self.y <= block.y + block.height - Constants.MOVE_SPEED
            ) or 
            (
                self.y > -self.x + block.x + block.y + block.width and
                self.x < block.x + block.width and
                self.y < block.y + Constants.MOVE_SPEED
            ) or
            (
                self.y < self.x - block.x + block.y - block.width + block.height and
                self.x < block.x + block.width and
                self.y > block.y + block.height - Constants.MOVE_SPEED
            )             
        ):
            return "Right"

        return "Inside"

    def detectCollision(self, block):
        blockNearestPointToBall_x = self.x; blockNearestPointToBall_y = self.y
        collisionSide = "Inside"; x_collision = ""; y_collision = "" 
        
        if(self.x <= block.x):
            blockNearestPointToBall_x = block.x
            collisionSide = "Left"; x_collision = "Left"
        elif(self.x >= block.x + block.width):
            blockNearestPointToBall_x = block.x + block.width
            collisionSide = "Right"; x_collision = "Right"

        if(self.y <= block.y):
            blockNearestPointToBall_y = block.y
            collisionSide = "Top"; y_collision = "Top"
        elif(self.y >= block.y + block.height):
            blockNearestPointToBall_y = block.y + block.height
            collisionSide = "Bottom"; y_collision = "Bottom"

        if(math.sqrt( (blockNearestPointToBall_x - self.x) ** 2 + (blockNearestPointToBall_y - self.y) ** 2 ) > self.radius):
            return "NO_COLLISION"
        if(x_collision and y_collision):
            if(
                (
                    x_collision == "Left" and y_collision == "Top" and
                    self.angle >= 1.5 * math.pi and (self.angle < 2 * math.pi or self.angle == 0)
                ) or
                (
                    x_collision == "Left" and y_collision == "Bottom" and
                    self.angle >= 0 and self.angle <= 0.5 * math.pi                    
                ) or
                (
                    x_collision == "Right" and y_collision == "Top" and
                    self.angle >= math.pi and self.angle <= 1.5 * math.pi  
                ) or
                (
                    x_collision == "Right" and y_collision == "Bottom" and
                    self.angle >= 0.5 * math.pi and self.angle <= math.pi  
                )
            ):
                return "Corner"
        if(collisionSide == "Inside"):
            return self.determineSideOfEntry(block)
        return collisionSide

    def moveBall(self, isStartingBallMissing, ball_starting_point_x, blocks):
        normalMoving = True
        self.isMoving = True

        if((self.x >= Constants.SCREEN_WIDTH or self.x <= 0) and (self.y <= 0)):
            self.angle = math.pi + self.angle
        elif(self.x >= Constants.SCREEN_WIDTH or self.x <= 0):
            self.angle = math.pi - self.angle
        elif(self.y <= 0):
            self.angle = 2 * math.pi - self.angle
        elif(self.y >= Constants.SCREEN_HEIGHT):
            self.angle = None
        else:
            pass

        if(self.angle is None):
            if(isStartingBallMissing):
                self.y = 590; self.isMoving = False
                isStartingBallMissing = False
                return isStartingBallMissing, self.x
            
            self.x = ball_starting_point_x; self.y = 590; self.isMoving = False
            return isStartingBallMissing, None        

        self.correctAngle()

        for block in blocks:
            hadCollision = False
            while(True):
                collisionSide = self.detectCollision(block)
                if(collisionSide == "NO_COLLISION"):
                    break

                if(collisionSide == "Right" or collisionSide == "Left"):
                    self.angle = math.pi - self.angle
                elif(collisionSide == "Bottom" or collisionSide == "Top"):
                    self.angle = 2 * math.pi - self.angle
                else:
                    self.angle = math.pi + self.angle

                self.correctAngle()
                self.x += Constants.MOVE_SPEED * math.cos(self.angle); self.y -= Constants.MOVE_SPEED * math.sin(self.angle)
                hadCollision = True; normalMoving = False
            
            if(hadCollision):
                block.value -= 1
        
        if(normalMoving):
            self.x += Constants.MOVE_SPEED * math.cos(self.angle); self.y -= Constants.MOVE_SPEED * math.sin(self.angle)
        return isStartingBallMissing, None