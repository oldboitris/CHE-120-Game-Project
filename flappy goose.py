import pygame, random, time
from pygame.locals import * 

#VARIABLES
SCREEN_WIDTH = 400 
SCREEN_HEIGHT = 600 
SPEED = 20 
GRAVITY = 2.5 
GAME_SPEED = 15 

GROUND_WIDTH = 2 * SCREEN_WIDTH 
GROUND_HEIGHT= 100 

PIPE_WIDTH = 80 
PIPE_HEIGHT = 500

# A string list of top-to-bottom columns of pipes (indices 0 to 4)
COLUMN_SPRITES = [
    'assets/sprites/yellow-column.png',  # 0: Top
    'assets/sprites/orange-column.png',  # 1
    'assets/sprites/green-column.png',   # 2 These strings can be indexed
    'assets/sprites/blue-column.png',    # 3
    'assets/sprites/purple-column.png',  # 4: Bottom 
]
# Total number of colored sections in one full column, the variable NUM_SECTIONS equals 5.
NUM_SECTIONS = len(COLUMN_SPRITES) #

#removing PIPE_GAP since no more gap. 
wing = 'assets/audio/wing.wav' 
hit = 'assets/audio/hit.wav' 

pygame.mixer.init() 


class Bird(pygame.sprite.Sprite): 

    def __init__(self): # this makes the bird self spawn, we want to keep this
        pygame.sprite.Sprite.__init__(self) 

        sheet = pygame.image.load('assets/sprites/texture.png').convert_alpha() #this loads the spritesheet file
        
       goose_coords_colours = {
           "purple": (0, 0, 229, 307), #(x, y, width, height)
           "blue": (0, 307, 223, 307), 
           "yellow": (0, 614, 223, 307),
           "green": (0, 921, 221, 307),
           "orange": (0, 1228, 221, 307)
       }
        # set a target size to make them fit the flappy bird pipes
        target_size = (35, 48)

        #now we have everything set up to define our geese, so we make a dictionary to slice and resize the sprites
        #
        self.sprites = {
            colour: pygame.transform.scale(sheet.subsurface(coords), #This first part takes coords, crops out the excess and shrinks it down to the target size
            for colour, coords in goose_coords_colours.items() #this part is a loop that grabs each item (colour) and repeats the value transformation for each sprite
        }
        
        self.speed = SPEED

        #pick a random colour upon starting up the game by turning each item from the self.sprites into a list, then picks one name randomly
        self.colour = random.choice(list(self.sprites.keys())) 
        self.image = self.sprites[self.colour] #then this part takes that random choice to load up the corresponding image
        self.mask = pygame.mask.from_surface(self.image) 

        self.rect = self.image.get_rect() #This calls on my sprite to spawn a hitbox at the start of the game
        self.rect[0] = SCREEN_WIDTH / 6 #this places my sprite at the left of the screen, giving time to see the pipes ahead
        self.rect[1] = SCREEN_HEIGHT / 2 #This places my sprite in the middle of the screen vertically, assuring that its in a playable position.

    def change_colour(self):
        other_colours = [c for c in self.sprites.keys() if c != self.colour] #These two lines pick a new colour that isn't the previous one
        self.colour = random.choice(other_colours)
        
        self.image = self.sprites[self.colour]
        self.mask = pygame.mask.from_surface(self.image) #this swaps the images and refreshes the hitbox
    
    def update(self): #from here we deleted the cycling through wing flapping animation as our goose doesnt do that, and we just kept gravity and the upwards movement the same
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed 

    def bump(self): #This section makes our goose jump up when the spacebar is pressed, we want to keep this function exactly as is 
        self.speed = -SPEED 

    def begin(self): 
        pass #I put pass here because I dont need this function anymore but also don't want the game to crash if i forget to change the line where it is called upon 


class Pipe(pygame.sprite.Sprite): 

    def __init__(self, xpos, ypos, section_height, chosen_color): #init accepts 5 names, xpos ypos used to position pipe columns. 
        pygame.sprite.Sprite.__init__(self) #code treats pipe (self) as a Sprite. 
        
        #chosen_color is color of column, which is assigned to self using the method color_index, basically assigning color for collision comparison. 
        self.color_index = chosen_color

        # Step 1: Get the file path string from the list using the color number
        image_path = COLUMN_SPRITES[chosen_color]

        # Step 2: Load the image from the assets folder, use convert_alpha() to make transparent parts transparent and blend in. 
        raw_image = pygame.image.load(image_path).convert_alpha()
        
        # Step 3: Resize the image to match the pipe width and this section's height. 
        self.image = pygame.transform.scale(raw_image, (PIPE_WIDTH, section_height))

        # Step 4: Set up the position of rect and place it at (xpos, ypos)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = ypos
        self.passed = False #this will be used in the colour change of the bird as it passes the pipe

        # Step 5: Create the collision mask from the resized image
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Move this column piece to the left at GAME_SPEED
        self.rect[0] -= GAME_SPEED

    
        
class Ground(pygame.sprite.Sprite): 
    
    def __init__(self, xpos): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT)) 
        self.mask = pygame.mask.from_surface(self.image) 

        self.rect = self.image.get_rect() 
        self.rect[0] = xpos 
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT 
    def update(self): 
        self.rect[0] -= GAME_SPEED 


def is_off_screen(sprite): 
    return sprite.rect[0] < -(sprite.rect[2]) 

def get_random_pipes(xpos): 
    size = random.randint(100, 300) 
    pipe = Pipe(False, xpos, size) 
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP) 
    return pipe, pipe_inverted 


pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption('Flappy Bird')  

BACKGROUND = pygame.image.load('assets/sprites/background-day.png') 
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha() 

bird_group = pygame.sprite.Group() 
bird = Bird() 
bird_group.add(bird) 
ground_group = pygame.sprite.Group() 

for i in range (2): 
    ground = Ground(GROUND_WIDTH * i) 
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])



clock = pygame.time.Clock()

begin = True

while begin:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False

    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    bird.begin()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()


while True:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        
    for pipe in pipe_group:
        if not pipe.passed and pipe.rect.right < bird.rect.left: #this checks if the pipe.passed function in the pipe class still reads false
            for p in pipe group:
            if p.rect.x == pipe.rect.x: #this loop makes sure that the passed switch is only flipped once, as the bird passes all pipe parts at the same time (since their x position is equal)
                p.passed = True #this states that if we pass the x position of the pipe that we have passed the pipe
            bird.change_colour() #this calls for the bird to change colour since we've passed the pipe

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        time.sleep(1)
        break

