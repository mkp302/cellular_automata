from models.cell import Cell


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

    def update_cells(self):
        # Skip edges for now
        # TODO figure out boundary conditions
        for i, row in enumerate(self.cells[1 : N + 1]):
            for j, col in enumerate(row[1 : N + 1]):
                ...
