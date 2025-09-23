# Responsible Use of AI:
# Extent and Purpose of AI Use:
#   Used AI how to use randomization and raise errors in python to make the program
#   run smooth. Also used for reviewing some syntax.
# Responsible Use Justification:
#   No code written are generated from an AI agent. Everything is typewritten by me

# Name:     Alexander Gabriel A. Aranes
# Section:  EF-4L


# Tic-Tac-Toe

import copy, random

# Look up for utility
utility: dict = {
    'X': -1,
    'O': 1,
    '': 0
}

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
            raise Exception("Invalid Cell")
        else:
            if self.grid[pos[0]][pos[1]] != '': raise Exception("Invalid Cell")
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

        # Check for draw
        for row in self.grid:
            for val in row:
                if val == '':
                    return None
        
        # Draw
        return ''


# Static class with methods to search
class Search:
    def alpha_beta_search(board: Board) -> tuple:
        v, move = Search.max_val(Board(copy.deepcopy(board.grid)), -2, 2)
        return move

    def max_val(board: Board, alpha: int, beta: int) -> tuple:
        # check winner
        winner: str = board.winner()
        if winner != None:
            return (utility[winner], None)
        
        best_v: int = -2
        # Get actions
        actions: list = Player.get_actions(board.grid)
        for a in actions:
            new_board: Board = Board(copy.deepcopy(board.grid))
            new_board.put(Player.get_turn(new_board.grid), a)    # Update the board
            v, move = Search.min_val(new_board, alpha, beta)
            if v > best_v:
                best_v, best_move = v, a
                alpha = max(alpha, best_v)      # lower bound update
            if best_v >= beta: return (best_v, best_move)   # Prune at most
        return (best_v, best_move)


    def min_val(board: Board, alpha: int, beta: int) -> tuple:
        
        # check winner
        winner: str = board.winner()
        if winner != None:
            return (utility[winner], None)
        
        best_v: int = 2
        # Get actions
        actions: list = Player.get_actions(board.grid)
        for a in actions:
            new_board: Board = Board(copy.deepcopy(board.grid))
            new_board.put(Player.get_turn(new_board.grid), a)    # Update the board
            v, move = Search.max_val(new_board, alpha, beta)
            if v < best_v:
                best_v, best_move = v, a
                beta = min(beta, best_v)      # upper bound update
            if best_v <= alpha: return (best_v, best_move)   # Prune at least
        return (best_v, best_move)


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

    def get_actions(board: list) -> list:
        actions: list = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    actions.append((i,j))
        return actions

    def ai_turn(board: Board):
        winner: str = board.winner()
        if winner != None: return
        move: tuple = Search.alpha_beta_search(board)
        board.put(Player.get_turn(board.grid), move)


# Execute when file is ran
if __name__ == '__main__':

    # starting grid
    grid: list = [
        ['','',''],
        ['','',''],
        ['','','']
    ]

    # game logic
    my_board: Board = Board(grid)
    choice: str = None
    while True:
        choice = input("Go first? (y/n): ").lower()
        if choice == 'n':
            utility['X'], utility['O'] = utility['O'], utility['X']

            # COM first
            print('COM turn')
            actions = Player.get_actions(my_board.grid)
            my_board.put(Player.get_turn(my_board.grid), random.choice(actions))
            break
        elif choice == 'y':
            break
        
    while(my_board.winner() == None):
        my_board.show()
        print("Player turn")
        row: int = int(input('Row: '))
        col: int = int(input('Col: '))
        try:
            my_board.put(Player.get_turn(my_board.grid), (row-1, col-1))
            # AI turn
            print('COM turn')
            Player.ai_turn(my_board)
        except:
            print("Invalid Cell")

        
    
    my_board.show()
    print(f"{my_board.winner()} {'wins!' if my_board.winner() != '' else 'Draw!'}")