from eightpuzzle import EightPuzzle

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