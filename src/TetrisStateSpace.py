"""
Our original state space specification was flawed.

Although our state space variables were fine, our transition function over-complicated the state space by a large amount.
This included features that would massively expand the state space beyond what was necessary for each successor state.
These features were things that could be handled by our visualizer/simulator, and did not need to be included within the
state space.

A single new transition will replace a few of the documented ones:
The place transition T(s, "place", y, o, p):
    This transition takes the provided column "y" alongside the provided orientation "o" and computes the lowest row that
    the piece could be placed without overlapping filled board cells. It then writes this piece onto the board by copying
    the current board and filling in all tile locations occupied by the piece.

    Then, it calculates which rows are cleared, adjusting the board accordingly and incrementing the lines cleared variable.
    Finally it takes the given next piece and puts it in the next queue. This allows for proper branching, while our simulator
    emulates nondeterminism.


This single transition accounts for all of the other ones, excluding those that were solely for the purpose of simulation,
(e.g. gravity, etc), which will be implemented in our simulator and not the state space.
"""

import copy

"""
Mappings of each tetris type and possible orientations to a 2D array representings its values.
Some shapes have less orientation options than others as multiple orientations are identical.
For example, there is no point iterating through four different orientations of a square.
"""
SHAPES = {
    "O": {
        0: [[1,1],
            [1,1]]
    },
    "I": {
        0: [[1],
            [1],
            [1],
            [1]],
        1: [[1,1,1,1]]
    },
    "S": {
        0: [[0,1,1],
            [1,1,0]],
        1: [[1,0],
            [1,1],
            [0,1]]
    },
    "Z": {
        0: [[1,1,0],
            [0,1,1]],
        1: [[0,1],
            [1,1],
            [1,0]]
    },
    "L": {
        0: [[1,0],
            [1,0],
            [1,1]],
        1: [[1,1,1],
            [1,0,0]],
        2: [[1,1],
            [0,1],
            [0,1]],
        3: [[0,0,1],
            [1,1,1]]
    },
    "J": {
        0: [[0,1],
            [0,1],
            [1,1]],
        1: [[1,0,0],
            [1,1,1]],
        2: [[1,1],
            [1,0],
            [1,0]],
        3: [[1,1,1],
            [0,0,1]]
    },
    "T": {
        0: [[1,1,1],
            [0,1,0]],
        1: [[1,0],
            [1,1],
            [1,0]],
        2: [[0,1,0],
            [1,1,1]],
        3: [[0,1],
            [1,1],
            [0,1]]
    }
}

class TetrisStateSpace:
    """
    Valid tetrimones, defined columns and rows constants
    """
    VALID_SHAPES = {"O", "I", "S", "Z", "L", "J", "T"}
    COLUMNS = 10
    ROWS = 20
    
    def __init__(self, board, queue, lines, cache=True):
        """
        Instantiate this state space and validate provided variables
        """

        # Validate the board
        if not isinstance(board, list):
            raise TypeError("board must be a list of lists")

        if len(board) != self.ROWS:
            raise ValueError("board must have exactly 20 rows")

        for row in board:
            if not isinstance(row, list):
                raise TypeError("board rows must be lists")

            if len(row) != self.COLUMNS:
                raise ValueError("each board row must have exactly 10 columns")

            for cell in row:
                if cell not in (0, 1):
                    raise ValueError("board cells must be 0 or 1")

        # Validate queue
        if not (isinstance(queue, (list, tuple)) and len(queue) == 3):
            raise ValueError("next must be a list/tuple of length 3")

        for shape in queue:
            if shape not in self.VALID_SHAPES:
                raise ValueError(f"invalid piece '{shape}' in next queue")

        # Validate lines
        if not isinstance(lines, int):
            raise TypeError("lines must be an integer")

        if lines < 0: 
            raise ValueError("lines cannot be negative")

        # Assignments
        self.board = board
        self.queue = list(queue)
        self.lines = lines
        self.cache = cache
        self.cached_placements = None
        self.cached_grids = {}


    def _occupied_cells(self, grid, row, col):
        """
        Given a grid representing a shape in some orientation, the desired row and column for the
        shape to be dropped, return a list of (x, y) coordinates in the main board representing
        the tiles that need to be filled. If there is some contradiction, for example one or more
        of the tiles is already occupied or if 
        """
        cells = []

        for i, grid_row in enumerate(grid):
            for j, cell in enumerate(grid_row):
                if cell == 1:
                    board_i = row + i
                    board_j = col + j

                    if board_i < 0 or board_i >= self.ROWS or board_j < 0 or board_j >= self.COLUMNS:
                        return None

                    if self.board[board_i][board_j] == 1:
                        return None

                    cells.append((board_i, board_j))

        return cells
    
    def _drop_location(self, piece, col, orientation):
        """
        Given a grid representing a shape in some orientation and a target column,
        return the list of (row, col) cells where the piece would come to rest
        if dropped straight down in that column. Return None if it cannot be
        placed anywhere in that column.
        """
        key = (piece, col, orientation)

        if self.cache and key in self.cached_grids:
            return self.cached_grids[key]
            
        grid = SHAPES[piece][orientation]
        grid_height = len(grid)
        last_cells = None

        for row in range(self.ROWS - grid_height + 1):
            cells = self._occupied_cells(grid, row, col)

            if cells is None:
                break

            last_cells = cells

        if self.cache:
            self.cached_grids[key] = last_cells

        return last_cells

    def clone(self):
        """
        Clones this state space
        """
        return TetrisStateSpace(copy.deepcopy(self.board), self.queue.copy(), self.lines, cache=self.cache)
    
    def is_terminal(self):
        """
        Returns whether or not this state space is terminal
        """
        return len(self.legal_placements()) == 0
    
    def legal_placements(self):
        """
        Returns a list of legal placements in (col, orientation) format.
        """
        if self.cache and self.cached_placements is not None:
            return self.cached_placements

        placements = []

        piece = self.queue[0]
        orientations = SHAPES[piece]

        for orientation, grid in orientations.items():
            grid_width = len(grid[0])

            for col in range(self.COLUMNS - grid_width + 1):
                cells = self._drop_location(piece, col, orientation)

                if cells is not None:
                    key = (col, orientation)
                    placements.append(key)

        if self.cache:
            self.cached_placements = placements

        return placements

    def place_piece(self, y, o, p):
        """
        Places the current piece in the provided column and orientation, and then sets
        the next piece to be p for the new state.
        """
        if p not in self.VALID_SHAPES:
            raise ValueError(f"invalid piece type '{p}'")

        piece = self.queue[0]

        if o not in SHAPES[piece]:
            raise ValueError(f"invalid orientation {o} for piece '{piece}'")

        cells = self._drop_location(piece, y, o)

        if cells is None:
            raise ValueError("collision at final landing position")

        new_board = copy.deepcopy(self.board)
        new_queue = self.queue.copy()
        new_lines = self.lines

        for (i, j) in cells:
            new_board[i][j] = 1

        full_rows = [r for r in range(self.ROWS) if all(new_board[r][c] == 1 for c in range(self.COLUMNS))]

        if full_rows:
            num_cleared = len(full_rows)
            new_lines += num_cleared

            for r in sorted(full_rows, reverse=True):
                del new_board[r]

            for _ in range(num_cleared):
                new_board.insert(0, [0]*self.COLUMNS)

        new_queue[0] = new_queue[1]
        new_queue[1] = new_queue[2]
        new_queue[2] = p

        return TetrisStateSpace(new_board, new_queue, new_lines)
    

    
