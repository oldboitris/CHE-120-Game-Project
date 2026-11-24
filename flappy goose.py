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

PIPE_GAP = 150
#sets dimensions for the pipes (TC)
wing = 'assets/audio/wing.wav' 
hit = 'assets/audio/hit.wav' 

pygame.mixer.init() 

#we want to define a new set of birds, where there is a sprite corresponding to each colour. we will do this by importing the sprite from the png, and take the specific coordinates of each sprite 
#then we will randomly generate a colour each time the game starts and each time the bird passes the pipe
#we want to make sure our new geese sprites are the right size for the game, so we adjust them to a target size
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

        self.rect = self.image.get_rect() 
        self.rect[0] = SCREEN_WIDTH / 6 
        self.rect[1] = SCREEN_HEIGHT / 2 

    def update(self): 
        self.current_image = (self.current_image + 1) % 3  
        self.image = self.images[self.current_image] 
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed 

    def bump(self):
        self.speed = -SPEED 

    def begin(self): 
        self.current_image = (self.current_image + 1) % 3 
        self.image = self.images[self.current_image]
"""In sum, ln 26 defines Bird as a Pygame sprite. 
ln 28 _init_ sets up a new bird, it loads the three flap images (upflap, midflap, downflap), sets the starting speeds (jump) and images, 
and sets up bird's collision shape and position (rectangular hitbox).
ln 45 update(self) cycles through the images we loaded in ln 28, adds gravity to bird's speed, and moves bird vertically.
ln 53 bump(self) gives flap a negative (up) speed when player clicks Space or Up. (ln 28 sets speed, ln 53 assigns jump speed to click) 
ln 56 begin(self) cycles bird's pictures on start screen. But bird not moving, just start screen animation. (TC)
"""

class Pipe(pygame.sprite.Sprite): 

    def __init__(self, inverted, xpos, ysize): 
        pygame.sprite.Sprite.__init__(self) 

        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))


        self.rect = self.image.get_rect() 
        self.rect[0] = xpos 

        if inverted: 
            self.image = pygame.transform.flip(self.image, False, True) 
            self.rect[1] = - (self.rect[3] - ysize) 
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize 


        self.mask = pygame.mask.from_surface(self.image) 


    def update(self): 
        self.rect[0] -= GAME_SPEED
"""
This class defines Pipe as a Pygame sprite. It can be positioned as a top (inverted) or bottom pipe,
and the pipe moves left during the game, remember the bird's speed is only defined vertically (gravity and jump). 
"""
        

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
"""
Ground is created and scaled, then it is given a collision box, and set in position. 
When ground is updated it starts moving right to left at 15 pixels, the code will later remove the ground that is off-screen and generate new ones on the right.
"""

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

