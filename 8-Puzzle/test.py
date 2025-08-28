from eightpuzzle import EightPuzzle
from state import State

puzzle = EightPuzzle("input.txt")
state01 = State(puzzle.grid)
print(state01)

state01.get_neighbors(puzzle.zLoc)
print(state01)
state01.show_neighbors()