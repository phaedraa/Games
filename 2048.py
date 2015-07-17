'''
My creation of 2048 game.
'''

import poc_2048_gui
import random    

def main():
    new_game = TwentyFortyEight(4,4)
    poc_2048_gui.run_gui(new_game)

class TwentyFortyEight:
    '''
    Class to run the game logic.
    '''
   
    def __init__(self, grid_height, grid_width):

        self.grid_height = grid_height
        self.grid_width = grid_width
        
        self.UP = 1
        self.DOWN = 2
        self.LEFT = 3
        self.RIGHT = 4

        # Offsets for computing tile indices in each direction.
        self.OFFSETS = {self.UP: (1, 0),
                        self.DOWN: (-1, 0),
                        self.LEFT: (0, 1),
                        self.RIGHT: (0, -1)}
        # Grid span for each direction for grabbing appropriate row/column
        self.SPAN = {self.UP: self.grid_height,
                     self.DOWN: self.grid_height,
                     self.LEFT: self.grid_width,
                     self.RIGHT: self.grid_width}
        
        self.reset() 
        self.initial_tiles_dict = {self.UP: [], self.DOWN: [], 
            self.LEFT: [], self.RIGHT: []}
        height = self.grid_height - 1
        width = self.grid_width - 1
        for key in self.OFFSETS.keys():
            if key == 1:
                for i in range(self.grid_width):
                    self.initial_tiles_dict[self.UP].append((0, i))
            if key == 2:
                for i in range(self.grid_width):
                    self.initial_tiles_dict[self.DOWN].append((height, i))
            if key == 3:
                for i in range(self.grid_height):
                    self.initial_tiles_dict[self.LEFT].append((i, 0))
            if key == 4:
                for i in range(self.grid_height):
                    self.initial_tiles_dict[self.RIGHT].append((i, width))
    
    def reset(self):
        '''
        Reset the game so the grid is empty except for two
        initial tiles.
        '''
        # initialize matrix of all zeros based on input width and height
        self._board = [[0 for row in range(0,self.grid_width)] for \
            col in range(0,self.grid_height)]
        
        # generate 2 new tile values at random nonzero locations
        self.new_tile()
        self.new_tile() 
        
    def __str__(self):
        '''
        Return a string representation of the grid for debugging.
        '''
        temp = list(self._board)
        temp.reverse()
        return str(temp)

    def get_grid_height(self):
        '''
        Get height of the board.
        '''
        return self.grid_height 

    def get_grid_width(self):
        '''
        Get the width of the board.
        '''
        return self.grid_width

    def merge(self, line):
        '''
        Helper function that merges a single row or column in 2048
        '''
        # Use lastmerged as a placeholder index to prevent summing pairs that 
        # have already been summed. Summing of pairs can only occur once.
        lastmerged = None
        pivot = None
        newline = [0]*len(line)
        for i in range(0, len(line)):
            newline[i] = line[i]
        
        for index in range(0, len(line)):
            if newline[index] != 0:
                if pivot == None:
                    pivot = index
                    if lastmerged == None:
                        # Case when everything preceding the first found pivot 
                        # is 0. If this pivot is at first index, don't analyze.
                        if pivot != 0 and newline[0:pivot] == [0] * (pivot):
                            newline[0] = newline[pivot]
                            newline[pivot] = 0
                            pivot = 0
                    else:
                        newline[lastmerged + 1] = newline[pivot]
                        newline[pivot] = 0
                        pivot = lastmerged + 1
                else:
                    if pivot < index:
                        if newline[pivot] == newline[index]:
                            newline[pivot] = 2 * newline[pivot]
                            newline[index] = 0
                            lastmerged = pivot
                            pivot = None
                        elif (index - pivot) > 1:
                            newline[pivot + 1] = newline[index]
                            newline[index] = 0
                            pivot += 1
                        else:
                            pivot = index
        return newline

    def move(self, direction):
        '''
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        '''
        move_vector = self.OFFSETS[direction]
        tile_has_changed = False
        game_won = False
        x = 0
        y = 1
        for index, tile in enumerate(self.initial_tiles_dict[direction]):
            temp = []
            for idx in range(0, self.SPAN[direction]):
                row = idx * move_vector[x] + tile[x]
                col = idx * move_vector[y] + tile[y]
                temp.append(self._board[row][col]) 
            
            # merge each row/column in input direction
            merged = self.merge(temp)
            
            for idx in range(0, self.SPAN[direction]):
                row = idx * move_vector[x] + tile[x]
                col = idx * move_vector[y] + tile[y]
                if self._board[row][col] != merged[idx]:
                    tile_has_changed = True
                self._board[row][col] = merged[idx]
                if self._board[row][col] == 2048:
                    game_won = True
        
        if game_won == True:
            print "You win!!"
            self.reset()
        elif tile_has_changed == True:
            self.new_tile()
        else:
            if self.new_tile() == False:
                print "Sorry, you lose."
                print "Starting new game..."
                self.reset()
        
    def new_tile(self):
        '''
        Create a new tile in a randomly selected empty
        square.  The tile should be val 2 90% of the time and
        val 4 10% of the time.
        '''
        zero_points = []
        x = 0
        y = 1
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self._board[row][col] == 0:
                    zero_points.append((row, col))

        if len(zero_points) == 0:
            return False
        # generate random point for empty location on board
        new_tile_index = random.randrange(0, len(zero_points))
        new_tile = zero_points[new_tile_index]

        if random.randrange(0,10) >= 1:
            self._board[new_tile[x]][new_tile[y]] = 2
        else:
            self._board[new_tile[x]][new_tile[y]] = 4     

    def set_tile(self, row, col, value):
        '''
        Set the tile at position row, col to have the given value.
        '''
        self._board[row][col] = value

    def get_tile(self, row, col):
        '''
        Return the value of the tile at position row, col.
        '''
        return self._board[row][col]

main()
