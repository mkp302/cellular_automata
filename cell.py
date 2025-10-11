from enum import Enum


class burning_state(Enum):
    NONFLAMMABLE = 0
    NOTBURNING = 1
    BURNING = 2
    BURNEDOUT = 3


class cell:
    tree_density = 0.0
    burning = burning_state.NONFLAMMABLE
