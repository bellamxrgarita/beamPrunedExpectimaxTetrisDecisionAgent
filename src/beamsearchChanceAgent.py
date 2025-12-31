from TetrisStateSpace import TetrisStateSpace
from operator import itemgetter

# punish height increases because they reduce available space and increase risk of topping out
HEIGHT_WEIGHT = -0.51
# reward number of lines cleared 
LINES_WEIGHT = 0.76
# punish hole creation because they make it impossible to clear lines for the blocks around them
HOLES_WEIGHT = -0.36
# punish bumpiness to prioritize moves that lead to a flatter board space 
BUMPINESS_WEIGHT = -0.18


"""
Expectimax-Beam Search Hybrid Approach:
Attempting to take advantage of Beam search and expectimax by simulating a deterministic beam search for queue[0], queue[1], and queue[2]
and then implementing a chance layer for the unknown random piece that's going to be added to the queue after

Why Combine Beam Search with Expectimax:
In expectimax, the number of state spaces that need to be evaluated explodes in size when trying to look more than 3 turns ahead. 
I created this agent with the intention of having the agent make more informed decisions by taking the pieces that
are stored in the queue in the gamestate, however after devling deeper and discussing the model's weaknesses in modeling Tetris' stochastic nature with my teammates, 
I realized it would be better to instead try investing more time into optimizing the expectimax agent.
"""
class beamsearchChanceAgent:

    def __init__(self, agentName: str):
        self.agentName = agentName
        self.beam_width = 4

    def getAction(self, currGameState: TetrisStateSpace):
        # LAYER 1: piece at queue[0]
        moves = currGameState.legal_placements()
        if not moves: 
            return None

        candidates_layer1 = []
        #place current piece in all possible legal placements and evaluate each successor state's expected value
        for col, orient in moves:
            # this "O" that's being placed is a dummy piece that we will never simulate
            # the state_space function needs to receive the "next piece being added to the queue" but it's never taken into account for future predictions
            next_state = currGameState.place_piece(col, orient, "O")
            score = self.evaluationFunction(next_state)
            candidates_layer1.append((score, (col, orient), next_state))

        #print("Candidate Layer 1:")
        #for item in candidates_layer1:
            #print(item[:2])
        
        # pruning to have the beam contain only the top 4 initial moves with the greatest evaluated expected scores 
        beam = self.pruneStates(candidates_layer1)

        # LAYER 2: piece at queue[1] 
        candidates_layer2 = []

        # go through each successor state from layer 1 simulate placing the next piece 
        # in the queue in all possible legal placements and evaluate each of those successor state's expected value
        # length of candidate_layer2 = 4 * number of legal placements of moves per state
        for _, initial_move, state_q1 in beam:
           moves_q1 = state_q1.legal_placements()
           if not moves_q1: continue
           for col, orient in moves_q1:
                # this "O" that's being placed is a dummy piece that we will never simulate
                # the state_space function needs to receive the "next piece being added to the queue" but it's never taken into account for future predictions
                state_q2 = state_q1.place_piece(col, orient, "O")
                score = self.evaluationFunction(state_q2)
                candidates_layer2.append((score, initial_move, state_q2))

        # fallback
        if not candidates_layer2:
            return beam[0][1] if beam else None

        #print("Candidate Layer 2:")
        #for item in candidates_layer2:
            #print(item[:2])
        
        # pruning to have the beam contain only the top 4 initial moves with the greatest evaluated expected scores
        # after simulating placement of queue[1]
        beam_layer2 = self.pruneStates(candidates_layer2)

        # LAYER 3: piece at queue[2]
        candidates_layer3 = []

        # go through each survivor of layer 2 and generate successor state for legal moves to place piece at queue[2]
        for _, initial_move, state_q2 in beam_layer2:
            moves_q2 = state_q2.legal_placements()
            if not moves_q2: continue

            for col, orient in moves_q2:
                # edge of the known universe 
                # this "O" that's being placed is a dummy piece that we will never simulate
                # the state_space function needs to receive the "next piece being added to the queue" but it's never taken into account for future predictions
                state_q3 = state_q2.place_piece(col, orient, "O")
                
                # CHANCE LAYER Expectimax Tail
                # now we account for the unknown random piece spawning after placing the last known piece down 
                expected_value = self.runChanceLayer(state_q3)
                candidates_layer3.append((expected_value, initial_move, state_q3))
            
        if not candidates_layer3:
            return beam_layer2[0][1] if beam_layer2 else None

        # sort Layer 3 results to find best initial action with highest expected value 
        best_candidate = self.pruneStates(candidates_layer3)[0]

        # return the move associated with the best score
        return best_candidate[1]
    
    # it finds the average case scenario of the current given board state if a random piece were to be played onto it
    def runChanceLayer(self, state: TetrisStateSpace):
        """
        simulates the Agent playing optimally against every possible random piece
        that could spawn.
        """
        total_score = 0
        probability = 1.0 / 7.0
        valid_shapes = ["O", "I", "S", "Z", "L", "J", "T"]
        
        for piece in valid_shapes:
            # 1. Create a hypothetical universe where 'piece' is next
            temp_state = state.clone()
            temp_state.queue[0] = piece 
            
            # 2. Find best move for this specific piece
            # we can now use the standard helper since queue[0] is correct
            moves = temp_state.legal_placements()
            
            if not moves:
                # if a piece spawns and we can't place it -> Game Over
                best_response = -float('inf')
            else:
                best_response = -float('inf')
                for col, orient in moves:
                    child_state = temp_state.place_piece(col, orient, "O")
                    score = self.evaluationFunction(child_state)
                    
                    if score > best_response:
                        best_response = score
            
            total_score += best_response * probability

        return total_score

    def pruneStates(self, candidates):
        # Sort in-place by score (Highest first)
        candidates.sort(key=itemgetter(0), reverse=True)
        return candidates[:self.beam_width]
    
    # Referencing Pierre Dellacherie's Algorithm 
    # modify this to also make this take the queue's "fit" to the board 
    def evaluationFunction(self, currGameState: TetrisStateSpace):
        board = currGameState.board
        rows = len(board)
        cols = len(board[0])

        aggregateHeight = 0
        columnHeights = [0] * cols
        holes = 0

        for c in range(cols):
            blockFound = False

            for r in range(rows):
                if board[r][c] == 1:
                    if not blockFound:
                        h = rows - r
                        columnHeights[c] = h
                        aggregateHeight += h
                        blockFound = True
                elif blockFound and board[r][c] == 0:
                    holes += 1

        bumpiness = 0

        #sum of absolute difference between adjacent column height
        for c in range(cols - 1):
            bumpiness += abs(columnHeights[c] - columnHeights[c+1])

        score = (
            HEIGHT_WEIGHT * aggregateHeight
            + HOLES_WEIGHT * holes
            + BUMPINESS_WEIGHT * bumpiness
            + LINES_WEIGHT * currGameState.lines
        )

        return score
    

    
    
