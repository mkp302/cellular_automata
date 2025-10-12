from enum import Enum


class burning_state(Enum):
    NONFLAMMABLE = 0
    NOTBURNING = 1
    BURNING = 2
    BURNEDOUT = 3


class Cell:
    def __init__(self):
        self.tree_density = 0.0
        self.burning = burning_state.NONFLAMMABLE

    @staticmethod
    def generate_cell():
        return Cell()
