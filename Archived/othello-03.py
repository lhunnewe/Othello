import pygame


class Othello:
    """
    Simple interactive Othello game implemented with PyGame.
    Throughout the code, col = row = 0 means the lower-left corner.
    """
    def __init__(self, offset=10, tile_size=80, line_width=4, line_color=(0,0,0), background_color=(255,255,255), disc_radius=30, disc_color=(0,0,255)):
        """Initializes the game"""
        
        # Custom Attributes
        self.offset = offset
        self.tile_size = tile_size
        self.linewidth = line_width
        self.line_color = line_color
        self.background_color = background_color
        self.disc_radius = disc_radius
        self.disc_color = disc_color


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
    def draw_circle(self,x,y):
        pygame.draw.circle(self.screen, self.disc_color, (x, y), self.disc_radius)
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
        #Calculate new width and height of the window 
        self.tile_size *= new_ratio
        width = 2*self.offset + 8*self.tile_size
        height = 2*self.offset + 8*self.tile_size
        #Update the PyGame window
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        #Use the method draw_board() to redraw the board.
        self.draw_board()
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
                    self.draw_circle(mouse_x, mouse_y)
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

# Main program:
R = Othello()
R.start()
