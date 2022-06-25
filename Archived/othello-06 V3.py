import pygame

class Othello:
    """
    Simple interactive Othello game implemented with PyGame.
    Throughout the code, col = row = 0 means the lower-left corner.
    """
    def __init__(self, discs=[[3, 3, 1], [3, 4, 2], [4, 3, 2], [4, 4, 1]],offset=10, tile_size=80, line_width=4, line_color=(0,0,0), background_color=(255,255,255), disc_radius=30, disc_color_1=(0,0,255), disc_color_2=(255,165,0), A=[], active_player=1):
        """Initializes the game"""
        
        # Custom Attributes
        self.offset = offset
        self.discs = discs  #This is a list of triplets [col, row, player_id] which represents the initial configuration of discs on the board.
        self.tile_size = tile_size
        self.linewidth = line_width
        self.line_color = line_color
        self.background_color = background_color
        self.disc_radius = disc_radius
        self.disc_color_1 = disc_color_1
        self.disc_color_2 = disc_color_2
        self.A = A
        self.active_player = active_player

        #  A to be a list of eight lists of length eight, and set all its 64 values to zero. The value 0 represents an empty board square with no disc in it. Later, the value 1 will represent a board square with a disc in it. 
        for i in range(0,8):
            self.A.append([0,0,0,0,0,0,0,0])
        for item in self.discs:
            col, row, player_id = item
            self.set_value(col, row, player_id)

        # Import and initialize the PyGame library:
        pygame.init()
        # Set up the PyGame window:
        width = round(2*self.offset + 8*self.tile_size)
        height = round(2*self.offset + 8*self.tile_size)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        # Set window title:
        pygame.display.set_caption('Othello')
        # Manage how frequently the screen will update:
        self.clock = pygame.time.Clock()
        # Draw the board:
        self.draw_board()
    #def draw_circle(self,x,y):
    #    pygame.draw.circle(self.screen, self.disc_color, (x, y), self.disc_radius)
    def draw_board(self):
        """Displays the grid"""
        # Coordinates (0,0) is the upper left of the of the PyGame window
        # Fill the PyGame window with white color:
        self.screen.fill(self.background_color)
        # Draw the outer square of the board:
        
        index=0  #to iterate over tile_size
        for x in range(9):
            pygame.draw.line(self.screen, self.line_color, (round(self.offset+index), round(self.offset)), (round(self.offset + index), round(2*self.offset + 8*self.tile_size - self.offset)), self.linewidth)
            for y in range(9):
                pygame.draw.line(self.screen, self.line_color, (round(self.offset), round(self.offset+index)), (round(2*self.offset + 8*self.tile_size - self.offset), round(self.offset + index)), self.linewidth)
                #print(index, self.offset+index,round(2*self.offset + 8*self.tile_size))
            index+= self.tile_size
        
        #Upon resize, this redraws all the discs in list "A" to resize and repopulate the board.
        for col in range(8):
            for row in range(8):
                p = self.get_value(col, row)
                if p == 1:
                    self.draw_disc(col, row,color=self.disc_color_1)
                if p == 2:
                    self.draw_disc(col, row,color=self.disc_color_2)
    def start(self):
        """PyGame event loop"""
        # Event loop:
        finished = False
        while not finished:
            # Process any new PyGame events:
            for event in pygame.event.get():
                # Mouse moved over the PyGame window:
                if event.type == pygame.MOUSEMOTION:
                    pass
                # Mouse button was released over the PyGame window:
                if event.type == pygame.MOUSEBUTTONUP:
                    #pass
                    mouse_x, mouse_y = event.pos
                    #returns the col, row of click location, rounds numbers tha are off screen to 0 or 7. 
                    col, row = self.get_board_pos(mouse_x, mouse_y)
                    n = self.check_board_pos(col, row)
                    print("Pos:", col, row, "player:", self.active_player, "captured:", n)
                    #Draws the disk
                    if self.get_value(col, row) == 0:
                        if self.active_player == 1:
                            #self.set_value(col, row, 1)  #Updates list from 0 to player "1" or "2" to use the position
                            #self.draw_disc(col, row, self.disc_color_1)  #draws the new disc
                            self.active_player = 2  #change player
                        else: 
                            #self.set_value(col, row, 2)  #Updates list from 0 to player "1" or "2" to use the position
                            #self.draw_disc(col, row, self.disc_color_2)  #draws the new disc
                            self.active_player = 1  #change player

                # PyGame window was resized:
                if event.type == pygame.VIDEORESIZE:
                    #pass
                    self.resize(event.w, event.h)
                # User closed the window:
                if event.type == pygame.QUIT:
                    finished = True
                # Some key was pressed:
                if event.type == pygame.KEYDOWN:
                    # If the pressed key was ESC, exit:
                    if event.key == pygame.K_ESCAPE:
                        finished = True
            # Limit refresh rate to 20 frames per second:
            self.clock.tick(20)
            # Refresh the screen:
            pygame.display.update()
        # Terminate PyGame:
        pygame.quit()
    def resize(self, new_width, new_height):
        #calculate new_size as the minimum of new_width and new_height
        if new_width < new_height:  
            new_size = new_width
        else:
            new_size = new_height
        if new_size < 200:
            new_size = 200
        
        #Calculate the old_size of the window
        old_size = 2*self.offset + 8*self.tile_size
        #Calculate the ratio of the new_size and old_size
        new_ratio = new_size / old_size
        print(new_size, new_ratio) 
        #Use the ratio to update the values of self.offset and self.tile_size
        self.offset *= new_ratio
        self.disc_radius *= new_ratio
        #Calculate new width and height of the window 
        self.tile_size *= new_ratio
        width = 2*self.offset + 8*self.tile_size
        height = 2*self.offset + 8*self.tile_size
        #Update the PyGame window
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        #Use the method draw_board() to redraw the board.
        self.draw_board()
    def get_value(self, col, row):
        """Gets the values of list A"""
        #print('get_value: ',self.A[7-row][col])
        return self.A[7-row][col]
    def set_value(self, col, row, p):
        """
        Note: bottom row on board is row 7 in A, top row on board is row 0 in A.
        Sets the value of self.A[7-row][col] to p (player id).
        Only this method should be used to write values to the array A.
        """
        self.A[7-row][col] = p
        #print("Value at", col, row, "changed to", p)
    def draw_disc(self, col, row, color):
        """will draw a circle of radius self.disc_radius and given color at the center of the square (col, row) on the board"""
        xc = round(self.offset + (col+0.5)*self.tile_size)
        yc = round(self.offset + (7-row+0.5)*self.tile_size)
        #self.draw.circle(xc, yc)
        pygame.draw.circle(self.screen, color, (xc, yc), self.disc_radius)
    def get_board_pos(self, mouse_x, mouse_y):
        """for mouse position (mouse_x, mouse_y) returns the (col, row) position on the game square."""
        col = int((mouse_x - self.offset) / self.tile_size)
        row = 7 - int((mouse_y - self.offset) / self.tile_size)
        if col < 0:
            print('column corrected to 0')
            col = 0
        if row < 0:
            print('row corrected to 0')
            row = 0
        if col > 7:
            print('column corrected to 7')
            col = 7
        if row > 7:
            print('row corrected to 7')
            row = 7
        return col, row
    def valid_pos(self, col, row):
        """returns True if the position (col, row) is a valid board position and False otherwise"""
        return True if col in range(0,7) or row in range(0,7) else False
   
    def check_east(self, col, row):
        """to count all opponents discs in positions (col+1, row), (col+2, row), … but only if such a sequence ends with a disc of the active player"""
        opponent = 2 if self.active_player == 1 else 1
        captured = 0
        c = col
        r = row
        c += 1
        #print('valid pos: ',self.valid_pos(c,r),'get_value: ', self.get_value(c,r))

        while self.valid_pos(c,r) and self.get_value(c,r) == opponent:
            captured += 1
            c+=1
        #  Check if position is outside the board
        if not self.valid_pos(c,r):
            return 0       
        if self.get_value(c,r) == 0:
            return 0
        #  If none of these two last conditions are satisfied, it means that there is an active player’s disc at the end of the sequence, hence return the value of captured
        return captured
    def check_board_pos(self, col, row):
        """
        will calculate how many opponent discs 
        the move of active player to position (col, row) 
        would capture.
        """
        # If there already is a disc, return 0:
        if self.get_value(col, row) != 0:
            return 0
        # Number of captured opponent's discs:
        captured = self.check_east(col, row)
        return captured
    
    
    

# Main program:
R = Othello(discs=[[1, 4, 1], [2, 4, 1], [3, 4, 1], [4, 4, 1], [5, 4, 1], [6, 4, 1], [7, 4, 2]])
R.start()