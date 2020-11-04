"""
 A snake game developed in Python 3 using the pygame library.
 
"""
import pygame
import random






class GV (object):
    """
    This class is an interface containing the global variables.

    """
    black = (0 , 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    window_x = 800
    window_y = 600

    width = 15
    height = 15
    margin = 3

    initlength = 10

    clocktick = 5




class Food (pygame.sprite.Sprite):
    """
    Class to represent the food.

    """
    def __init__ (self, x, y):
        """
        Initialize
        """
        super().__init__()

        # Set height, width
        self.image = pygame.Surface ((GV.width//2, GV.height//2))   #pygame.transform.scale(pygame.image.load ("mouse.png"), (40, 40))
        self.image.fill (GV.red)
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #print(f"New food in position ({x}, {y})")




 

class Segment(pygame.sprite.Sprite):
    """
    Class to represent one segment of the snake.
	
    """
    def __init__(self, x, y):
        """
        Initialize.

        """
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([GV.width, GV.height])
        self.image.fill(GV.white)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    
    




def run ():
    # Set initial speed and food
    direction = "RIGHT"
    x_change = GV.width + GV.margin
    y_change = 0
    food = Food (random.randrange(0, GV.window_x - GV.width//2, GV.width//2), random.randrange(0, GV.window_y - GV.height//2, GV.height//2))

    pygame.init()
    screen = pygame.display.set_mode((GV.window_x, GV.window_y))
    pygame.display.set_caption('Snake')
    allspriteslist = pygame.sprite.Group()

    # Initialize the snake
    snake_segments = [Segment (250 - (GV.width + GV.margin)*i, 30 - GV.margin) for i in range (GV.initlength)]
    allspriteslist.add (food)
    for s in snake_segments:
        allspriteslist.add (s)

    clock = pygame.time.Clock()


    done = False
    while done is False:
     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
     
            # Set the speed based on the key pressed
            # We want the speed to be enough that we move a full segment, plus the margin.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                    x_change = (GV.width + GV.margin) * (-1)
                    y_change = 0
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                    x_change = GV.width + GV.margin
                    y_change = 0
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                    x_change = 0
                    y_change = (GV.height + GV.margin) * (-1)
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                    x_change = 0
                    y_change = GV.height + GV.margin

        # Move the snake
        moved_segment = snake_segments.pop()
        moved_segment.rect.x = snake_segments[0].rect.x + x_change
        moved_segment.rect.y = snake_segments[0].rect.y + y_change
        snake_segments.insert(0, moved_segment)

        # Appear on the other side of the window
        if moved_segment.rect.x > GV.window_x:
            moved_segment.rect.x = 0
        elif moved_segment.rect.x < 0:
            moved_segment.rect.x = GV.window_x - GV.width

        # Appear on the other side of the window
        if moved_segment.rect.y > GV.window_y:
            moved_segment.rect.y = 0
        elif moved_segment.rect.y < 0:
            moved_segment.rect.y = GV.window_y - GV.height

        # If the food is eaten, the snake get longer
        if moved_segment.rect.x - GV.margin <= food.rect.x + GV.width//2 and moved_segment.rect.x + GV.width + GV.margin >= food.rect.x and moved_segment.rect.y - GV.margin <= food.rect.y + GV.height and moved_segment.rect.y + GV.height + GV.margin >= food.rect.y:
            new_segment = Segment (snake_segments[-1].rect.x - (snake_segments[-2].rect.x - snake_segments[-1].rect.x), snake_segments[-1].rect.y - (snake_segments[-2].rect.y - snake_segments[-1].rect.y))
            snake_segments.append (new_segment)
            allspriteslist.add (new_segment)
            food.rect.x = random.randrange(0, GV.window_x - GV.width//2, GV.width//2)
            food.rect.y = random.randrange(0, GV.window_y - GV.height//2, GV.height//2)


        # Check if the snake bit itself
        head = snake_segments[0]
        for i, segm in enumerate(snake_segments):
            if i != 0:
                if segm.rect.x <= head.rect.x <= segm.rect.x + GV.width and segm.rect.y <= head.rect.y + GV.height <= segm.rect.y + GV.height:
                    done = True
                    break
     
        # Clear screen
        screen.fill(GV.black)
     
        allspriteslist.draw(screen)
     
        # Flip screen
        pygame.display.flip()
     
        # Pause
        clock.tick(GV.clocktick)

    pygame.quit()





if __name__ == "__main__":
    run ()