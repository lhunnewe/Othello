import pygame


class Othello:
    """
    Simple interactive Othello game implemented with PyGame.
    Throughout the code, col = row = 0 means the lower-left corner.
    """
    def __init__(self, offset=10, tile_size=80, line_width=4, line_color=(0,0,0), background_color=(255,255,255)):
        """Initializes the game"""
        # Import and initialize the PyGame library:
        pygame.init()
        # Set up the PyGame window:
        width = round(2*self.offset + 8*self.tile_size)
        height = round(2*self.offset + 8*self.tile_size)
        
        self.offset = offset
        self.tile_size = tile_size
        self.linewidth = line_width
        self.line_color = line_color
        self.background_color = background_color
        
        self.screen = pygame.display.set_mode((width, height))
        # Set window title:
        pygame.display.set_caption('Othello')
        # Manage how frequently the screen will update:
        self.clock = pygame.time.Clock()
        # Draw the board:
        self.draw_board()

    def draw_board(self):
        """Displays the grid"""
        # Fill the PyGame window with white color:
        color = (255, 255, 255)     # white
        self.screen.fill(color)
        # Draw the outer square of the board:
        color = (0, 0, 0)     # black
        lw = 4                # line width
        xstart = 10
        ystart = 10
        xend = 10
        yend = 650
        pygame.draw.line(self.screen, color, (xstart, ystart), (xend, yend), lw)
        xstart = 650
        ystart = 10
        xend = 650
        yend = 650
        pygame.draw.line(self.screen, color, (xstart, ystart), (xend, yend), lw)
        xstart = 10
        ystart = 10
        xend = 650
        yend = 10
        pygame.draw.line(self.screen, color, (xstart, ystart), (xend, yend), lw)
        xstart = 10
        ystart = 650
        xend = 650
        yend = 650
        pygame.draw.line(self.screen, color, (xstart, ystart), (xend, yend), lw)

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
                    pass
                # PyGame window was resized:
                if event.type == pygame.VIDEORESIZE:
                    pass
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
