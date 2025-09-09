# Responsible use of AI
# Extent and Purpose of AI Use:
#   Used for reviewing python syntax and methods for lists
# Responsible Use Justification:
#   The code below are manually typed without any AI agent help for code generation.
#   AI was only used to to summarize review of syntax in the web.

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
        self.isSolved = self.grid == [['1','2','3'],['4','5','6'],['7','8','0']]
        if not self.isSolved:
            flat_grid = sum(self.grid, [])
            inversions = 0
            for i in range(9):
                for j in range(i + 1, 9):
                    if flat_grid[i] != '0' and flat_grid[j] != '0' and int(flat_grid[i]) > int(flat_grid[j]):
                        inversions += 1
            if inversions % 2 != 0:
                print("Cannot be solved")
                exit(1)

        return self.isSolved


# State class for BFS and DFS
class State:
    grid: tuple = None
    z_loc: list = None
    path: str = None
    cost: int = 0
    est_cost: int = 0
    f_cost: int = 0

    def __init__(self, grid: tuple):
        self.grid = tuple(grid)
        self.z_loc = self.get_z()
        self.path = ''

    def __repr__(self) -> str:
        return f"State(grid={self.grid}, zLoc={self.z_loc}, path={self.path}, f_cost={self.f_cost})"

    def get_actions(self, heuristic=None) -> list:
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
                if heuristic != None:
                	heuristic(new_action)
                
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

    def set_costs(self, est_cost: int):
        self.cost = len(self.path)
        self.est_cost = est_cost
        self.f_cost = self.cost + self.est_cost

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
                for a in actions:
                    if a.grid not in explored:
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
                for a in actions:
                    if a.grid not in explored:
                        frontier.append(a)
                        
    def explore_min_f_cost(frontier: list):
        min_state: State = frontier[0]

        for i in range(1, len(frontier)):
        	if frontier[i].f_cost < min_state.f_cost:
        		min_state = frontier[i]
        return frontier.pop(frontier.index(min_state))
                        
    def solve_astar(puzzle: EightPuzzle, heuristic):	# Heuristic is a callback
    	# Instantiate initial State object
        init_state = State(tuple(puzzle.grid))
        heuristic(init_state)	# Use heuristic

        frontier: list = [init_state]	# open_list
        explored: list = []				# closed_list	
        while len(frontier) > 0:
            current_state = Search.explore_min_f_cost(frontier)	# Remove min f_cost
            explored.append(current_state.grid)
            if current_state.grid == Search.goal:
                print("Path:", current_state.path)
                print("Cost:", len(current_state.path))
                print("No. of Explored:", len(explored))
                return current_state
            else:
                actions: State = current_state.get_actions(heuristic)
                frontier_grids = [state.grid for state in frontier]
                for a in actions:
                    if (a.grid not in explored and a.grid not in frontier_grids):
                        frontier.append(a)
                    if (a.grid in frontier_grids):
                    	# Check for dupes
                    	for state in frontier:
                    		if a.f_cost < state.f_cost:
                    			frontier.pop(frontier.index(state))
                    			frontier.append(a)
	
    def manhattan_h(state: State):
    	cumulative_cost = 0
    	for i in range(3):
    		for j in range(3):
    			expected_val = (i * 3 + j + 1)
    			curr_val = int(state.grid[i][j])
    			if curr_val != expected_val % 9:
    				# Get the correct position
    				correct_pos = [(curr_val - 1) // 3, (curr_val - 1) % 3]
    				cumulative_cost += abs(correct_pos[0] - i) + abs(correct_pos[1] + j)
    				
    	state.set_costs(cumulative_cost) # Update f_cost
    				
		
# Main Menu
def main():
    choice: int = None

    # initialize the puzzle
    puzzle = EightPuzzle("input.txt")
    puzzle.check_solved()
    while True:
        print("Initial Puzzle")
        puzzle.show_grid()
        print("[1] BFS")
        print("[2] DFS")
        print("[3] A*")
        print("[4] Exit")
        choice = int(input("Choose Strategy: "))

        if choice == 1:
            # BFS
            Search.solve_bfs(puzzle)

        elif choice == 2:
            # DFS
            Search.solve_dfs(puzzle)

        elif choice == 3:
        	# A*
        	Search.solve_astar(puzzle, Search.manhattan_h)
    		
        elif choice == 4:
            print("\nExit\n")
            break
        else:
            print("\nInvalid Input\n")


# Run only if this file is ran directly
if __name__ == '__main__':
    main()

