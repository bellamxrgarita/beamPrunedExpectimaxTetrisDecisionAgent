from TetrisStateSpace import TetrisStateSpace
from expectimaxAgent import expectimaxAgent 
from src.beamsearchChanceAgent import beamsearchChanceAgent
from beamPrunedExpectimaxAgent import beamPrunedExpectimaxAgent

import sys

def print_board(board):
    print("-" * 22)
    for row in board:
        line = "|"
        for cell in row:
            line += "[]" if cell == 1 else "  "
        line += "|"
        print(line)
    print("-" * 22)

# Created to theoretically validate expectimax's depth 2 behavior before game simulator has been created 
def test_i_piece_scenario(agentType):
    print("\n=== TEST 1: The Tetris Scenario ===")
    print("goal: the agent should drop the 'I' piece into the empty right column.")
    
    # 1. SETUP: create a custom board
    # 20 rows, 10 columns. 
    # we will fill the bottom 4 rows with blocks, leaving Column 9 empty.
    custom_board = [[0] * 10 for _ in range(20)]
    
    # fill bottom 4 rows (rows 16-19) except the last column (col 9)
    for r in range(16, 20):
        for c in range(0, 9):
            custom_board[r][c] = 1

    # 2. SETUP: define the queue
    # Queue: [Current='I', Next='O', NextNext='T']
    # The 'I' piece is the hero here.
    queue = ["I", "O", "T"]
    
    # 3. INITIALIZE STATE
    initial_state = TetrisStateSpace(custom_board, queue, lines=0)
    
    print("initial board state:")
    print_board(initial_state.board)
    print(f"queue: {queue}")
    
    if agentType == "beamSearchChance":
        print("\nBeam Search Chance Layer")
        agent = beamsearchChanceAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "expectimax":
        print("\nExpectimax")
        agent = expectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "beamPrunedExpectimaxAgent":
        agent = beamPrunedExpectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    
    # we expect the move to be Column 9 (or 6 depending on rotation offset)
    # orientation 1 of 'I' is vertical [[1,1,1,1]].
    best_move = agent.getAction(initial_state)
    
    print(f"agent chose action: {best_move}")
    
    if best_move:
        col, orientation = best_move
        # 5. SIMULATE THE RESULT
        # we assume the random piece spawning next is 'S' (just for testing)
        next_state = initial_state.place_piece(col, orientation, "S")
    
        print("\nresulting board:")
        print_board(next_state.board)
        print(f"Lines Cleared Total: {next_state.lines}")
        
        # validation
        if next_state.lines == 4:
            print("SUCCESS: Agent cleared 4 lines (Tetris)!")
        else:
            print("FAILURE: Agent missed the Tetris.")
    else:
        print("FAILURE: Agent returned None (Game Over or Bug).")


# Created to theoretically validate depth 2 expectimax's behavior before game simulator has been created 
def test_survival_scenario(agentType):
    print("\n=== TEST 2: Worst Case Scenario ===")
    print("goal: the board is high. agent must place piece low to survive.")
    
    custom_board = [[0] * 10 for _ in range(20)]
    
    # build a tower in column 5 that is dangerously high (up to row 2)
    for r in range(2, 20):
        custom_board[r][5] = 1
        
    queue = ["O", "T", "L"]
    initial_state = TetrisStateSpace(custom_board, queue, lines=0)
    print_board(initial_state.board)
    print(f"queue: {queue}")
    
    if agentType == "beamSearchChance":
        print("\nBeam Search Chance Layer")
        agent = beamsearchChanceAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "expectimax":
        print("\nExpectimax")
        agent = expectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "beamPrunedExpectimaxAgent":
        agent = beamPrunedExpectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    
    print(f"agent chose: {best_move}")
    
    if best_move and best_move[0] != 5:
        col, orientation = best_move
        # 5. SIMULATE THE RESULT
        # we assume the random piece spawning next is 'S' (just for testing)
        next_state = initial_state.place_piece(col, orientation, "S")
        print_board(next_state.board)
         # should not stack on col 5
        print("SUCCESS: Agent avoided the high tower.")

    else:
        print(f"FAILURE: Agent stacked on the tower or crashed. Move: {best_move}")

