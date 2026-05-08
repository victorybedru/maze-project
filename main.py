import pygame
import sys
import random

# -------------------
# SETTINGS
# -------------------
WIDTH, HEIGHT = 900, 900
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
FPS = 60

# COLORS
BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
GREEN = (0, 255, 120)
RED = (255, 60, 60)
BLUE = (70, 130, 255)
GRAY = (40, 40, 40)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator + Solver")
clock = pygame.time.Clock()

# -------------------
# CELL CLASS
# -------------------
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
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

# -------------------
# GRID
# -------------------
grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]

# -------------------
# HELPERS (MAZE GEN)
# -------------------
def get_neighbors(cell):
    r, c = cell.row, cell.col
    neighbors = []

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
    elif dy == 1:
        a.walls["top"] = False
        b.walls["bottom"] = False
    elif dy == -1:
        a.walls["bottom"] = False
        b.walls["top"] = False

    # ---------------- BONUS: random cycle creation ----------------
    if random.randint(1, 20) == 1:
        # randomly break a wall anyway (creates loops)
        a.walls["top"] = a.walls["top"] and False or False

# -------------------
# MAZE GENERATION
# -------------------
stack = []
current = grid[0][0]
current.visited = True

maze_done = False

# -------------------
# SOLVER
# -------------------
solve_stack = []
visited_solver = set()

solver_current = None
solver_started = False
solver_done = False

start_cell = grid[0][0]
end_cell = grid[ROWS - 1][COLS - 1]

start_cell.walls["left"] = False
end_cell.walls["right"] = False


def get_moves(cell):
    r, c = cell.row, cell.col
    moves = []

    if not cell.walls["top"] and r > 0:
        moves.append(grid[r-1][c])
    if not cell.walls["bottom"] and r < ROWS-1:
        moves.append(grid[r+1][c])
    if not cell.walls["left"] and c > 0:
        moves.append(grid[r][c-1])
    if not cell.walls["right"] and c < COLS-1:
        moves.append(grid[r][c+1])

    return [m for m in moves if (m.row, m.col) not in visited_solver]


# -------------------
# MAIN LOOP
# -------------------
while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw grid
    for row in grid:
        for cell in row:
            cell.draw()

    # MAZE GENERATION
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

            for row in grid:
                for cell in row:
                    cell.visited = False

    # SOLVER INIT
    elif not solver_started:
        solver_current = start_cell
        solve_stack.append(solver_current)
        visited_solver.add((solver_current.row, solver_current.col))
        solver_started = True

    # SOLVING
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

    # DRAW MOUSE
    if solver_started and not solver_done:
        x = solver_current.col * CELL_SIZE + CELL_SIZE // 2
        y = solver_current.row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(screen, RED, (x, y), CELL_SIZE // 4)

    pygame.display.update()