
import pygame
import sys

WIDTH = 900
HEIGHT = 900
ROWS = 20
COLS = 20
CELL_SIZE = WIDTH // COLS

BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Cell:
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls["top"]:
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)


grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    for row in grid:
        for cell in row:
            cell.draw()

    pygame.display.update()