# Responsible use of AI
# Extent and Purpose of AI Use:
#   Used for reviewing python syntax especially on OOP
# Responsible Use Justification:
#   The code below are typewritten manually without any AI generation. The user only used the AI overview in Google
#   for faster searching.

# Name:     Alexander Gabriel A. Aranes
# Section:  EF-4L

# Class for EightPuzzle
class EightPuzzle:
    grid: list = None
    zLoc: list = None
    isSolved: bool = False

    def __init__(self, grid_str: str):
        self.isSolved = False
        self.load_grid(grid_str)

    def __repr__(self):
        return f"EightPuzzle(grid={self.grid}, zLoc={self.zLoc}, isSolved={self.isSolved})"
         
    # Load grid from file
    # format x=0-8:
    """
    x;x;x
    x;x;x
    x;x;x 
    """
    def load_grid(self, grid_str: str):
        with open(grid_str) as f:
            content = f.read().strip().split("\n")
            self.grid = [row.split(";") for row in content]

            # Get zLoc
            # I used assert becaue try catch is ahh
            assert len(self.grid) == 3 and all(len(row) == 3 for row in self.grid), "Grid should be 3x3"
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j] == '0':
                        self.zLoc = [i, j] # (row, col)
                        return
        # test if the grid is solvable
        if not self.check_solved():
            flat_grid = sum(self.grid, [])
            inversions = 0
            for i in range(9):
                for j in range(i + 1, 9):
                    if flat_grid[i] != '0' and flat_grid[j] != '0' and int(flat_grid[i]) > int(flat_grid[j]):
                        inversions += 1
            if inversions % 2 != 0:
                raise ValueError("Impossible Puzzle")
    
    # Display grid
    def show_grid(self):
        print("_____________")
        for row in self.grid:
            print("| " + " | ".join(row) + " |")
            print("_____________")
    
    # Swap position of two grid items
    def swap(self, pos1: list, pos2: list):
        self.grid[pos1[0]][pos1[1]], self.grid[pos2[0]][pos2[1]] = self.grid[pos2[0]][pos2[1]], self.grid[pos1[0]][pos1[1]]
        self.zLoc = pos2
    
    # The ff methods are for movement (I seperated so that it can be used in other ways)
    # The movement pertains to the tile possible to swap with 0 and not the movement of 0 otself
    def right(self):
        if self.zLoc[1] > 0:
            self.swap(self.zLoc, [self.zLoc[0], self.zLoc[1] - 1])
        else:
            print("\nInvalid Move!\n")

    def left(self):
        if self.zLoc[1] < 2:
            self.swap(self.zLoc, [self.zLoc[0], self.zLoc[1] + 1])
        else:
            print("\nInvalid Move!\n")

    def up(self):
        if self.zLoc[0] < 2:
            self.swap(self.zLoc, [self.zLoc[0] + 1, self.zLoc[1]])
        else:
            print("\nInvalid Move!\n")
    
    def down(self):
        if self.zLoc[0] > 0:
            self.swap(self.zLoc, [self.zLoc[0] - 1, self.zLoc[1]])
        else:
            print("\nInvalid Move!\n")

    # Check if the Puzzle is solved
    # Solved state:
    """
    1;2;3
    4;5;6
    7;8;0
    """
    def check_solved(self):
        self.isSolved = self.grid = [['1','2','3'],['4','5','6'],['7','8','0']]
        return self.isSolved


# State class for BFS and DFS
class State:
    grid: tuple = None
    z_loc: list = None
    path: str = None

    def __init__(self, grid: tuple):
        self.grid = tuple(grid)
        self.z_loc = self.get_z()
        self.path = ''

    def __repr__(self) -> str:
        return f"State(grid={self.grid}, zLoc={self.z_loc}, path={self.path})"

    def get_actions(self) -> list:
        z: list = self.z_loc
        actions: list = []
        #               UP              DOWN                RIGHT       LEFT 
        for [i,j] in [[z[0]-1, z[1]], [z[0]+1, z[1]], [z[0], z[1]+1], [z[0], z[1]-1]]:
            movement = ''
            if i >= 0 and i < 3 and j >= 0 and j < 3: # Allow action in bounds only
                # Copy grid of curr state
                grid_copy: list = [row[:] for row in self.grid]   # Copy the grid
                grid_copy[z[0]][z[1]], grid_copy[i][j] = grid_copy[i][j], grid_copy[z[0]][z[1]]

                # Instantiate a new state
                new_action: State = State(grid_copy) 
                new_action.path = self.path
                if i < z[0] and j == z[1]:  # UP
                    new_action.path += 'U'
                elif i > z[0] and j == z[1]:
                    new_action.path += 'D'
                elif i == z[0] and j > z[1]:
                    new_action.path += 'R'
                elif i == z[0] and j < z[1]:
                    new_action.path += 'L'
                else:   # IDK WHAT TODO BASTA BAWAL
                    exit(1)

                actions.append(new_action)
        return actions

    def get_z(self) -> list:
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == '0':
                    self.z_loc = [i,j]
                    return self.z_loc
    
# Search class for searching
class Search:
    goal: tuple = (['1','2','3'],['4','5','6'],['7','8','0'])

    def solve_bfs(puzzle: EightPuzzle):
        # Instantiate initial State object
        init_state = State(tuple(puzzle.grid))

        frontier: list = [init_state] 
        explored: list = []
        while len(frontier) > 0:
            current_state = frontier.pop(0)
            explored.append(current_state.grid)
            if current_state.grid == Search.goal:
                print("Path:", current_state.path)
                print("Cost:", len(current_state.path))
                print("No. of Explored:", len(explored))
                return current_state
            else:
                actions: State = current_state.get_actions()
                frontier_tuples: list = [tuple(state.grid) for state in frontier]
                for a in actions:
                    if a.grid not in explored and a.grid not in frontier_tuples:
                        frontier.append(a)



    def solve_dfs(puzzle: EightPuzzle):
        # Instantiate initial State object
        init_state = State(tuple(puzzle.grid))

        frontier: list = [init_state] 
        explored: list = []
        while len(frontier) > 0:
            current_state = frontier.pop(-1)
            explored.append(current_state.grid)
            if current_state.grid == Search.goal:
                print("Path:", current_state.path)
                print("Cost:", len(current_state.path))
                print("No. of Explored:", len(explored))
                return current_state
            else:
                actions: State = current_state.get_actions()
                frontier_tuples: list = [tuple(state.grid) for state in frontier]
                for a in actions:
                    if a.grid not in explored and a.grid not in frontier_tuples:
                        frontier.append(a)


# Main Menu
def main():
    choice: int = None

    # initialize the puzzle
    puzzle = EightPuzzle("input.txt")
    while True:
        print("Initial Puzzle")
        puzzle.show_grid()
        print("[1] BFS")
        print("[2] DFS")
        print("[3] Exit")
        choice = int(input("Choose Strategy: "))

        if choice == 1:
            # BFS
            Search.solve_bfs(puzzle)

        elif choice == 2:
            # DFS
            Search.solve_dfs(puzzle)

        elif choice == 3:
            print("\nExit\n")
            break
        else:
            print("\nInvalid Input\n")


# Run only if this file is ran directly
if __name__ == '__main__':
    main()

