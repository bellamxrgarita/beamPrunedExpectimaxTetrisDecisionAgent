from TetrisStateSpace import TetrisStateSpace

HEIGHT_WEIGHT = -0.51
LINES_WEIGHT = 0.76
HOLES_WEIGHT = -0.36
BUMPINESS_WEIGHT = -0.18

class expectimaxAgent:
    def __init__(self, agentName: str):
        self.agentName = agentName

    # This needed to be adjusted to simulate the next
    def getAction(self, currGameState: TetrisStateSpace, depth: int = 3):
        #loops over all potential moves and returns the one with the highest score
        possibleMoves = currGameState.legal_placements()

        if not possibleMoves:
            return None

        bestScore = -float("inf")
        bestMove = None

        for (col, orientation) in possibleMoves:
            # but expectiMax now properly alternates max/chance and uses depth
            score = self.expectiMax(currGameState, depth, (col, orientation), False)
            #print(score)
            if score > bestScore:
                bestScore = score
                bestMove = (col, orientation)
            
        return bestMove
    

    # the current gamestate actually has the piece that we are supposed to put down stored in the queue
    # the queue contains the next 3 pieces that will be placed by the player
    # should this be modified to actualy take those 3 next pieces?
    def expectiMax(self, gameState: TetrisStateSpace, depth: int, action, isMaxAgent: bool):
        #alternating maxAgent and randomAgent
        #simulate placing each piece, and use evaluation function on each move

        # If terminal, stop
        if gameState.is_terminal() or depth <=0:
            return self.evaluationFunction(gameState)

        # If depth reached, stop
        #if isMaxAgent or depth <= 0:
            #return self.evaluationFunction(gameState)
    
        if isMaxAgent:
            maxScore = -float("inf")

            for (col, orientation) in gameState.legal_placements():
                score = self.expectiMax(gameState, depth - 1 , (col, orientation), isMaxAgent=False)

                maxScore = max(score, maxScore)

            return maxScore
        else:
            (col, orientation) = action
            expectedScore = 0

            # for the chance node, simulate the random next piece from the game
            # don't decrement depth
            for piece in gameState.VALID_SHAPES:
                newState = gameState.place_piece(col, orientation, piece)
                # max agent does not need action
                score = self.expectiMax(newState, depth , None, isMaxAgent=True)
                expectedScore += score / len(gameState.VALID_SHAPES)

            return expectedScore
    
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
