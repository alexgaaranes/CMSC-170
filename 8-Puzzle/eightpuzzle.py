# Name:     Alexander Gabriel A. Aranes
# Section:  EF-4L

class EightPuzzle:
    grid: list = None
    zLoc: list = None
    isSolved: bool = False

    def __init__(self, grid_str: str):
        self.isSolved = False
        self.load_grid(grid_str)
        self.check_if_solvable()

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
    def check_if_solvable(self):
        flat_grid = sum(self.grid, [])
        inversions = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if flat_grid[i] != '0' and flat_grid[j] != '0' and int(flat_grid[i]) > int(flat_grid[j]):
                    inversions += 1
        if inversions % 2 != 0:
            print("Not solvable!")
            exit(1)
    
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
        for i in range(3):
            for j in range(3):
                val = (i * 3 + j + 1) % 9
                if int(self.grid[i][j]) != val:
                    return False
        self.isSolved = True
        return True


# Main Menu
def main():
    puzzle = EightPuzzle("input.txt")
    print("8-Puzzle")
    while not puzzle.isSolved:
        puzzle.show_grid()
        move = input("MOVE (waxd): ").strip().lower()

        if move == 'w':
            puzzle.up()
        elif move == 'a':
            puzzle.left()
        elif move == 'x':
            puzzle.down()
        elif move == 'd':
            puzzle.right()
        else:
            print("\nInvalid Input!\n")
            continue

# Run only if this file is ran directly
if __name__ == '__main__':
    main()

