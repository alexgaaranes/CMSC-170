# Created by Marc Ian D.S. Aquino
# CMSC 170 EF-4L
# Exercise 1

# Responsible use: I used W3Schools to search on how to use file read on Python for the function input_file(f)
# The programmer did not use any AI when writing the code. The programmer used python.org documentations for searching the proper usage of functions such as classes.
# The programmer also used geeksforgeeks.org/python to search for the proper usage of operators such as self and __init__ method.
# The programmar used https://stackoverflow.com/questions/32238196/how-does-the-key-argument-in-pythons-sorted-function-work and https://www.programiz.com/python-programming/methods/built-in/enumerate as a references on how to use key function lambda and enumerate
# The programmer used the website https://www.programiz.com/dsa/graph-dfs and https://www.geeksforgeeks.org/python/convert-list-to-tuple-in-python/ to understand more about how dfs traversal and tuple conversion work
# The programmer did not use AI for completing the exercise, and is able to complete the task with the help of tutorial websites for Python programming.

# This program is an 8-bit sliding puzzle on a 3x3 grid.
# The goal of the program is to let the users 'move' the pieces, and solve the puzzle.
# This program is able to do BFS and DFS, and count the path cost and explored state
# If the puzzle is unsolvable, the program will print so.

# For the input file, the correct format is
# 1;2;3
# 4;5;6
# 7;8;0

# IMPORTANT: When the solution is being shown, please follow the movement of 0 as it is the base of how the code works. When it says Move 'w', it means that the 0 moved downwards, etc.

# Movements:
# 'a' = left, 'd' = right, 'w' = up, 'x' = down

def input_file(f):
    try:
        with open(f, 'r') as file: # Opens and read the files inside the input.txt
            lines = file.readlines()
            board = [] # Initialize the board array as empty
            for line in lines:
                row = [int(x) for x in line.strip().split(';')] # Read the file's content that are separated by a semicolon
                board.append(row)
            return board
    except FileNotFoundError: # Catch error for when the file cannot be found in the same directory.
        print(f"Error: The file is not on the same directory. ")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

class solvepuzzle:
    def __init__(self, initial):
        self.state = initial
        self.moves = 0
        self.goal_state = [[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 0]] # Placeholder for the correct orientation of the 8-puzzle
        self.empty_tile = self.find_empty_state()
    def find_empty_state(self): # find the empty tile for the movement
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j) # Returns the empty tile's location
        return None
    def solved(self): # Function for when the puzzle is solved already
        return self.state == self.goal_state

    def move(self, direction):
        i, j = self.empty_tile
        if direction == 'd':  # right movement
            if j > 0: # Checks if the column on the right is empty
                self.state[i][j], self.state[i][j-1] = self.state[i][j-1], self.state[i][j]
                self.empty_tile = (i, j-1)
                self.moves += 1 # Add movement count for each move
                return True
        elif direction == 'a':  # left movement
            if j < 2: # Checks if there is a missing tile on the left of a filled tile
                self.state[i][j], self.state[i][j+1] = self.state[i][j+1], self.state[i][j]
                self.empty_tile = (i, j+1)
                self.moves += 1 # Add movement count for each move
                return True
        elif direction == 'x':  # down movement
            if i > 0: # Checks if the row is not empty
                self.state[i][j], self.state[i-1][j] = self.state[i-1][j], self.state[i][j]
                self.empty_tile = (i-1, j)
                self.moves += 1 # Add movement count for each move
                return True
        elif direction == 'w':  # up movement
            if i < 2:
                self.state[i][j], self.state[i+1][j] = self.state[i+1][j], self.state[i][j]
                self.empty_tile = (i+1, j)
                self.moves += 1 # Add movement count for each move
                return True
        return False
   
    def display(self):
        print("\n8-Puzzle Board:")
        for i in range(3):
            for j in range(3): # Continuously print a horizontal and vertical line for the puzzle's board
                if self.state[i][j] == 0:
                    print("   ", end="")
                else:
                    print(f"  {self.state[i][j]} ", end="")
                if j < 2:
                    print("|", end="")
            print()
            if i < 2:
                print("------------")
        print(f"Move Count: {self.moves}\n")

def is_solvable(state): # Function for counting inversions to determine if the puzzle is solvable
    solvable = []
    for row in state:
        for tile in row:
                if tile != 0:
                    solvable.append(tile)
    inversions = 0
    n = len(solvable)
    for i in range(n):
        for j in range(i + 1, n):
            if solvable[i] > solvable[j]:
                inversions = inversions + 1
    return inversions % 2 == 0

