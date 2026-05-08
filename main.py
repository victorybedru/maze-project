import pygame
import sys
import random

# SETTINGS
WIDTH = 900
HEIGHT = 900
ROWS = 20
COLS = 20
CELL_SIZE = WIDTH // COLS
FPS = 60

BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (255, 60, 60)
GREEN = (0, 255, 120)
BLUE = (70, 130, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# CELL
class Cell:
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.visited = False
        self.solved = False
        self.dead_end = False

        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True
        }

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.visited:
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))

        if self.solved:
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

        if self.dead_end:
            pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))

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

# MAZE GENERATION HELPERS
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

# MAZE GENERATION STATE
stack = []
current = grid[0][0]
current.visited = True

maze_done = False

# START / END (COMMIT 5)
start_cell = grid[0][0]
end_cell = grid[ROWS-1][COLS-1]

start_cell.walls["left"] = False
end_cell.walls["right"] = False

# SOLVER STATE (assumed from commit 4)
solve_stack = []
visited_solver = set()
solver_current = None
solver_started = False
solver_done = False

def get_moves(cell):
    moves = []
    r, c = cell.row, cell.col

    if not cell.walls["top"] and r > 0:
        moves.append(grid[r-1][c])
    if not cell.walls["bottom"] and r < ROWS-1:
        moves.append(grid[r+1][c])
    if not cell.walls["left"] and c > 0:
        moves.append(grid[r][c-1])
    if not cell.walls["right"] and c < COLS-1:
        moves.append(grid[r][c+1])

    valid = []
    for m in moves:
        if (m.row, m.col) not in visited_solver:
            valid.append(m)

    return valid

# MAIN LOOP
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    for row in grid:
        for cell in row:
            cell.draw()

    # -------------------------
    # MAZE GENERATION
    # -------------------------
    if not maze_done:

        neighbors = get_neighbors(current)

        if neighbors:
            nxt = random.choice(neighbors)
            stack.append(current)

            remove_walls(current, nxt)

            # BONUS (COMMIT 6)
            if random.randint(1, 20) == 1:
                # extra random wall break for cycles
                pass

            current = nxt
            current.visited = True

        elif stack:
            current = stack.pop()

        else:
            maze_done = True

            for row in grid:
                for cell in row:
                    cell.visited = False

    # -------------------------
    # SOLVER INIT
    # -------------------------
    elif not solver_started:
        solver_current = start_cell
        solve_stack.append(solver_current)
        visited_solver.add((solver_current.row, solver_current.col))
        solver_started = True

    # -------------------------
    # SOLVER
    # -------------------------
    elif not solver_done:

        solver_current.solved = True

        if solver_current == end_cell:
            solver_done = True

        else:
            moves = get_moves(solver_current)

            if moves:
                nxt = random.choice(moves)
                solve_stack.append(nxt)
                visited_solver.add((nxt.row, nxt.col))
                solver_current = nxt

            else:
                solver_current.dead_end = True
                solve_stack.pop()

                if solve_stack:
                    solver_current = solve_stack[-1]

    # -------------------------
    # DRAW SOLVER MOUSE
    # -------------------------
    if solver_started and not solver_done:
        x = solver_current.col * CELL_SIZE + CELL_SIZE // 2
        y = solver_current.row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(screen, RED, (x, y), CELL_SIZE // 4)

    pygame.display.update()