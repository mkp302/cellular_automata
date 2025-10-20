from models.cell import Cell
import random


class Grid:
    def __init__(self, N, max_N, min_N):
        self.N = N
        self.max_N = max_N
        self.min_N = min_N
        self.cells = []
        for _ in range(0, N + 2):
            row = []
            for _ in range(0, N + 2):
                cell = Cell.generate_cell()
                row.append(cell)
            self.cells.append(row)

    def set_N(self, new_N):
        if new_N > self.max_N:
            new_N = self.max_N
        if new_N < self.min_N:
            new_N = self.min_N

        if new_N > self.N:
            for row in self.cells:
                for _ in range(0, new_N - self.N):
                    cell = Cell.generate_cell()
                    row.append(cell)
        elif self.N < new_N:
            for row in self.cells:
                row = row[: new_N + 2]
        self.N = new_N
        return new_N

    def update_cells(self, wind=(0, 0)):
        # Skip edges for now
        # TODO figure out boundary conditions
        print("OG Grid")
        self.print_cells()
        new_grid = [[Cell() for _ in range(self.N + 2)] for _ in range(self.N + 2)]
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                new_grid[i][j].tree_density = cell.tree_density
                new_grid[i][j].burning = cell.burning
                new_grid[i][j].burn_count = cell.burn_count
                print("looking at", i, j)
                if i == 0 or j == 0 or i == self.N + 1 or j == self.N + 1:
                    continue
                if cell.burning == 3:
                    continue

                if cell.burning == 2:
                    "cell is burning"
                    new_grid[i][j].burn_count += 1
                    if new_grid[i][j].burn_count > 15:
                        new_grid[i][j].burning = 3
                    continue
                # rightmost
                if self.cells[i + 1][j].burning == 2:
                    print("i+1")
                    new_grid[i][j].burning = 2
                    continue
                # top
                if self.cells[i][j + 1].burning == 2:
                    print("j+1")
                    new_grid[i][j].burning = 2
                    continue
                # left
                if self.cells[i - 1][j].burning == 2:
                    print("i-1")
                    new_grid[i][j].burning = 2
                    continue
                # bottom
                if self.cells[i][j - 1].burning == 2:
                    print("j-1")
                    new_grid[i][j].burning = 2
                    continue

        self.cells = new_grid
        print("New Grid")
        self.print_cells()

    def randomize(self):
        for i, row in enumerate(self.cells[1 : self.N + 1]):
            for j, cell in enumerate(row[1 : self.N + 1]):
                cell.tree_density = random.random()
                cell.burning = 0
                cell.burn_count = 0
        i = random.randint(1, self.N)
        j = random.randint(1, self.N)
        self.cells[i][j].burning = 2
    def randomize_topology(self):

    def print_cells(self):
        for i, row in enumerate(self.cells[1 : self.N + 1]):
            for j, cell in enumerate(row[1 : self.N + 1]):
                print(cell.burning, sep=" ", end=" ")
            print("\n")
