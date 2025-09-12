# Responsible Use of AI:
# Extent and Purpose of AI Use:
#
# Responsible Use Justification:
#

# Name:     Alexander Gabriel A. Aranes
# Section:  EF-4L

# Tic-Tac-Toe

# separate class for the board of the game
class Board:
    grid: list = None

    def __init__(self, grid: list):
        self.grid = grid
    
    def show(self):
        for row in self.grid:
            for cell in row:
                print(f"| {' ' if cell == '' else cell} ", end='')
            print('|')
    
    def put(self, turn: str, pos: tuple) -> None:
        if pos[0] > 2 or pos[0] < 0 or pos[1] > 2 or pos[1] < 0:
            print("Invalid Position")
        else:
            if self.grid[pos[0]][pos[1]] != '': print("Occupied")
            else: self.grid[pos[0]][pos[1]] = turn
    
    def winner(self) -> str:
        for i in range(3):
            # Horizontal
            if (self.grid[i][0] == self.grid[i][1] == self.grid[i][2]) and self.grid[i][0] != '':
                return self.grid[i][0]
            # Vertical
            if (self.grid[0][i] == self.grid[1][i] == self.grid[2][i]) and self.grid[0][i] != '':
                return self.grid[0][i]
        # Diagonal
        if ((self.grid[0][0] == self.grid[1][1] == self.grid[2][2]) or (self.grid[0][2] == self.grid[1][1] == self.grid[2][0])) and self.grid[1][1] != '':
            return self.grid[1][1]
        
        return None

# static class that handles player turn
class Player:
    def get_turn(board: list) -> str:
        num_x: int = 0    
        num_o: int = 0
        for row in board:
            for val in row:
                if val == 'X':
                    num_x += 1
                elif val == 'O':
                    num_o += 1
        if num_o >= num_x:
            return 'X'
        else:
            return 'O'


# Execute when file is ran
if __name__ == '__main__':

    my_grid = [
        ['','',''],
        ['','',''],
        ['','','']
    ]
    # game logic
    my_board: Board = Board(my_grid)

    while(my_board.winner() == None):
        my_board.show()
        row: int = int(input('Row: '))
        col: int = int(input('Col: '))
        my_board.put(Player.get_turn(my_board.grid), (row-1, col-1))
    
    my_board.show()
    print(f'{my_board.winner()} wins!')