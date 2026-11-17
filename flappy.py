#Katherine Elvidge(KE) Kiana Alenabi Amlashi(KA) Mohammed Ibrahim Rashaed(MR) Tristan Yong Keng Chay(TC)
import pygame, random, time #importing python packages, pygame, random, time which gives us functions to work with. (TC)
from pygame.locals import * #further imports constant variables from pygame, like QUIT (to close game), KEYDOWN, K_SPACE, K_UP. (TC)

#VARIABLES
SCREEN_WIDTH = 400 #setting screen width to 400 pixels (KE) (KA) (MR) (TC)
SCREEN_HEIGHT = 600 #setting screen height to 400 pixels (KE) (KA) (MR) (TC)
SPEED = 20 #the speed of the bird's jump in pixels per frame  (upwards), only when the user taps (KE) (KA) (MR) (TC)
GRAVITY = 2.5 #the acceleration of falling, every second the speed downwards increases by 2.5 pixels per frame (KE) (KA) (MR) (TC)
GAME_SPEED = 15 #the ground, pipes, map moves from right to left at 15 pixels per frame (KE) (KA) (MR) (TC)

GROUND_WIDTH = 2 * SCREEN_WIDTH #ground is double screen width so that animations flow seamlessly rather than having random gaps. (TC)
GROUND_HEIGHT= 100 #sets the ground to be placed at 100 pixels, since the ground in game needs to be on-screen. (TC)

PIPE_WIDTH = 80 
PIPE_HEIGHT = 500

PIPE_GAP = 150
#sets dimensions for the pipes (TC)
wing = 'assets/audio/wing.wav' 
hit = 'assets/audio/hit.wav' 
#createa and initializes variables wing and hit, will play these audio files in folders assets -> audio (we gotta have these folders too) (TC)
pygame.mixer.init() #initializes Pygame's audio mixer to play audio files. (TC)

#a sprite is a 2D graphical object that represents a moving or interactive element of a game - bird, coins, pipes. (TC)
class Bird(pygame.sprite.Sprite): #loads preexisting sprite graphic from pygame to use as the bird
#the code above defines Bird as a Pygame sprite. Now Bird has sprite behavior: it can be grouped, drawn, updated. (TC)
    def __init__(self): #defines a new method that sets up a new bird (start a new game), this function will give it a starting speed, position. (TC)
        pygame.sprite.Sprite.__init__(self) #initializes Bird so that Pygame gives it attributes of a sprite. (TC)
# self is used to say that updates and any new addition affects the bird. (TC)
        self.images =  [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(), #the .convert_alpha() converts each image to a format suitable for displaying with transparency rather than a solid black background. (TC)
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()] #these three images are loaded and attributed to self (Bird) so that it can actually flap in game. (TC)
#loads graphics for the wing flap of the bird
        self.speed = SPEED #sets the bird's vertical speed, from every jump, in pixels per frame (TC)

        self.current_image = 0 #the starting image of Bird is image 0, or up_flap.(TC)
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha() #open the image of bird up-flap, convert alpha makes adjusts transparency to fit background (pretty graphics). (TC) 
        self.mask = pygame.mask.from_surface(self.image) #makes a pixel-based collision image, so that it follows the shape of bird rather than a rectangular hitbox. (TC)

        self.rect = self.image.get_rect() #creates a rectangular size around the bird, and the bird's position. (TC)
        self.rect[0] = SCREEN_WIDTH / 6 #places the bird at 1/6 of screen width. (TC)
        self.rect[1] = SCREEN_HEIGHT / 2 #places bird at 1/2 of screen height. (TC)

    def update(self): #_init_ above gives Bird starting attributes, this defines a new action for Bird. (TC)
        self.current_image = (self.current_image + 1) % 3 #every tap the bird will have different animations, this line cycles to the next image (+1), %3 means remain between 0 and 2, so we always cycle between up-, mid-, down-flap images. (TC)
        self.image = self.images[self.current_image] #display the bird's image on screen to whichever stage of flight we're in, defined by indexing in the line above. (TC)
        self.speed += GRAVITY #adds gravity to bird's vertical speed, in the game, down is positive, line 9 defined acc due to g as 2.5 pixels/frame. (TC)

        #UPDATE HEIGHT
        self.rect[1] += self.speed #changes bird's vertical position by its current speed (positive is down so Bird is falling due to gravity). (TC)

    def bump(self): #defines what happens when bird flaps. (TC)
        self.speed = -SPEED #gives bird a negative vertical speed (negative is up) so this is bird's jump when player taps. (TC)

    def begin(self): #begin defines the bird's starting animation. (TC)
        self.current_image = (self.current_image + 1) % 3 #like ln 46, cycles display of bird through 3 images. (TC)
        self.image = self.images[self.current_image] #displays the newly selected image. (TC)