def find_empty_state(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None
def copy_state(state):
    new_state = []
    for row in state:
        new_state.append([x for x in row])
    return new_state
def get_neighbor_state(state):
    valid_neighbors = []
    x, y = find_empty_state(state)
    directions = [[-1,0, 'w'], [1,0, 'x'], [0,-1, 'a'], [0,1, 'd']]  # directions for up, down, left, right with move labels
    for d in directions:
        emptyrow, emptycolumn = x + d[0], y + d[1]
        if 0 <= emptyrow < 3 and 0 <= emptycolumn < 3:
            new_state = copy_state(state)
            new_state[x][y], new_state[emptyrow][emptycolumn] = new_state[emptyrow][emptycolumn], new_state[x][y]
            valid_neighbors.append((new_state, d[2]))  # Include the move direction
    return valid_neighbors

def equalstate(s1, s2):
    for i in range(3):
        for j in range(3):
            if s1[i][j] != s2[i][j]:
                return False
    return True
def converttuples(state):
    return tuple(tuple(row) for row in state)
def printpath(path, explored_count):
    print("-------- Solution Path --------")
    for step in range(len(path)):
        state, move = path[step]
        print(f"Step {step}: Move '{move}'" if step > 0 else "Step 0: Initial state")
        for row in state:
            print("\t", row)
        print("-------------------")
    print(f"Path cost (number of moves): {len(path)-1}")
    print(f"Number of explored states: {explored_count}")
    print()

def solve_bfs(initial_state):
    final_goalstate = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]
    given_state = converttuples(initial_state)
    goal_state = converttuples(final_goalstate)
    frontier = [(given_state, [], 0)]  # (state, path, cost)
    explored = set() # 
    explored_count = 0
    while frontier:
        current_state, path, cost = frontier.pop(0)
        if current_state == goal_state: # Check if we are already at the goal state
            explored_count += 1 # Add that move to the number of moves
            solution_path = [] # Convert path to readable format
            solution_path.append((initial_state, 'start')) # Add initial state
            for movecount, move in path: # add all of the moves
                solution_path.append((list(list(row) for row in movecount), move))
            printpath(solution_path, explored_count)
            return
        if current_state in explored: # Skip the state if already explored
            continue
        
        explored.add(current_state) # The state is marked as explored
        explored_count += 1
        
        current_list = [list(row) for row in current_state] # Convert back the tuple to list for processing
        valid_neighbors = get_neighbor_state(current_list) # Get all the possible next states that might be a valid move
        for neighbor_state, move in valid_neighbors:
            neighbor_state = converttuples(neighbor_state)
            if neighbor_state not in explored: # checks if that state is not yet explored, and add it as a move cost
                new_path = path + [(neighbor_state, move)] # add the current path counted to the neighbors of the current tile adjacent to 0 plus the current move count
                path_cost = cost + 1
                frontier.append((neighbor_state, new_path, path_cost))
    print("No solution found with BFS.")
    print(f"Number of explored states: {explored_count}")

def solve_dfs(initial_state):
    final_goalstate = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]
    given_state = converttuples(initial_state) # Convert the initial state of the 8 puzzle as a tuple
    goal_state = converttuples(final_goalstate) # Convert the final state of the puzzle to be the goal state
    frontier = [(given_state, [], 0)]  # (state, path, cost)
    explored = set()
    explored_count = 0 # Track the number of explored states
    
    while frontier:
        current_state, path, cost = frontier.pop()
        if current_state == goal_state: # check if the current state is already in the goal state
            explored_count += 1 # Add count to the explored_count if not in goal state yet
            solution_path = []
            solution_path.append((initial_state, 'start')) # Add the initial state of the puzzle
            for movecount, move in path: # Add all the moevs
                solution_path.append((list(list(row) for row in movecount), move))
            printpath(solution_path, explored_count)
            return
        if current_state in explored:
            #explored_count += 1
            continue
        explored.add(current_state) # Mark the state as explored
        explored_count += 1
        current_list = [list(row) for row in current_state]
        valid_neighbors = get_neighbor_state(current_list) # Get all the posible next sattes
        for neighbor_state, move in valid_neighbors:
            neighbor_state = converttuples(neighbor_state)
            if neighbor_state not in explored:
                new_path = path + [(neighbor_state, move)]
                path_cost = cost + 1
                frontier.append((neighbor_state, new_path, path_cost))
    print("No solution found with DFS.")
    print(f"Number of explored states: {explored_count}")
def misplaced_tiles_heuristic(state): # Count the number of misplaced tiles (h1)
    goalstate = [[1, 2, 3], 
                 [4, 5, 6], 
                 [7, 8, 0]]
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goalstate[i][j]: #Compares if the state not in goal state yet
                count += 1 #add a count if not in goal state yet
    return count
