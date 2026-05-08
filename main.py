import pygame
import sys
import random

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

# CELL
class Cell:
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.visited:
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls["top"]:
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)

# GRID
grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]

# DFS HELPERS
def get_neighbors(cell):
    neighbors = []
    r, c = cell.row, cell.col

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dr, dc in directions:
        nr, nc = r + dr, c + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if not grid[nr][nc].visited:
                neighbors.append(grid[nr][nc])

    return neighbors


def remove_walls(a, b):
    dx = a.col - b.col
    dy = a.row - b.row

    if dx == 1:
        a.walls["left"] = False
        b.walls["right"] = False
    elif dx == -1:
        a.walls["right"] = False
        b.walls["left"] = False

    if dy == 1:
        a.walls["top"] = False
        b.walls["bottom"] = False
    elif dy == -1:
        a.walls["bottom"] = False
        b.walls["top"] = False

# MAZE GEN STATE
stack = []
current = grid[0][0]
current.visited = True

maze_done = False

# MAIN LOOP
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

    # -------------------------
    # DFS MAZE GENERATION
    # -------------------------
    if not maze_done:

        neighbors = get_neighbors(current)

        if neighbors:
            nxt = random.choice(neighbors)
            stack.append(current)

            remove_walls(current, nxt)

            current = nxt
            current.visited = True

        elif stack:
            current = stack.pop()

        else:
            maze_done = True

    pygame.display.update()