"""In sum, ln 26 defines Bird as a Pygame sprite. 
ln 28 _init_ sets up a new bird, it loads the three flap images (upflap, midflap, downflap), sets the starting speeds (jump) and images, 
and sets up bird's collision shape and position (rectangular hitbox).
ln 45 update(self) cycles through the images we loaded in ln 28, adds gravity to bird's speed, and moves bird vertically.
ln 53 bump(self) gives flap a negative (up) speed when player clicks Space or Up. (ln 28 sets speed, ln 53 assigns jump speed to click) 
ln 56 begin(self) cycles bird's pictures on start screen. But bird not moving, just start screen animation. (TC)
"""

class Pipe(pygame.sprite.Sprite): #Pipe is defined as a Pygame sprite again, we'll define Pipe behavior here. (TC)

    def __init__(self, inverted, xpos, ysize): #a method is defined using these 4 pieces of info. (TC)
        #self means pipe being created. inverted takes True/False for whether pipe is inverted (since we need 2 pipes with opening)
        #xpos is pipe's horizontal position on screen. ysize is pipe's position vertically. (TC)
        pygame.sprite.Sprite.__init__(self) #the pipe is a sprite. (TC)

        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha() #loads image pipe-green.png stored in assets/sprites. convert_alpha just beautifies with transparency. (TC)
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT)) #resizes image of pipe variables initialized in ln 6 and 7. (TC)


        self.rect = self.image.get_rect() #creatses rectangle around image, rectangle's x and y values refer to top left edge. 
        self.rect[0] = xpos #the rectangle's horizontal position is set to xpos (3rd argument) (TC)

        if inverted: #this conditional changes how pipe looks if inverted, we will flip it upside-down. (TC)
            self.image = pygame.transform.flip(self.image, False, True) #flip(bird'simage, don't flip left to right, True flip top to bottom). (TC)
            self.rect[1] = - (self.rect[3] - ysize) #self.rect[3] #self.rect[3] is 500 pixels (PIPE_HEIGHT in ln 16), ysize gives position (negative puts pipe above visible screen to make gap). (TC)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize #else (if pipe is upright), then some of pipe is below visible screen. (TC)


        self.mask = pygame.mask.from_surface(self.image) #creates pixel-based collision box around pipe image. Bird's mask collides with pipe's mask. (TC)


    def update(self): #defines updates to pipe, pipe needs to move. (TC)
        self.rect[0] -= GAME_SPEED #moves pipe left by game_speed pixels each update. 
"""
This class defines Pipe as a Pygame sprite. It can be positioned as a top (inverted) or bottom pipe,
and the pipe moves left during the game, remember the bird's speed is only defined vertically (gravity and jump). 
"""
        

class Ground(pygame.sprite.Sprite): #The ground is created as a sprite, since it needs to interact with bird.
    
    def __init__(self, xpos): #initializing the ground and its starting position (ground will be moving)
        pygame.sprite.Sprite.__init__(self) # again, ground is a sprite
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha() #load the image base.png in folders: assets -> sprites, convert_alpha makes it transparent and fit in.
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT)) #scale the photo to fit the sizes (in pixels) 800 by 100, ln 6 & ln 7. The ground is double the width of screen so it scrolls smoothly.
        self.mask = pygame.mask.from_surface(self.image) #generates a mask (hitbox) around the ground so it can interact with bird.

        self.rect = self.image.get_rect() #generates a rectangle around ground
        self.rect[0] = xpos #left edge of ground's rectangle put set to xpos.
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT #screen height = 600, ground height = 100, ground occupies the bottom rows of pixels 500-599. 
    def update(self): #when ground is updated
        self.rect[0] -= GAME_SPEED #move ground left by 15 pixels, the code will remove ground off-screen and generate another one so that the map scrolls. 
"""
Ground is created and scaled, then it is given a collision box, and set in position. 
When ground is updated it starts moving right to left at 15 pixels, the code will later remove the ground that is off-screen and generate new ones on the right.
"""

def is_off_screen(sprite): #creates function, this checks if a sprite moved completely off the left side of the screen.
    return sprite.rect[0] < -(sprite.rect[2]) #sprite.rect[0] is the sprite’s left-edge x-coordinate.
    #sprite.rect[2] is the rectangle’s width.
    #this function returns a Boolean, this is False only until the left edge is completely past the screen, then this returns True.

def get_random_pipes(xpos): #function that creates pair of pipes at horizontal position xpos.
    size = random.randint(100, 300) #uses randomizer to pick random number between 100-300 (for position), stores int in variable size.
    pipe = Pipe(False, xpos, size) #creates bottom pipe, False means don't invert, xpos for horizontal position, size for vertical position.
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP) #creates top pipe at same horizontal position, True means invert. Calculation leaves a gap (for the bird to fly through). 
    return pipe, pipe_inverted #returns both the bottom and top pipe. 


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