def rotation_required(agentType):
    print("\n === Rotation Required TEST 3: ===")
    print("goal: agent must rotate piece to clear a line.")


    custom_board = [[0] * 10 for _ in range(20)]

    for r in range(17, 20):
        for c in range(5):
            custom_board[r][c] = 1

    queue = ["I", "O", "T"]
    initial_state = TetrisStateSpace(custom_board, queue, lines=0)

    print("initial board state:")
    print_board(initial_state.board)
    print(f"queue: {queue}")


    if agentType == "beamSearchChance":
        print("\nBeam Search Chance Layer")
        agent = beamsearchChanceAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "expectimax":
        print("\nExpectimax")
        agent = expectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "beamPrunedExpectimaxAgent":
        agent = beamPrunedExpectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)

    best_move = agent.getAction(initial_state)

    print(f"agent chose: {best_move}")
    if best_move:
        col, orientation = best_move
        nextState = initial_state.place_piece(col, orientation, "S")
        print("\nresulting board:")
        print_board(nextState.board)
        print(f"Lines Cleared Total: {nextState.lines}")

        #check if piece was placed horizontal
        if orientation == 1:
            print("SUCCESS: Agent picked orientation that rotates 'I' optimally.")
        else: 
            print("FAIL: Agent did not rotate 'I' optimally.")


def hole_avoidance(agentType):
    print("\n === Hole Avoidance TEST 4: ===")
    print("goal: agent must not create new holes or bury existing ones")

    custom_board = [[0] * 10 for _ in range(20)]

    #make one block hole at 18, 4
    for r in range(17, 20):
        for c in range(5):
            if not (r == 18 and c == 4):
                custom_board[r][c] = 1
    
    queue = ["T", "L", "O"]
    initial_state = TetrisStateSpace(custom_board, queue, lines=0)

    print("initial board state:")
    print_board(initial_state.board)
    print(f"queue: {queue}")

    if agentType == "beamSearchChance":
        print("\nBeam Search Chance Layer")
        agent = beamsearchChanceAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "expectimax":
        print("\nExpectimax")
        agent = expectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)
    elif agentType == "beamPrunedExpectimaxAgent":
        agent = beamPrunedExpectimaxAgent("TestAgent")
        best_move = agent.getAction(initial_state)

    best_move = agent.getAction(initial_state)

    print(f"agent chose: {best_move}")
    if best_move:
        col, orientation = best_move
        nextState = initial_state.place_piece(col, orientation, "S")
        print("\nresulting board:")
        print_board(nextState.board)
        print(f"Lines Cleared Total: {nextState.lines}")

        #check if hole was buried
        if nextState.board[18][4] != 1:
            print("SUCCESS: Agent avoided burying the hole.")
        else: 
            print("FAIL: Agent buried the hole, which is not optimal for future plays.")

def run_all_tests(agentType: str):
    """
    Run all test scenarios for the given agent type.

    agentType must be one of: "beamSearchChance", "expectimax", "beamPrunedExpectimaxAgent".
    """
    valid_types = {"beamSearchChance", "expectimax", "beamPrunedExpectimaxAgent"}
    if agentType not in valid_types:
        print(f"Invalid agent type: {agentType}")
        print("Valid options: beamSearchChance, expectimax, beamPrunedExpectimaxAgent")
        return

    print(f"\n==============================")
    print(f" Running tests for: {agentType} ")
    print(f"==============================")

    test_i_piece_scenario(agentType)
    test_survival_scenario(agentType)
    rotation_required(agentType)
    hole_avoidance(agentType)


if __name__ == "__main__":
    # expect exactly one CLI argument: the agent type
    if len(sys.argv) != 2:
        print("Usage: python agentTester.py [beamSearchChance|expectimax|beamPrunedExpectimaxAgent]")
        sys.exit(1)

    arg_agent_type = sys.argv[1]
    run_all_tests(arg_agent_type)