def manhattan_distance_heuristic(state): # Calculate the Manhattan distance
    goalpos = { # Assumed correct positions for Manhattan distanec search strategy
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 0: (2, 2)
    }
    distance = 0 # Count the distance taken
    for i in range(3): # iterate for each of the rows and columns
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                goali, goalj = goalpos[tile] 
                distance += abs(i - goali) + abs(j - goalj) # Get the final distance with the given equation: |x1-x2| + |y1-y2|
    return distance
def solve_astar(initial_state, heuristic):
    final_goalstate = [[1, 2, 3], 
                       [4, 5, 6], 
                       [7, 8, 0]]
    given_state = converttuples(initial_state)
    goal_state = converttuples(final_goalstate)
    # Select the heuristic function based on user choice
    if heuristic == 1:
        heu_function = misplaced_tiles_heuristic
    elif heuristic == 2:
        heu_function = manhattan_distance_heuristic
    else:
        print("Invalid choice. Please select 1 or 2. ")
        return main()
    # Initialize the frontier with the initial state
    initial_h = heu_function(initial_state)
    frontier = [(initial_h, 0, given_state, [])]  # for (fn, gn, state, path)
    explored = set() # set as list to avoid duplication
    explored_count = 0 # Initialize the explored count as 0

    while frontier: #Get the state with the lowest fn value
        frontier.sort(key=lambda x: x[0])  # Sort by the fn value of each frontier
        fn, gn, cur_state, path = frontier.pop(0)
        if cur_state == goal_state:
            explored_count += 1
            solution_path = []

            solution_path.append((initial_state, 'start')) 
            for state_tuple, move in path: # print the solution path appended on the list
                stlist = [list(row) for row in state_tuple] # Create a list of row object
                solution_path.append((stlist, move)) 
            printpath(solution_path, explored_count)
            return
        
        if cur_state in explored:
            continue
        explored.add(cur_state) # Add the current state in explored 
        explored_count += 1 
        
        current_list = [list(row) for row in cur_state] # add as a current list of row 
        validneighbors = get_neighbor_state(current_list)
        for neighbor_state, move in validneighbors: # check the neighbor state for each move
            neighbor_tuple = converttuples(neighbor_state) # Convert the neighbor as a list
            if neighbor_tuple not in explored: # Check if that neighbor is not yet explored
                newgn = gn + 1
                newhn = heu_function(neighbor_state) #pass the neighbor state for manhattan or misplaced tiles search
                newfn = newgn + newhn
                newpath = path + [(cur_state, move)]
                found = False # Check if this state is already in the frontier with a higher cost
                for n, (fn_value, gn_value, state, path_val) in enumerate(frontier): # loop for each of the frontier
                    if state == neighbor_tuple and newgn < gn_value:
                        frontier[n] = (newfn, newgn, neighbor_tuple, newpath)
                        found = True
                        break
                if not found:
                    frontier.append((newfn, newgn, neighbor_tuple, newpath)) # append the values in the frontier 
    print("No solution found with A* search.")
    print(f"Number of explored states: {explored_count}")
def manual_solver(initial):
    puzzle = solvepuzzle(initial)
    while not puzzle.solved():
        puzzle.display()
        move = input("Please enter your next move: ").lower()
        if move == 'q':
            print("Goodbye! ")
            return
        if move in ['a', 'd', 'w', 'x']:
            if not puzzle.move(move):
                print("Invalid move! Try again.")
        else:
            print("Invalid input! Use 'a', 'd', 'w', or 'x'.") # Catch error if the user does not enter the given instructions
    puzzle.display()
    print("Congratulations! You solved the puzzle!")
    print(f"Total moves: {puzzle.moves}") # Shows the total moves taken by the user to solve the problem

def main():
    f = "input.txt" # input the text file as 'f'
    initial = input_file(f)
    if initial is None:
        return
    if not is_solvable(initial): # Passes through the is_solvable() function and checks if it can be solved or not
        print("This puzzle configuration is unsolvable!")
        return
    print("\n[1] Manually Solve the Puzzle")
    print("[2] Solve using BFS traversal")
    print("[3] Solve using DFS traversal")
    print("[4] Solve using A* search")
    print("[q] Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        manual_solver(initial)
    elif choice == '2':
        solve_bfs(initial)
    elif choice == '3':
        solve_dfs(initial)
    elif choice == '4':
        print("\n[1] Misplaced tiles heuristic")
        print("[2] Manhattan distance heuristic")
        heuristic = int(input("\nInput your choice: "))
        if heuristic in [1, 2]:
            solve_astar(initial, heuristic)
        else:
            print("\nInvalid choice. Please select 1 or 2 only. ")
            return main()
    elif choice == 'q':
        print("\nGoodbye! ")
        return
    else:
        print("Invalid choice!")
        return main()

if __name__ == "__main__":
    main()