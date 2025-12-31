# game simulator class that should simulate next piece the game will play

'''
Sources used for this
Understanding the game flow for tetris
https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-2

TKinter
https://docs.python.org/3/library/tkinter.html 

'''


'''
Notes:

Choosing the next uhhh piece thatll be randomly generated that we need to place down

kinda rough doing this without and agent but we'll set it up for now

one of 7 possible pieces being put into the queue

this will be giving the expectimax the possible state 

initializes the state transitions


state from expectimax will be given to the game simulator which will
generate the next piece that will get handled by the expectimax

expectimax returns and action, the gamesim does that action then randomly generates
the next piece for expectimax to handle 

'''
#the python GUI thing (According to google summary)
import tkinter as tk
import time
import random
import copy
from TetrisStateSpace import TetrisStateSpace, SHAPES
import sys 

# config items
CELL_SIZE = 30
COLS = 10
ROWS = 20
SIDEBAR_WIDTH = 150
# Speed of the falling animation 
DELAY = 0.05 

#Pieces and their respective colors
PIECE_COLORS = {
    "I": "cyan", "O": "yellow", "T": "purple", 
    "S": "green", "Z": "red", "J": "blue", "L": "orange"
}
PIECES = list(PIECE_COLORS.keys())

class TetrisApp:
    def __init__(self, agent, headless = False):
        self.agent = agent
        self.headless = headless
        self.actions_taken = 0
        
        #Items that need to be initialized regardless of GUI or not GUI
        # make an empty board (logical)
        self.logical_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        # make the game queue with 3 random pieces
        self.queue = [random.choice(PIECES) for _ in range(3)]
        # initial State Object
        self.current_state = TetrisStateSpace(self.logical_board, self.queue, 0)
        
        
        
        #GUI setup if not headless
        if not self.headless:
            #  "Shadow Board" for colors (visual)
            self.color_board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
            # Setup the GUI Window
            self.root = tk.Tk()
            self.root.title("Tetris Simulator")
            self.canvas = tk.Canvas(
                self.root,
                width=COLS * CELL_SIZE + SIDEBAR_WIDTH, 
                height=ROWS * CELL_SIZE, 
                bg="black"
            )
            self.canvas.pack()
            
            # Begin game loop
            self.root.after(100, self.game_loop_gui)
            self.root.mainloop()
        
        # else:
        #     # Begin game loop
        #     self.game_loop_headless()

    
    #Redraws the permanent blocks on the board
    def draw_board(self):
        self.canvas.delete("all")
        
        #main board
        for r in range(ROWS):
            for c in range(COLS):
                color = self.color_board[r][c]
                if color:
                    self.draw_cell(r, c, color)
                    
        #queue side bar
        sep_x = COLS * CELL_SIZE
        self.canvas.create_line(sep_x, 0, sep_x, ROWS * CELL_SIZE, fill="white", width=2)
        
        # Draw Score
        self.canvas.create_text(
            50, 20, text=f"Lines: {self.current_state.lines}", 
            fill="white", anchor="w", font=("Arial", 14)
        ) 
        
        self.canvas.create_text(
            sep_x + 10, 50, text=f"Moves: {self.actions_taken}", 
            fill="gray", anchor="w", font=("Arial", 12)
        )
        
        #The queue itself
        self.canvas.create_text(
            sep_x + 10, 90, 
            text="Next:", 
            fill="white", anchor="w", font=("Arial", 14)
        )
        
        #pull the next
        current_y = 120
        for piece in self.current_state.queue:
            self.draw_piece_preview(piece, sep_x + 40, current_y)
            current_y += 80
        
       

    #helper to draw individual squares 
    def draw_cell(self, row, col, color, tag=None):
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", tags=tag)
        
    #mini shape drawer for the queue 
    def draw_piece_preview(self, piece, x, y):
        shape = SHAPES[piece][0] 
        color = PIECE_COLORS[piece]
        
        # Mini cell size for preview
        mini_size = 20 
        
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c] == 1:
                    px = x + c * mini_size
                    py = y + r * mini_size
                    self.canvas.create_rectangle(
                        px, py, px + mini_size, py + mini_size, 
                        fill=color, outline="black"
                    )

    def animate_fall(self, piece_type, col, orientation, target_cells):
        #grab shape grid to know what to draw
        grid = SHAPES[piece_type][orientation]
        grid_h = len(grid)
        grid_w = len(grid[0])
        
        # Calculate the lowest row in the target (where it lands)
        if not target_cells: return
        
        
        color = PIECE_COLORS[piece_type]
        
        # animation loop
        final_top_row = min(r for r, c in target_cells)

        for curr_r in range(-grid_h, final_top_row + 1):
            # Clear previous animation frame (tags="anim")
            self.canvas.delete("anim")
            
            # Draw the piece at current row 'curr_r'
            for r in range(grid_h):
                for c in range(grid_w):
                    if grid[r][c] == 1:
                        draw_r = curr_r + r
                        draw_c = col + c
                        # Only draw if on screen
                        if 0 <= draw_r < ROWS:
                            self.draw_cell(draw_r, draw_c, color, tag="anim")
                            
            # Force Tkinter to redraw immediately
            self.root.update() 
            time.sleep(DELAY) 
            
        self.canvas.delete("anim")
        
    
    
    # now we detect lines that were cleared which i think is the hardest thing
    # If a row disappeared in the new board, we need to shift colors down
    # This is a bit weird cuz `place_piece` already deleted the logical row
    # My best bet rn is i think u just re-sync color board based on logic board structure.
    

    def update_color_board(self, old_board, new_board, piece_type):
        current_color = PIECE_COLORS[piece_type]
         # If a cell is 0 in old but 1 in new, it's the new piece.
        for r in range(ROWS):
            for c in range(COLS):
                if old_board[r][c] == 0 and new_board[r][c] == 1:
                    self.color_board[r][c] = current_color
        
        
        for r in range(ROWS):
            for c in range(COLS):
                if new_board[r][c] == 0:
                    self.color_board[r][c] = None
                elif self.color_board[r][c] is None:
                    # This handles the case where lines cleared and blocks shifted down
                    #i think this could lose the specific color of shifted blocks 
                    self.color_board[r][c] = "gray"
        
        

    def game_loop_gui(self):
        if self.current_state.is_terminal():
            print("Game Over")
            self.canvas.create_text(
                COLS*CELL_SIZE/2, ROWS*CELL_SIZE/2, 
                text="GAME OVER", fill="red", font=("Arial", 24)
            )
            return

        #redraw current static state
        self.draw_board()
        self.root.update()

        #Get Action from agent 
        action = self.agent.getAction(self.current_state)
        if action is None:
            return 
        col, orientation = action
        current_piece_type = self.current_state.queue[0]

        # calculate "Target Cells" for animation (state space)
        target_cells = self.current_state._drop_location(current_piece_type, col, orientation)
        #animate the falling
        self.animate_fall(current_piece_type, col, orientation, target_cells)

        #randomly pick a piece for the queue
        next_random_piece = random.choice(PIECES)

        #Update Logic
        try:
            #Update Color Board with the new piece before we clear
            current_color = PIECE_COLORS[current_piece_type]
            for r, c in target_cells:
                self.color_board[r][c] = current_color
            
            #Like with last itratiuon, we make a temp logic board to detect which lines are full
            temp_board = copy.deepcopy(self.current_state.board)
            for r, c in target_cells:
                temp_board[r][c] = 1
                
            full_rows = [r for r in range(ROWS) if all(temp_board[r][c] == 1 for c in range(COLS))]

            #Logic Transition
            next_random_piece = random.choice(PIECES)
            self.current_state = self.current_state.place_piece(col, orientation, next_random_piece)
            
            self.actions_taken += 1
            
            #Now we do the visual line clear 
            if full_rows:
                # Remove rows from color board
                for r in sorted(full_rows, reverse=True):
                    del self.color_board[r]
                # Add new empty rows at top
                for _ in range(len(full_rows)):
                    self.color_board.insert(0, [None for _ in range(COLS)])
            
        except ValueError as e:
            print(f"Error: {e}")
            return

        #keep the loop going
        self.root.after(10, self.game_loop_gui)
        
        
    #game loop that doesnt make a pop up
    def game_loop_headless(self):
        print(f" Starting Headless Simulation ({self.agent.agentName})")
        start_time = time.time()
        
        while not self.current_state.is_terminal():
            # grab action
            action = self.agent.getAction(self.current_state)
            if action is None: break
            
            col, orientation = action
            
            # Logic Update
            try:
                next_random_piece = random.choice(PIECES)
                self.current_state = self.current_state.place_piece(col, orientation, next_random_piece)
                
                self.actions_taken += 1
                
                if self.actions_taken % 5 == 0:
                    print(f"Actions: {self.actions_taken} | Lines: {self.current_state.lines}")
                    
            except ValueError:
                break
        
        end_time = time.time()
        print(f"\nGAME OVER")
        print(f"Total Actions: {self.actions_taken}")
        print(f"Total Lines:   {self.current_state.lines}")
        print(f"Time Elapsed:  {end_time - start_time:.2f}s")

    #game loop that takes input to control the number of pieces placed and rounds simulated.
    def limitGameLoop(self, maxPiecesPlayed):
        start_time = time.time()

        while not self.current_state.is_terminal():
            # grab action
            action = self.agent.getAction(self.current_state)
            if action is None: 
                break
            
            col, orientation = action
            next_random_piece = random.choice(PIECES)

            
            # Logic Update
            try:
                self.current_state = self.current_state.place_piece(col, orientation, next_random_piece)
                self.actions_taken += 1
                
            except ValueError:
                break

            if maxPiecesPlayed is not None and self.actions_taken >= maxPiecesPlayed:
                break

            end_time = time.time()

        return {
            "lines": self.current_state.lines,
            "pieces": self.actions_taken,
            "time": end_time - start_time
        }


if __name__ == "__main__":
    from beamsearchChanceAgent import beamsearchChanceAgent
    from beamPrunedExpectimaxAgent import beamPrunedExpectimaxAgent
    from expectimaxAgent import expectimaxAgent

    if len(sys.argv) != 2:
        print("Usage: python3 gameSimulator.py [beamSearchChance|expectimax|beamPrunedExpectimax]")
        sys.exit(1)

    agentType = sys.argv[1]
    if (agentType not in ["beamSearchChance", "expectimax","beamPrunedExpectimax"]):
        print("Please enter a valid agentType as an argument to simulate. The valid options are `beamSearchChance`, `beamPrunedExpectimax`, and `expectimax`")
        sys.exit(1)
    if (agentType == "beamSearchChance"):
        bot =  beamsearchChanceAgent("BeamChanceBot")
    elif agentType == "beamPrunedExpectimax":
        bot = beamPrunedExpectimaxAgent("BeamPrunedExpectimax")
    else:
        bot = expectimaxAgent("expectimaxBot")
    
    # True = No Pop up (Fast)
    # False = Pop up window (Animation)
    HEADLESS_MODE = False
    
    # Start App
    app = TetrisApp(bot, headless=HEADLESS_MODE)
