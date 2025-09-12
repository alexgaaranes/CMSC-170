
# Class for the state of the game
class Board:
    # attributes
    grid: list = None

    # Constructor
    def __init__(self, grid: list):
        self.grid = grid 

    # show the board grid content
    def show(self):
        for row in self.grid:
            for val in row:
                print(f"| {val if val != '' else ' '} ", end='')
            print("|")

    # method that updates the board itself 
    def put(self, turn: str, pos: tuple):
        if pos[0] < 0 or pos[0] > 2 or pos[1] < 0 or pos[1] > 2:
            print("Invalid Position")
            raise Exception("invalid-pos")
        if self.grid[pos[0]][pos[1]] != '':
            print("Cell occupied!")
            raise Exception("occupied")
        self.grid[pos[0]][pos[1]] = turn 
    
    # TODO: 
    def get_winner(self):
        for i in range(3):
            sgrid = self.grid
            # horizontal
            if 

            # vertical

class Search:
    pass


# Static class
class Game:
    # get whose turn it is
    def get_turn(board: Board) -> str:
        xs = 0
        os = 0
        for row in board.grid:
            for val in row:
                if val == 'X':
                    xs += 1
                elif val == 'O':
                    os += 1
        if xs <= os:
            return 'X'
        else:
            return 'O'

# Do whatever inside this block if this file is ran directly
# Basically this is main ig?
if __name__ == '__main__':
    my_grid: list = [
       ['','',''],
       ['','',''],
       ['','','']
    ] 

    my_board = Board(my_grid)

    while True:
        my_board.show()
        turn: str = Game.get_turn(my_board)
        print(f"{turn}'s turn")
        row: int = int(input("row: "))
        col: int = int(input("col: "))
        try:
            my_board.put(turn, (row-1, col-1))
        except:
            continue

        # AI turn
    
