# Responsible Use of AI:
# Extent and Purpose of AI Use:
#   AI was used during the searching/reviewing of python syntax through google.
#   Google implemented AI Overview via Gemini summarizing the content I was searching for.
# Responsible Use Justification:
#   The AI was only used for reviewing python syntax especially the built-in methods for objects.
#   Any code generation or direct prompting for answers was never done. Only for searching purposes.


# Name:     Alexander Gabriel A. Aranes
# Section:  EF-4L

# Tic-Tac-Toe

# Static class for the game grid
class GridMap:
    turn = True    # pertains to 'X' as first turn
    numOfTurns = 0
    hasWinner = False
    map = None

    def clear(): 
        GridMap.map = [
            ['','',''],
            ['','',''],
            ['','','']
        ]
        GridMap.numOfTurns = 0
        GridMap.turn = True
        GridMap.hasWinner = False

    
    # Decode the array element for showing
    def decode(e: str):
        if e == '':
            print("   |", end="")
        else:
            print(f" {e} |", end="")

    # Formats to the stdout the map
    def show():
        print("    1 | 2 | 3 |")
        for i in range(3):
            print(f"{i+1} |", end="")
            for j in range(3):
                GridMap.decode(GridMap.map[i][j])
            print()
    
    # Check for row
    def checkRow(row: int):
        if len(set(GridMap.map[row])) == 1:
            GridMap.hasWinner = True
    
    # Check for col
    def checkCol(col: int):
        grid_col = []
        for i in range(3):
            grid_col.append(GridMap.map[i][col])

        if len(set(grid_col)) == 1:
            GridMap.hasWinner = True

    # Check for win
    def checkWin(row: int, col: int):
        if row != 1 and col != 1: # check corner
            diag = []
            if row == col:  # Check diagonal
                for i in range(3):
                    diag.append(GridMap.map[i][i])
                if len(set(diag)) == 1:
                    GridMap.hasWinner = True
            else:
                for i in range(3):
                    diag.append(GridMap.map[2-i][i])
                if len(set(diag)) == 1:
                    GridMap.hasWinner = True
        # All inputs must check row and col
        GridMap.checkRow(row)
        GridMap.checkCol(col)

    
    # Get the coords of input of the player
    def getMapInput():
        if GridMap.turn:
            print("X turn")
        else:
            print("O turn")
        row = int(input("Enter row: ")) - 1
        col = int(input("Enter col: ")) - 1

        # Check if valid to input
        cell = GridMap.map[row][col]
        if cell == '':
            if GridMap.turn == True:
                GridMap.map[row][col] = 'X'
            else:
                GridMap.map[row][col] = 'O'
            GridMap.turn = not GridMap.turn
            GridMap.numOfTurns += 1
            GridMap.checkWin(row, col)
        else:
            print("\nCell occupied!\n")

# Main Gameplay Loop
def play():
    GridMap.clear()
    while not GridMap.hasWinner:    # Check for winner
        GridMap.show()
        if GridMap.numOfTurns >= 9: # Check if draw
            print("Draw!")
            return
        GridMap.getMapInput()       # Get Input
    GridMap.show()
    if GridMap.turn:                # Evaluate Winner
        print("O wins!")
    else:
        print("X wins!")

# Shows game main menu
def showMenu():
    print("\n===== TIC-TAC-TOE =====")
    print("[1] Play")
    print("[2] Exit")
    print("=======================")

# Main Menu
def main():
    choice = None
    while True:
        showMenu()
        choice = int(input("Choice: "))

        # Evaluate choice
        if choice == 1:
            play()
        elif choice == 2:
            print("\nEXIT\n")
            break
        else:
            print("\nINVALID INPUT\n")
        

# Run the app
if __name__ == '__main__':
    main()
