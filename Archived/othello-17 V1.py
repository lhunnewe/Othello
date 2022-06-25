import pygame
import random

class Othello:
    """
    Simple interactive Othello game implemented with PyGame.
    Throughout the code, col = row = 0 means the lower-left corner.
    """
    def __init__(self, discs=[[3, 3, 1], [3, 4, 2], [4, 3, 2], [4, 4, 1]],offset=10, tile_size=80, line_width=4, line_color=(0,0,0), background_color=(255,255,255), disc_radius=30, disc_color_1=(0,0,255), disc_color_2=(255,165,0), A=[], active_player=1, legal_moves=[], players=['human', 'computer']):
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
        self.legal_moves = legal_moves
        self.players = players [:]
        self.strategy = [self.strategy0, self.strategy0]
        self.zone_corner = [[0, 0], [7, 0], [0, 7], [7, 7]]
        self.zone_red = [[1, 0], [0, 1], [1, 1], [6, 0], [6, 1], [7, 1], [0, 6], [1, 6], [1, 7], [6, 6], [6, 7], [7, 6]]
        self.zone_green = [[2, 0], [2, 2], [0, 2], [5, 0], [5, 2], [7, 2], [0, 5], [2, 5], [2, 7], [5, 7], [5, 5], [7, 5]]
        self.zone_side = [[2, 0], [3, 0], [4, 0], [5, 0], [0, 2], [0, 3], [0, 4], [0, 5], [2, 7], [3, 7], [4, 7], [5, 7], [7, 2], [7, 3], [7, 4], [7, 5]]
        self.zone_center = []

        #  A to be a list of eight lists of length eight, and set all its 64 values to zero. The value 0 represents an empty board square with no disc in it. Later, the value 1 will represent a board square with a disc in it. 
        for i in range(0,8):
            self.A.append([0,0,0,0,0,0,0,0])
        for item in self.discs:
            col, row, player_id = item
            self.set_value(col, row, player_id)

        #  list of the center 4X4 central area.
        for x in range(2,6):
            for y in range(2,6):
                self.zone_center.append([x,y])
        
        self.get_legal_moves()  #to populate the list with all legal moves of the active player.

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
                    mouse_x, mouse_y = event.pos
                    col, row = self.get_board_pos(mouse_x, mouse_y)
                    self.highlight_legal_move(col, row)
                # Mouse button was released over the PyGame window:
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    if self.player_human():
                        mouse_x, mouse_y = event.pos
                        #returns the col, row of click location, rounds numbers tha are off screen to 0 or 7. 
                        col, row = self.get_board_pos(mouse_x, mouse_y)
                    else:
                        col, row = self.computer_move()
                        #print(col, row)
                        
                    if self.move_legal(col, row):
                        self.check_board_pos(col, row, True)
                        self.set_value(col, row, p=self.active_player)
                        self.draw_board()
                        self.switch_active_player()
                        self.get_legal_moves()
                        if len(self.legal_moves) == 0:
                            print('Player', self.active_player, 'cannot move.')
                            self.switch_active_player()
                            self.get_legal_moves()
                            if len(self.legal_moves) == 0:
                                pygame.display.update()
                                print('Game ended!')
                                p1, p2 = self.count()
                                if p1 > p2:
                                    print("Player 1 wins " + str(p1) + " to " + str(p2))
                                elif p2 > p1:
                                    print("Player 2 wins " + str(p2) + " to " + str(p1))
                                elif p1 == p2:
                                    print("Tie! Both players have", p1)
                                a = input("Press ENTER to exit the game.")
                                finished = True

                    else:
                        self.invalid_move_alert(col, row)
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
        p = self.A[7-row][col]
        #print('get_value: ',self.A[7-row][col])
        return p
    def set_value(self, col, row, p=-1):
        """
        Note: bottom row on board is row 7 in A, top row on board is row 0 in A.
        Sets the value of self.A[7-row][col] to p (player id).
        Only this method should be used to write values to the array A.
        """
        self.A[7-row][col] = p if p != -1 else self.active_player

        #print("Value at", col, row, "changed to", p)
    def draw_disc(self, col, row, color=None):
        """will draw a circle of radius self.disc_radius and given color at the center of the square (col, row) on the board"""
        xc = round(self.offset + (col+0.5)*self.tile_size)
        yc = round(self.offset + (7-row+0.5)*self.tile_size)
        #self.draw.circle(xc, yc)
        if color == None:
            color = self.active_player
        pygame.draw.circle(self.screen, color, (xc, yc), self.disc_radius)
    def get_board_pos(self, mouse_x, mouse_y):
        """for mouse position (mouse_x, mouse_y) returns the (col, row) position on the game square."""
        col = int((mouse_x - self.offset) / self.tile_size)
        row = 7 - int((mouse_y - self.offset) / self.tile_size)
        if col < 0:
            #print('column corrected to 0')
            col = 0
        if row < 0:
            #print('row corrected to 0')
            row = 0
        if col > 7:
            #print('column corrected to 7')
            col = 7
        if row > 7:
            #print('row corrected to 7')
            row = 7
        return col, row
    def valid_pos(self, col, row):
        """returns True if the position (col, row) is a valid board position and False otherwise"""
        #return True if col in range(0,7) or row in range(0,7) else False
        return col >= 0 and col <= 7 and row >= 0 and row <= 7
    def check_direction(self, col, row, dir_x, dir_y, change_values=False):
        """to count all opponents discs in positions in all 8 direecections, … but only if such a sequence ends with a disc of the active player"""
        opponent = 2 if self.active_player == 1 else 1
        captured = 0
        c = col
        r = row
        c += dir_x
        r += dir_y
        #print('valid pos: ',self.valid_pos(c,r),'get_value: ', self.get_value(c,r))

        while self.valid_pos(c,r) and self.get_value(c,r) == opponent:
            captured += 1
            c += dir_x
            r += dir_y
        #  Check if position is outside the board
        if not self.valid_pos(c,r):
            return 0       
        if self.get_value(c,r) == 0:
            return 0
        #  If none of these two last conditions are satisfied, it means that there is an active player’s disc at the end of the sequence, hence return the value of captured
        if change_values:
            #use the method set_value() to change the board values of all captured opponent’s squares to the active player’s id
            c = col
            r = row
            for i in range(captured):
                c += dir_x
                r += dir_y
                self.set_value(c, r, p=self.active_player)
        return captured
    def check_board_pos(self, col, row, change_values):
        """
        will calculate how many opponent discs 
        the move of active player to position (col, row) 
        would capture.
        """
        # If there already is a disc, return 0:
        if self.get_value(col, row) != 0:
            return 0
        # Number of captured opponent's discs:
        captured = 0
        for dir_x in [-1, 0, 1]:
            for dir_y in [-1, 0, 1]:
                captured += self.check_direction(col, row, dir_x, dir_y, change_values)
        return captured   
    def get_legal_moves(self):
        """
        This method will empty the list self.legal_moves, 
        and go through all 64 positions (col, row) on the game board. 
        For each position it will calculate the number captured 
        of the opponent's discs which would be captured. 
        Whenever captured is nonzero, the triplet [col, row, captured] 
        will be added to the list legal_moves.
        """
        self.legal_moves = []
        for col in range(0,8):
            for row in range(0,8):
                captured = self.check_board_pos(col, row, False)
                if captured > 0:
                    l_moves = [col, row, captured]
                    self.legal_moves.append(l_moves)
        
        print("Player", self.active_player, "legal moves:", self.legal_moves)
    def move_legal(self, col, row):
        """
        will return True 
        if the position (col, row) is present in legal_moves, 
        and False otherwise
        """
        for L in self.legal_moves:
            if col == L[0] and row == L[1]:
                return True
        #print('Player', self.active_player, 'illegal move. try again')
        return False

    def switch_active_player(self):
        if self.active_player == 1:
            self.active_player = 2
            #print('Turn Orange: Player ', self.active_player, self.players[1])
        else:
            self.active_player = 1
            #print('Turn Blue: Player ', self.active_player, self.players[0])
    def highlight_legal_move(self, mouse_x, mouse_y):
        """To highlight legal moves when the player hovers over the location"""
        self.draw_board()
        if self.move_legal(mouse_x, mouse_y):
            self.draw_disc(mouse_x, mouse_y, color=(0, 255,0))
    def invalid_move_alert(self, col, row):
        """
        to highlight invalid moves of the active player. 
        We are not going to add discs to the board yet, 
        but when the active player clicks into a square 
        which is not eligible, 
        we will briefly flash a red circle.
        """
        self.draw_disc(col, row, color=(255,0,0))
        pygame.display.update()
        pygame.time.delay(100)
        self.draw_board()
    def count(self):
        """To count the end game points"""
        p1 = 0
        p2 = 0
        for col in range(8):
            for row in range(8):
                p  = self.get_value(col, row)
                #if p != 0:
                #    print (col, row, p)
                if p == 1:
                    p1 += 1
                if p == 2:
                    p2 += 1
        return p1, p2
    def player_human(self):
        """returns True if the active player is human and False if Computer"""
        
        #print(self.players)

        if self.active_player == 1:
            if self.players[0] == 'human':
                return True
            else:
                return False
        elif self.active_player == 2:
            if self.players[1] == 'human':
                return True
            else:
                return False
        
    def computer_move(self):
        """
        From the list of legal moves, select those moves which capture the fewest opponents discs. 
        Recall that the list legal_moves contains triplets of the form [col, row, c] 
        where the third value is the number of opponent's discs which would be captured by the move 
        to position (col, row). 
        If there are more moves with the lowest value of c, choose one of them randomly. 
        There are many possible ways to do this. 
        Probably the easiest one is to use the function random.choice()
        """
        #pass
        return self.strategy[self.active_player - 1]()
        """
        L = []
        for i in range(len(self.legal_moves)):
            discs = self.legal_moves[i][2]
            L.append(discs)
        minimum_discs = min(L)
        #print('Min: ',minimum_discs)
        choices = []
        for i in range(len(self.legal_moves)):
            if self.legal_moves[i][2] == minimum_discs:
                choices.append(self.legal_moves[i])
        choice = random.choice(choices)
        #print('computer chooses: ',choice)
        col = choice[0]
        row = choice[1]
        return col, row
        """
    def strategy0(self):
        L = []
        for i in range(len(self.legal_moves)):
            discs = self.legal_moves[i][2]
            L.append(discs)
        minimum_discs = min(L)
        #print('Min: ',minimum_discs)
        choices = []
        for i in range(len(self.legal_moves)):
            if self.legal_moves[i][2] == minimum_discs:
                choices.append(self.legal_moves[i])
        #print('choices: ',choices)
        choice = random.choice(choices)
        #print('choice: ', choice)
        print('Active player', self.active_player, 'using strategy0().') 
        return choice[0], choice[1]
    def strategy1(self):
        #Take a corner if possible
        for move in self.legal_moves:
            if [move[0], move[1]] in self.zone_corner:
                #print(move, 'Zone found in corner.Taking the corner')
                return move[0], move[1]
        #If a corner move was not possible, try to avoid squares which are adjacent to corners.
        moves = []
        for move in self.legal_moves:
            if [move[0],move[1]] not in self.zone_red:
                moves.append(move)
        if len(moves) == 0:
            return self.strategy0()  #call the disc-minimizing move
        else:
            # If the list moves did not remain empty (great!) then replace the contents of legal_moves with it, again call strategy0() to select from legal_moves the disc-minimizing move, and return the result.
            self.legal_moves = []
            self.legal_moves = moves
            return self.strategy0()  #call the disc-minimizing move

        #print('Active player', self.active_player, 'using strategy1(). Temporarily the same as strategy0().') 
    def strategy2(self):
        #Take a corner if possible
        for move in self.legal_moves:
            if [move[0], move[1]] in self.zone_corner:
                #print(move, 'Zone found in corner.Taking the corner')
                print('Active player', self.active_player, 'using strategy2a().', move)
                return move[0], move[1]
        # try to place a disc in the 4X4 area
        for move in self.legal_moves:
            if [move[0],move[1]] in self.zone_center:
                print('Active player', self.active_player, 'using strategy2b().', move)
                return move[0], move[1]
        # try to place a move in the green zone
        for move in self.legal_moves:
            if [move[0],move[1]] in self.zone_green:
                print('Active player', self.active_player, 'using strategy2c().', move)
                return move[0], move[1]
        # try to place a move on the side
        for move in self.legal_moves:
            if [move[0],move[1]] in self.zone_side:
                print('Active player', self.active_player, 'using strategy2d().', move)
                return move[0], move[1]
        #If a corner move was not possible, try to avoid squares which are adjacent to corners.
        moves = []
        for move in self.legal_moves:
            if [move[0],move[1]] not in self.zone_red:
                moves.append(move)
        
        if len(moves) != 0:
            num_red_moves = len(self.legal_moves) - len(moves)
            print(num_red_moves,'red_zone move(s) removed, legal moves are: ', moves)
            self.legal_moves.clear()
        #print(self.legal_moves)
            for move in moves:
                self.legal_moves.append(move)
            return self.strategy0()
        else:
            print('red_zone forced to take: ', self.legal_moves)
            return self.strategy0()
    def set_player_strategy(self, player_id, name):
        """
        player_id will be either 1 or 2 (check user input) 
        and strategy name will be either 
        [beginner, intermediate, advanced] (again check user input). 
        The value self.strategy[0] corresponds to player_id == 1.
        """

        #player_id = input('Player id: [1 or 2]')
        #name = input('Select strategy: [beginner, intermediate, advanced]')

        if player_id == 1:
            if name == 'beginner':
                self.strategy[0] = self.strategy0
            elif name == 'intermediate':
                self.strategy[0] = self.strategy1
            elif name == 'advanced':
                self.strategy[0] = self.strategy2
        else:
            if name == 'beginner':
                self.strategy[1] = self.strategy0
            elif name == 'intermediate':
                self.strategy[1] = self.strategy1
            elif name == 'advanced':
                self.strategy[1] = self.strategy2
        

# Main program:
R = Othello(players=['computer', 'computer'])
R.set_player_strategy(1, 'beginner')
R.set_player_strategy(2, 'advanced')
R.start()