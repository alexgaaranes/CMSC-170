class State:
    state: list = None
    neighbors = []

    def __init__ (self, state: list):
        self.state = state.copy()

    def __repr__(self):
        return f"State(state={self.state})"

    def get_neighbors(self, zLoc: list):
        zrow = zLoc[0]
        zcol = zLoc[1]
        for i, j in [(zrow-1, zcol), (zrow+1, zcol), (zrow, zcol-1), (zrow, zcol+1)]:
            if i >= 0 and i < 3 and j >= 0 and j < 3:
                temp_state: list = [row.copy() for row in self.state]
                temp_state[zrow][zcol], temp_state[i][j] = temp_state[i][j], temp_state[zrow][zcol]
                print(temp_state)
                self.neighbors.append(temp_state)
    
    def is_goal(state: list):
        goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]
        return state == goal

    def show_neighbors(self):
        for neighbor in self.neighbors:
            print(State.is_goal(neighbor))
            print("_____________")
            for row in neighbor:
                print("| " + " | ".join(row) + " |")
                print("_____________")

