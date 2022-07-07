import pygame

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