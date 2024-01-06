
import pygame
import math
import copy
import random
import High_Scores
from random import sample
from Tilesets.DOTS import Dots
from Tilesets.PLAY import PLAY_AREA
from Tilesets.GHOSTS import GHOST_AREA
pygame.init()

WIDTH, HEIGHT = 672, 900
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PacMan")

#Colors
WHITE = 255,255,255
BLACK = 0,0,0

#Player is ready to play

#frames
FPS = 60
#clock for tracking time stpes
TIMER = 0
#entity velocity
VEL = 2
#this is not needed as far as i know, but code is a bit of spaghetti so I will leave it for now
VEL_BANDAID = 1
#player score
SCORE = 7810
#highest recorded score
HIGH_SCORE = High_Scores.get_highest_score()
#array for inputing scorers name
SCORER_NAME = [0,0,0]
#to select slot of array
SCORER_EDIT_COLUMN = 0
#let me know if the high score input has had any edits done
EDITED = False
#lets me know if the score was submitted
SUBMITTED = False
#alphabet for score input
ALHAPHABET = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"] 
#time location and point value of events like eating ghost or contact
EVENT_X = -200
EVENT_Y = -200
EVENT_TIME = 0
EVENT_VALUE = 0
#fonts for use
text_font = pygame.font.Font("Quinquefive-ALoRM.ttf", 15)
menu_font = pygame.font.Font("Quinquefive-ALoRM.ttf", 10)
event_font = pygame.font.Font("Quinquefive-ALoRM.ttf", 6)

#Sound files
pygame.mixer.init()
#music list
#eat fruit
eat_fruit = pygame.mixer.Sound("Sounds\eat_fruit.wav")
#eat ghost sound
eat_ghost = pygame.mixer.Sound("Sounds\eat_ghost.wav")
#siren background noise
siren = pygame.mixer.Sound("Sounds\Siren.mp3")
siren.set_volume(0.5)
#powerup sound
power_up_sound = pygame.mixer.Sound("Sounds\Powerup.mp3")
#pacman waka sound
WA = False
wa = pygame.mixer.Sound("Sounds\Wa.mp3")
ka = pygame.mixer.Sound("Sounds\Ka.mp3")
#level start sound
Death = pygame.mixer.Sound("Sounds\Death.mp3")
#intro
Intro = pygame.mixer.Sound("Sounds\Intro.mp3")
MUTE = False

#deep copy dots to left and right side arrays
dots_left = copy.deepcopy(Dots)
dots_right = copy.deepcopy(Dots)
#track how many dots were eaten, and at what time the 70th and 176th were so we can drop fruit
DOT_COUNT = 0
DOT_70_TIME = 0
DOT_176_TIME = 0
#rand variable for time to get fruits
FRUIT_TIME_RAND = 0

##pacman sprite download
#resizing pacman image
PACMAN_WIDTH = 60
PACMAN_HEIGHT = 60
Pacman_image = pygame.image.load("Sprites\Pacman\Pacman(1).png")
Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),0)


#lives
#lives
#lives so its easy to spot while editing
PLAYER_LIVES = 0
Lives_Image = pygame.transform.scale(pygame.image.load("Sprites\Pacman\Pacman(2).png"),(PACMAN_WIDTH -10 ,PACMAN_HEIGHT-10 ))
PLAYER_DEATH = False
EXTRA_LIFE = False
LEVEL_UP = False
CURRENT_LEVEL = 0
#menu selection
GAME_START = False
game_over_menu_select = False
INTRO_PLAY = False
INTRO_SEGMENT = False
STARTING_MENU = 0

#background image download
MAZE_WIDTH = 1500
MAZE_HEIGHT = 1400
IMAGE_OFFSET_X = -417
IMAGE_OFFSET_Y = -75
Background_image = pygame.image.load("Background\pacman-game.png")
Menu_image = pygame.image.load("Background\Logo.png")
Menu_image = pygame.transform.scale(Menu_image,(WIDTH-50,150))
Background_image = pygame.transform.scale(Background_image,(MAZE_WIDTH,MAZE_HEIGHT))
#background image resize
Pacman_Image_Arrary = [pygame.image.load("Sprites\Pacman\Pacman(1).png"),pygame.image.load("Sprites\Pacman\Pacman(2).png"),pygame.image.load("Sprites\Pacman\Pacman(3).png"),pygame.image.load("Sprites\Pacman\Pacman(4).png"),pygame.image.load("Sprites\Pacman\Pacman(5).png"),pygame.image.load("Sprites\Pacman\Pacman(6).png"),pygame.image.load("Sprites\Pacman\Pacman(7).png"),pygame.image.load("Sprites\Pacman\Pacman(8).png")]
#initial direction and position
PACMAN_DELTA_X = 1
PACMAN_DELTA_Y = 0
PACMAN_SPEED = 1
PACMAN_STEP_COUNTER = 0
PACMAN_STEP_LOOPS = 0
PACMAN_STARTING_Y = HEIGHT//2 - (PACMAN_HEIGHT/2) + 175
PACMAN_STARTING_X = (WIDTH//2 + 25 - PACMAN_WIDTH/2)

#making fruit class
class Fruit:
    def __init__(self,name):
        self.image = None
        self.point_value = None
FRUIT_EATEN = True
#adding fruits
Cherry = Fruit("Cherry")
Cherry.name = "Cherry"
Cherry.image = pygame.image.load("Sprites\Fruit\Cherry.png")
Cherry.point_value = 100

Strawberry = Fruit("Strawberry")
Strawberry.name = "Strawberry"
Strawberry.image = pygame.image.load("Sprites\Fruit\Strawberry.png")
Strawberry.point_value = 300

Orange = Fruit("Orange")
Orange.name = "Orange"
Orange.image = pygame.image.load("Sprites\Fruit\Orange.png")
Orange.point_value = 500

Apple = Fruit("Apple")
Apple.name = "Apple"
Apple.image = pygame.image.load("Sprites\Fruit\Apple.png")
Apple.point_value = 700

Melon = Fruit("Melon")
Melon.name = "Melon"
Melon.image = pygame.image.load("Sprites\Fruit\Melon.png")
Melon.point_value = 1000

Galaxian = Fruit("Galaxian")
Galaxian.name = "Galaxian"
Galaxian.image = pygame.image.load("Sprites\Fruit\Galaxian.png")
Galaxian.point_value = 2000

Bell = Fruit("Bell")
Bell.name = "Bell"
Bell.image = pygame.image.load("Sprites\Fruit\Bell.png")
Bell.point_value = 3000

Key = Fruit("Key")
Key.name = "Key"
Key.image = pygame.image.load("Sprites\Fruit\Key.png")
Key.point_value = 5000

#making fruit array
Fruit_Array = [Cherry,Strawberry,Orange,Apple,Melon,Galaxian,Bell,Key]
FRUIT_DISPLAY = None

#ghost delta varaibles
CLYDE_DELTA_X = 0
CLYDE_DELTA_Y = 0
BLINKY_DELTA_X = 1
BLINKY_DELTA_Y = 0
INKY_DELTA_X = 0
INKY_DELTA_Y = 0
PINKY_DELTA_X = 0
PINKY_DELTA_Y = 0

#Ghost Speed Multiplier
GHOST_SPEED = 1

#Ghost Node Variables
Node_Blinky = False
Node_Inky = False
Node_Clyde = False
Node_Pinky = False

#Ghost Eaten Variables
Eaten_Blinky = False
Eaten_Inky = False
Eaten_Clyde = False
Eaten_Pinky = False
BLINKY_FRIGHTENED = False
CLYDE_FRIGHTENED = False
INKY_FRIGHTENED  = False
PINKY_FRIGHTENED = False
EATEN_MULTIPLIER = 2
EATEN_COUNTER = 0

#Ghost Frightened Varaibles

#Ghost House Variables
BLINKY_HOUSE = False
CLYDE_HOUSE = True
INKY_HOUSE = True
PINKY_HOUSE = True

#Ghost sprites
GHOST_HEIGHT = 60
GHOST_WIDTH = 60
GHOST_SPRITE_HEIGHT = 50
GHOST_SPRITE_WIDTH = 50
Ghost_Eyes_Right = pygame.image.load("Sprites\Eyes\eyes_right.png")
Ghost_Eyes_Down = pygame.image.load("Sprites\Eyes\eyes_down.png")
Ghost_Eyes_Left = pygame.image.load("Sprites\Eyes\eyes_left.png")
Ghost_Eyes_Up = pygame.image.load("Sprites\Eyes\eyes_up.png")
Blinky_Image_1 = pygame.image.load("Sprites\Blinky\Blinky_1.png")
Blinky_Image_2 = pygame.image.load("Sprites\Blinky\Blinky_2.png")
Clyde_Image_1 = pygame.image.load("Sprites\Clyde\Clyde_1.png")
Clyde_Image_2 = pygame.image.load("Sprites\Clyde\Clyde_2.png")
Inky_Image_1 = pygame.image.load("Sprites\Inky\Inky_1.png")
Inky_Image_2 = pygame.image.load("Sprites\Inky\Inky_2.png")
Pinky_Image_1 = pygame.image.load("Sprites\Pinky\Pinky_1.png")
Pinky_Image_2 = pygame.image.load("Sprites\Pinky\Pinky_2.png")
Frightened_Image_1 = pygame.image.load("Sprites\Frightened\Frightened_1.png")
Frightened_Image_2 = pygame.image.load("Sprites\Frightened\Frightened_2.png")
Frightened_Image_3 = pygame.image.load("Sprites\Frightened\Frightened_3.png")
Frightened_Image_4 = pygame.image.load("Sprites\Frightened\Frightened_4.png")
Eaten_Image = pygame.image.load("Sprites\Eaten\eaten.png")

#Image to be drawn
Blinky_Body = pygame.image.load("Sprites\Blinky\Blinky_1.png")
Blinky_Eyes = pygame.image.load("Sprites\Eyes\eyes_right.png")
Inky_Body = pygame.image.load("Sprites\Inky\Inky_1.png")
Inky_Eyes = pygame.image.load("Sprites\Eyes\eyes_right.png")
Pinky_Body = pygame.image.load("Sprites\Pinky\Pinky_1.png")
Pinky_Eyes = pygame.image.load("Sprites\Eyes\eyes_right.png")
Clyde_Body = pygame.image.load("Sprites\Clyde\Clyde_1.png")
Clyde_Eyes = pygame.image.load("Sprites\Eyes\eyes_right.png")

#ghost starting velocity
START_CLYDE_DELTA_X = 0
START_CLYDE_DELTA_Y = 0
START_BLINKY_DELTA_X = 1
START_BLINKY_DELTA_Y = 0
START_INKY_DELTA_X = 0
START_INKY_DELTA_Y = 0
START_PINKY_DELTA_X = 0
START_PINKY_DELTA_Y = 0

#ghost starting positions
BLINKY_START_Y = (HEIGHT//2 - (GHOST_HEIGHT/2) - 85)
BLINKY_START_X = (WIDTH//2 - GHOST_WIDTH/2 +30)
CLYDE_START_Y = (HEIGHT//2 - (GHOST_HEIGHT/2) - 10)
CLYDE_START_X = (WIDTH//2 - GHOST_WIDTH/2) + 30
INKY_START_Y = (HEIGHT//2 - (GHOST_HEIGHT/2) - 10)
INKY_START_X = (WIDTH//2 - GHOST_WIDTH/2) - 15
PINKY_START_Y = (HEIGHT//2 - (GHOST_HEIGHT/2) - 10)
PINKY_START_X = (WIDTH//2 - GHOST_WIDTH/2) + 75


POWER_UP = False
SCATTER = False
FRIGHTENED = False
POWER_UP_TIMER = 0
CONTACT_TIME = 0
ROUND_START = 240

#Tile to pixel scaler and offset
num1 = (HEIGHT//38)
num2 = (WIDTH//14.5)
y_scaler = 1.86
y_offset = -45
x_scaler = .955
x_offset = -20

#ghosts chase pacman on the start screen
def chase_animation(pacman,blinky,clyde,inky,pinky):
    global Blinky_Body
    global Blinky_Eyes
    global Clyde_Body
    global Clyde_Eyes
    global Inky_Body
    global Inky_Eyes
    global Pinky_Body
    global Pinky_Eyes
    global Pacman_image
    #chase attributes
    chase_y_axis = HEIGHT/2 + 150
    x_mod = 75
    speed = TIMER*3
    starting_pos = 1000
    #sprite resizing
    size_mod = 1.5
    #take a starting x with each step, go back X_mod units. with each time step, move to the right one unit
    i = 0
    while i < 5:
        #pacmanx
        if pinky.x > WIDTH + 100:
            i = 5
        if i == 0:
            pacman.x = speed - starting_pos - x_mod *i
            pacman.y = chase_y_axis - 40
        if i == 1:
            blinky.x = speed - starting_pos - x_mod *i
            blinky.y = chase_y_axis
        if i == 2:
            clyde.x = speed - starting_pos - x_mod *i
            clyde.y = chase_y_axis
        if i == 3:
            inky.x = speed - starting_pos - x_mod *i
            inky.y = chase_y_axis
        if i == 4:
            pinky.x = speed - starting_pos - x_mod *i
            pinky.y = chase_y_axis
        i = i + 1

    #chose ghost sprites
    seconds = int(TIMER/60)
    sprite_flip = int(seconds)
    sprite_flip = int(sprite_flip%2)
    #pick eye direction based on d_x/d_y
    if sprite_flip == 1:
        Inky_Body = Inky_Image_1
        Blinky_Body = Blinky_Image_1
        Pinky_Body = Pinky_Image_1
        Clyde_Body = Clyde_Image_1
    else:
        Inky_Body = Inky_Image_2
        Blinky_Body = Blinky_Image_2
        Pinky_Body = Pinky_Image_2
        Clyde_Body = Clyde_Image_2
    ghost_eyes = Ghost_Eyes_Right
    i = 0
    #scale up ghost sprites
    while i < 4:
        ghost_body = [Blinky_Body, Clyde_Body, Inky_Body, Pinky_Body]
        ghost_eyes = [Blinky_Eyes, Clyde_Eyes, Inky_Eyes, Pinky_Eyes]
        ghost_body[i] = pygame.transform.scale(ghost_body[i],(GHOST_SPRITE_HEIGHT*size_mod,GHOST_SPRITE_WIDTH*size_mod))
        ghost_eyes[i] = pygame.transform.scale(ghost_eyes[i],(GHOST_SPRITE_HEIGHT*size_mod,GHOST_SPRITE_WIDTH*size_mod))
        Blinky_Body = ghost_body[0]
        Blinky_Eyes = ghost_eyes[0]
        Clyde_Body = ghost_body[1]
        Clyde_Eyes = ghost_eyes[1]
        Inky_Body = ghost_body[2]
        Inky_Eyes = ghost_eyes[2]
        Pinky_Body = ghost_body[3]
        Pinky_Eyes = ghost_eyes[3]
        i = i + 1
    pacman_sprite_select(pacman)
    Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH*size_mod,PACMAN_HEIGHT*size_mod)),0)

#mute sounds
def mute_sounds(key_released):
    global MUTE
    if (key_released == [pygame.K_m][0]) or MUTE:
        global eat_fruit
        global eat_ghost
        global siren
        global power_up_sound
        global wa
        global ka
        global Death
        global Intro
        pygame.mixer.pause()
        eat_fruit.set_volume(0)
        eat_ghost.set_volume(0)
        siren.set_volume(0)
        power_up_sound.set_volume(0)
        wa.set_volume(0)
        ka.set_volume(0)
        Death.set_volume(0)

def draw_ghosts(pacman,blinky,clyde,inky,pinky):
    WINDOW.blit(Blinky_Body,(blinky.x - GHOST_SPRITE_WIDTH/2, blinky.y - GHOST_SPRITE_HEIGHT/2))
    WINDOW.blit(Blinky_Eyes,(blinky.x - GHOST_SPRITE_WIDTH/2, blinky.y - GHOST_SPRITE_HEIGHT/2))
    #pygame.draw.circle(WINDOW,(Blinky_Color),(blinky.x, blinky.y),5)
    #Draw Inky and His Eyes
    WINDOW.blit(Inky_Body,(inky.x - GHOST_SPRITE_WIDTH/2, inky.y - GHOST_SPRITE_HEIGHT/2))
    WINDOW.blit(Inky_Eyes,(inky.x - GHOST_SPRITE_WIDTH/2, inky.y - GHOST_SPRITE_HEIGHT/2))
    #pygame.draw.circle(WINDOW,(Inky_Color),(inky.x, inky.y),5)
    #draw clyde and his eyes
    WINDOW.blit(Clyde_Body,(clyde.x - GHOST_SPRITE_WIDTH/2, clyde.y - GHOST_SPRITE_HEIGHT/2))
    WINDOW.blit(Clyde_Eyes,(clyde.x - GHOST_SPRITE_WIDTH/2, clyde.y - GHOST_SPRITE_HEIGHT/2))
    #pygame.draw.circle(WINDOW,(Clyde_Color),(clyde.x, clyde.y),5)
    #draw Pinky and her eyes
    WINDOW.blit(Pinky_Body,(pinky.x - GHOST_SPRITE_WIDTH/2, pinky.y - GHOST_SPRITE_HEIGHT/2))
    WINDOW.blit(Pinky_Eyes,(pinky.x - GHOST_SPRITE_WIDTH/2, pinky.y - GHOST_SPRITE_HEIGHT/2))

#starting game menu
def starting_menu(key_released,blinky,clyde,inky,pinky,pacman):
    global INTRO_SEGMENT
    global STARTING_MENU
    global GAME_START
    global TIMER
    global PLAYER_LIVES
    global game_over_menu_select
    global SUBMITTED
    global SCORE
    global CURRENT_LEVEL
    global dots_left
    global dots_right
    global ROUND_START
    global PLAYER_LIVES
    global CLYDE_HOUSE
    global INKY_HOUSE
    global PINKY_HOUSE
    global CONTACT_TIME
    global DOT_COUNT
    global PLAYER_DEATH
    global LEVEL_UP
    global FRUIT_EATEN
    global INTRO_PLAY
    global SCORER_NAME
    global SCORER_EDIT_COLUMN

    #here incase a player decides to loop around
    if GAME_START == False:
        PLAYER_DEATH = False
        SUBMITTED = False
        INTRO_PLAY = False
        SCORE = 0
        CURRENT_LEVEL = 0
        LEVEL_UP = False
        PLAYER_LIVES = 3
        ROUND_START = 240
        CONTACT_TIME = 0
        DOT_COUNT = 0
        global START_BLINKY_DELTA_X
        global START_BLINKY_DELTA_Y
        FRUIT_EATEN = True
        SCORER_NAME = [0,0,0]
        SCORER_EDIT_COLUMN = 0

        #frame counter
    TIMER = TIMER + 1
    WINDOW.fill((0,0,0))
    #Animate ghost chasing pacman across screen
    if TIMER > 240:
        chase_animation(pacman,blinky,clyde,inky,pinky)
        draw_ghosts(pacman,blinky,clyde,inky,pinky)
        #draw pacman
        WINDOW.blit(Pacman_image,(pacman.x -25, pacman.y + 5))
    #PACMAN title logo    
    WINDOW.blit(Menu_image,(25,25))
    pygame.draw.rect(WINDOW,WHITE,(30,200,WIDTH - 60,5),3)
    if (key_released == [pygame.K_DOWN][0]):
            STARTING_MENU = STARTING_MENU + 1
            #if we are a z wrap back around to a
            if STARTING_MENU > 1:
                STARTING_MENU = 1
        #if we press down, go down a letter
    if (key_released == [pygame.K_UP][0]):
            STARTING_MENU = STARTING_MENU - 1 
            #if we are a a wrap back around to z
            if STARTING_MENU < 0:
                STARTING_MENU = 0

    #menuing options and navigating
    offset = -120
    gap = 100
    if STARTING_MENU == 0:
        #Play pacman is blinking, if they pressed enter, start the game
        draw_text("View High Scores", text_font,WHITE,WIDTH/2, HEIGHT/2 + offset + gap, True)
        if (key_released == [pygame.K_RETURN][0]):
                STARTING_MENU = False
                GAME_START = True
                TIMER = 0
                ROUND_START = 240
                INTRO_SEGMENT = False
                BLINKY_DELTA_X = START_BLINKY_DELTA_X
                BLINKY_DELTA_Y = START_BLINKY_DELTA_Y
                DOT_COUNT = 0
                dots_right = copy.deepcopy(Dots)
                dots_left = copy.deepcopy(Dots)
                clyde.y = CLYDE_START_Y
                clyde.x = CLYDE_START_X
                inky.y = INKY_START_Y
                inky.x = INKY_START_X
                pinky.y = PINKY_START_Y
                pinky.x =PINKY_START_X
                CLYDE_HOUSE = True
                INKY_HOUSE = True
                PINKY_HOUSE = True
                blinky.y = BLINKY_START_Y
                blinky.x = BLINKY_START_X
                pacman.x = PACMAN_STARTING_X
                pacman.y = PACMAN_STARTING_Y
                
        if TIMER%40>15:
            draw_text("PLAY PACMAN",text_font,WHITE,WIDTH/2,HEIGHT/2 + offset,True)
     #select to view scores       
    if STARTING_MENU == 1:
        #View High Score is blinking, if they pressed enter, start the game
        draw_text("PLAY PACMAN",text_font,WHITE,WIDTH/2,HEIGHT/2 + offset,True) 
        if (key_released == [pygame.K_RETURN][0]):
                game_over_menu_select = True
                GAME_START = True
                SUBMITTED = True
                PLAYER_LIVES = 0
        if TIMER%40>15:
            draw_text("View High Scores", text_font,WHITE,WIDTH/2, HEIGHT/2 + offset + gap, True)
    text = "Use arrows keys and press enter to select"
    draw_text(text, menu_font,WHITE,WIDTH/2, HEIGHT/2 + 50, True)
    text = "Press " "'" "m" "'" " to mute audio"
    draw_text(text, menu_font,WHITE,WIDTH/2, HEIGHT/2 + 75, True) 

def intro(pacman):
    global INTRO_PLAY
    global TIMER
    global BLINKY_DELTA_X
    global BLINKY_DELTA_Y
    global INKY_DELTA_X
    global INKY_DELTA_Y
    global CLYDE_DELTA_X
    global CLYDE_DELTA_Y
    global PINKY_DELTA_X
    global PINKY_DELTA_Y
    global PACMAN_DELTA_Y
    global PACMAN_DELTA_X
    global INTRO_SEGMENT
    global Pacman_image
    #makes sure we only play the music once and at the start of the game
    if INTRO_SEGMENT and INTRO_PLAY == False and PLAYER_DEATH == False and POWER_UP == False:
        if TIMER%95 == 0:
            pygame.mixer.Sound.play(siren,0)
    if INTRO_PLAY == False and INTRO_SEGMENT == False:
        pygame.mixer.Sound.play(Intro,0)
        INTRO_PLAY = True
    if INTRO_SEGMENT == False:
        if  TIMER - ROUND_START > 0:
            INTRO_SEGMENT = True
            BLINKY_DELTA_X = 1
            PACMAN_DELTA_X = 1
            TIMER = 0
            INTRO_PLAY = False
        else:
            BLINKY_DELTA_Y = 0
            BLINKY_DELTA_X = 0
            CLYDE_DELTA_Y = 0
            CLYDE_DELTA_X = 0
            INKY_DELTA_Y = 0
            INKY_DELTA_X = 0
            PINKY_DELTA_Y = 0
            PINKY_DELTA_X = 0
            PACMAN_DELTA_Y = 0
            PACMAN_DELTA_X = 0
            Pacman_image = Pacman_Image_Arrary[0]
            Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),0) 
            pacman.x = PACMAN_STARTING_X
            pacman.y = PACMAN_STARTING_Y

def draw_dots(dots):
       num1 = (HEIGHT//36)
       num2 = (WIDTH//13.5)
       x_scaler = .99
       y_scaler = 1 
       ##Draw left dots
       for i in range(len(dots)):
        for j in range(len(dots_left[i])):
            #Small dots on the left
            if dots_left[i][j] == 1:
                pygame.draw.circle(WINDOW, (255,255,255), ((num2 * j//2 + 30) * x_scaler, num1 * i * y_scaler + 83), 2)
            #BIG dots on the left
            if dots_left[i][j] == 2:
                pygame.draw.circle(WINDOW, (255,255,255), ((num2 * j//2 + 30) * x_scaler, num1 * i * y_scaler + 83), 6)
        ##Draw right dots
        for j in range(len(dots_left[i])):
            #Small dots on the right
            if dots_right[i][j] == 1:
                pygame.draw.circle(WINDOW, (255,255,255), (WIDTH-((num2 * j//2 + 32) * x_scaler), num1 * i * y_scaler + 83), 2)
            #Big dots on the right
            if dots_right[i][j] == 2:
                pygame.draw.circle(WINDOW, (255,255,255), (WIDTH-((num2 * j//2 + 32) * x_scaler), num1 * i * y_scaler + 83), 6)
#Draw White Dots for pacman to eat
def clear_dots (dots_left,dots_right,pacman):
        #locating pacmans current coordinate, I did this in another function so i am sure there is a way to pass this number around better
        #note i = x and j = y
        global POWER_UP
        global POWER_UP_TIMER
        global SCORE
        global CLYDE_DELTA_X
        global CLYDE_DELTA_Y
        global BLINKY_DELTA_X 
        global BLINKY_DELTA_Y 
        global INKY_DELTA_X 
        global INKY_DELTA_Y 
        global PINKY_DELTA_X 
        global PINKY_DELTA_Y
        global BLINKY_FRIGHTENED 
        global CLYDE_FRIGHTENED 
        global INKY_FRIGHTENED
        global PINKY_FRIGHTENED
        global DOT_COUNT
        global WA
        global CONTACT_TIME
        num1 = (HEIGHT//38)
        num2 = (WIDTH//14.5)
        #center of pacman sprite   
        pacman_center_x = (pacman.x + PACMAN_WIDTH/2) + x_offset
        pacman_center_y = (pacman.y + PACMAN_HEIGHT/2) + y_offset
        # get pacman I and J on tilesets for their current position
        j = int((pacman_center_y)/num2 * y_scaler) - 1
        i = int((pacman_center_x)/num1 * x_scaler) - 1
        #scrubbing i and j for index error
        if j < 0:
            j = 0
        if i < 0:
            i = 0
        if j > len(dots_right):
            j = len(dots_right)-1
        #if pacman is on the right side
        if i < 13:
            if dots_left[j][i] == 1:
                if WA:
                    pygame.mixer.Sound.play(wa,0)
                    WA = False
                else:
                    WA = True
                SCORE = SCORE + 10
                DOT_COUNT = DOT_COUNT + 1
                dots_left[j][i] = 0
                #Score function incriment_score(muliplier, score)
            if dots_left[j][i] == 2:
                POWER_UP = True
                CLYDE_DELTA_X = CLYDE_DELTA_X * -1
                CLYDE_DELTA_Y = CLYDE_DELTA_Y * -1
                BLINKY_DELTA_X = BLINKY_DELTA_X * -1
                BLINKY_DELTA_Y = BLINKY_DELTA_Y * -1
                INKY_DELTA_X = INKY_DELTA_X * -1
                INKY_DELTA_Y = INKY_DELTA_Y * -1
                PINKY_DELTA_X = PINKY_DELTA_X * -1
                PINKY_DELTA_Y = PINKY_DELTA_Y * -1
                BLINKY_FRIGHTENED = True
                CLYDE_FRIGHTENED = True
                INKY_FRIGHTENED  = True
                PINKY_FRIGHTENED = True
                POWER_UP_TIMER = TIMER
                SCORE = SCORE + 50
                DOT_COUNT = DOT_COUNT + 1
                pygame.mixer.Sound.play(power_up_sound,0)
                dots_left[j][i] = 0
        if i > 12:
            i = i-(2*(i-13))-1
            if dots_right[j][i] == 1:
                if WA:
                    pygame.mixer.Sound.play(wa,0)
                    WA = False
                else:
                    WA = True
                SCORE = SCORE + 10
                DOT_COUNT = DOT_COUNT + 1
                dots_right[j][i] = 0
            if dots_right[j][i] == 2:
                POWER_UP = True
                CLYDE_DELTA_X = CLYDE_DELTA_X * -1
                CLYDE_DELTA_Y = CLYDE_DELTA_Y * -1
                BLINKY_DELTA_X = BLINKY_DELTA_X * -1
                BLINKY_DELTA_Y = BLINKY_DELTA_Y * -1
                INKY_DELTA_X = INKY_DELTA_X * -1
                INKY_DELTA_Y = INKY_DELTA_Y * -1
                PINKY_DELTA_X = PINKY_DELTA_X * -1
                PINKY_DELTA_Y = PINKY_DELTA_Y * -1
                BLINKY_FRIGHTENED = True
                CLYDE_FRIGHTENED = True
                INKY_FRIGHTENED  = True
                PINKY_FRIGHTENED = True
                POWER_UP_TIMER = TIMER
                pygame.mixer.Sound.play(power_up_sound,0)
                SCORE = SCORE + 50
                DOT_COUNT = DOT_COUNT + 1
                dots_right[j][i] = 0
#pacman eating dots  
def draw_fruit(pacman):
    global DOT_70_TIME
    global DOT_176_TIME
    global FRUIT_TIME_RAND
    global FRUIT_EATEN
    global FRUIT_CHOSEN
    global FRUIT_IMAGE
    global SCORE
    global EVENT_TIME
    global EVENT_X
    global EVENT_Y
    global EVENT_VALUE
    center_x = WIDTH/2
    center_y = (HEIGHT/2)+30
    #select a random fruit at 70 or 176 dot count
    if FRUIT_EATEN == True and (DOT_COUNT == 70 or DOT_COUNT == 176):
        DOT_70_TIME = TIMER
        FRUIT_EATEN = False
        i = CURRENT_LEVEL
        if DOT_COUNT > 175:
            i = i + 1
        if i > len(Fruit_Array):
            i = len(Fruit_Array) - 1
        FRUIT_TIME_RAND = random.randrange(540,600)
        FRUIT_CHOSEN = Fruit_Array[i]
        FRUIT_IMAGE = pygame.transform.scale(FRUIT_CHOSEN.image,(70,70))
    fruit_available = 0 < FRUIT_TIME_RAND + DOT_70_TIME - TIMER
    if fruit_available:
        if FRUIT_EATEN == False:
            WINDOW.blit(FRUIT_IMAGE,(center_x-35,center_y-35))
            if (center_x < pacman.centerx < center_x + 30) and (center_y - 8 < pacman.centery < center_y + 8):
                #remove and award points
                FRUIT_EATEN = True
                SCORE = SCORE + FRUIT_CHOSEN.point_value
                EVENT_TIME = TIMER
                EVENT_Y = pacman.centery
                EVENT_X = pacman.centerx
                EVENT_VALUE = FRUIT_CHOSEN.point_value
                pygame.mixer.Sound.play(eat_fruit)

def draw_lives():
    global PLAYER_LIVES
    global EXTRA_LIFE
    if SCORE > 10000 and EXTRA_LIFE == False:
        #play extra life sound
        PLAYER_LIVES = PLAYER_LIVES + 1
        EXTRA_LIFE = True
    if PLAYER_LIVES == 0:
        draw_text("GAME",text_font,WHITE,WIDTH/2 - 75,HEIGHT/2+15,False)
        draw_text("OVER",text_font,WHITE,WIDTH/2 + 5,(HEIGHT/2+15),False)
        draw_text("Press Enter to continue",event_font,WHITE,WIDTH/2,(HEIGHT/2+40),True)
    i = 0
    j = PLAYER_LIVES - 1
    while i < j:
        WINDOW.blit(Lives_Image,(5 + i* 30, 810))
        i = i + 1

def draw_text(text,font,text_col,x,y,centered):
    img = font.render(text,True, text_col)
    text_size = img.get_size()
    if centered:
        a = text_size[0]/2
        b = text_size[1]/2
    else:
        a = 0
        b = 0
     
    WINDOW.blit(img,(x-a,y-b))

def show_scoring_event():    
        global EVENT_X
        global EVENT_Y
        global EVENT_TIME
        #undulating motion function
        y_shift = int((4 * math.sin(1 * math.pi * TIMER /10)+(TIMER-EVENT_TIME))/5)
        x_shift = int(((TIMER-EVENT_TIME)/5))
        elapsed_time = TIMER - EVENT_TIME
        if 0 < elapsed_time < 60:
            value = str(EVENT_VALUE)
            draw_text(value,event_font,WHITE,EVENT_X - x_shift - 40,EVENT_Y - y_shift - 10,False)
#resets the board on death, levelup and new game
def board_rest(pacman,blinky,clyde,inky,pinky):
    global CURRENT_LEVEL
    global LEVEL_UP
    global dots_left
    global dots_right
    global ROUND_START
    global INTRO_PLAY
    global PLAYER_DEATH
    global BLINKY_DELTA_X
    global BLINKY_DELTA_Y
    global INKY_DELTA_X
    global INKY_DELTA_Y
    global CLYDE_DELTA_X
    global CLYDE_DELTA_Y
    global PINKY_DELTA_X
    global PINKY_DELTA_Y
    global PACMAN_DELTA_Y
    global PACMAN_DELTA_X
    global TIMER
    global PLAYER_LIVES
    global Pacman_image
    global BLINKY_HOUSE
    global CLYDE_HOUSE
    global INKY_HOUSE
    global PINKY_HOUSE
    global Eaten_Blinky
    global Eaten_Clyde
    global Eaten_Inky
    global Eaten_Pinky
    global POWER_UP
    global FRUIT_EATEN
    if PLAYER_DEATH or LEVEL_UP:
        contact_time = CONTACT_TIME

        #time holding in seconds before restarting movement
        reset_hold = 5
        #convert seconds of hold to frames
        reset_hold = reset_hold * 60
        resume_time = contact_time + reset_hold
        #everyone stops
        BLINKY_DELTA_Y = 0
        BLINKY_DELTA_X = 0
        CLYDE_DELTA_Y = 0
        CLYDE_DELTA_X = 0
        INKY_DELTA_Y = 0
        INKY_DELTA_X = 0
        PINKY_DELTA_Y = 0
        PINKY_DELTA_X = 0
        Eaten_Pinky = False
        Eaten_Blinky = False
        Eaten_Clyde = False
        Eaten_Inky = False
        POWER_UP = False
        FRUIT_EATEN = True
        #log pacmans rotation, then stop his movement
        rotation = 0
        flip = False
        if PACMAN_DELTA_Y != 0:
            if PACMAN_DELTA_Y == 1:
                rotation = 270
            else:
                rotation = 90
        if PACMAN_DELTA_X != 0:
            if PACMAN_DELTA_X == -1:
                flip = True
        #pacman dying animation for 2 seconds
        array_count = 0
        step_counter = PACMAN_STEP_COUNTER
        if 0 < step_counter <= 3 or 15 < step_counter <= 18:
                array_count = 0
            #if counter 10<x<=20 pic 2
        if 3 < step_counter <= 6 or 12 < step_counter <= 15:
                array_count = 1
             #if counter 20<x<=30 pic 3
        if 6 < step_counter <= 12:
                array_count = 2
        #determine initial array posiiton and if the player dies, do animation. 
        if PLAYER_DEATH:
            array_count = array_count + 1
            i = 0
            while i < 8:
                if TIMER > contact_time + 10*i:
                    array_count = i
                    i = i + 1
                else:
                    array_count = i
                    i = 8
                #if this is done while the player had one life, they are dead
        #draw pacman image
        Pacman_image = Pacman_Image_Arrary[array_count]
        Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),rotation)
        if flip:
            Pacman_image = pygame.transform.flip(Pacman_image,True,False)    
        #move all ghosts off map 
        if resume_time - 240 > TIMER:
            blinky.y = -100
            clyde.y = -100
            pinky.y = -100
            inky.y = -100

        #move everyone to start and hold for 4 seconds
        if resume_time > TIMER > resume_time - 240:
            if INTRO_PLAY == False and (PLAYER_DEATH or LEVEL_UP) == True and TIMER == resume_time - 235:
                if (PLAYER_DEATH and PLAYER_LIVES > 1) or (LEVEL_UP and PLAYER_LIVES > 0):
                    pygame.mixer.Sound.play(Intro,0)
                    INTRO_PLAY = True
            #allow ghost house to bounce
            if resume_time - 230 >TIMER:
                clyde.y = CLYDE_START_Y
                clyde.x = CLYDE_START_X
                inky.y = INKY_START_Y
                inky.x = INKY_START_X
                pinky.y = PINKY_START_Y
                pinky.x =PINKY_START_X
                CLYDE_HOUSE = True
                INKY_HOUSE = True
                PINKY_HOUSE = True
            if resume_time - 230 == TIMER and LEVEL_UP == False:
                PLAYER_LIVES = PLAYER_LIVES - 1
            blinky.y = BLINKY_START_Y
            blinky.x = BLINKY_START_X
            pacman.x = PACMAN_STARTING_X
            pacman.y = PACMAN_STARTING_Y
            PACMAN_DELTA_X = 1
            PACMAN_DELTA_Y = 0
            Pacman_image = Pacman_Image_Arrary[0]
            Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),0)

        if resume_time < TIMER:
            if LEVEL_UP:
                dots_left = copy.deepcopy(Dots)
                dots_right = copy.deepcopy(Dots)
                contact_time = 0
                resume_time = 300
                LEVEL_UP = False
            INTRO_PLAY = False
            BLINKY_DELTA_Y = START_BLINKY_DELTA_Y
            BLINKY_DELTA_X = START_BLINKY_DELTA_X
            CLYDE_DELTA_Y = START_CLYDE_DELTA_Y
            CLYDE_DELTA_X = START_CLYDE_DELTA_X
            INKY_DELTA_Y = START_INKY_DELTA_Y
            INKY_DELTA_X = START_INKY_DELTA_X
            PINKY_DELTA_Y = START_PINKY_DELTA_Y
            PINKY_DELTA_X = START_PINKY_DELTA_X
            pacman.x = PACMAN_STARTING_X
            pacman.y = PACMAN_STARTING_Y
            blinky.y = BLINKY_START_Y
            blinky.x = BLINKY_START_X
            clyde.y = CLYDE_START_Y
            clyde.x = CLYDE_START_X
            inky.y = INKY_START_Y
            inky.x = INKY_START_X
            pinky.y = PINKY_START_Y
            pinky.x =PINKY_START_X
            CLYDE_HOUSE = True
            INKY_HOUSE = True
            PINKY_HOUSE = True
            BLINKY_HOUSE = False
            TIMER = contact_time
            PLAYER_DEATH = False
        ROUND_START = resume_time - 60

def level_up(pacman,blinky,clyde,inky,pinky): ##BIG TO DO
    global CONTACT_TIME
    global CURRENT_LEVEL
    global LEVEL_UP
    global DOT_70_TIME
    global DOT_176_TIME
    global DOT_COUNT
    #if all the dots are cleared, increase level by 1 and reset the board
    if DOT_COUNT == 244:
        #recopy the dots to the board and reset the dot count
        DOT_COUNT = 0
        CONTACT_TIME = TIMER
        CURRENT_LEVEL = CURRENT_LEVEL + 1
        LEVEL_UP = True
        #run player death to reset location
        #reuse as much intro as possible 
    
    
    #see if there is a way to shorten powerup without it being a nightmare   

def game_over(pacman,blinky,clyde,inky,pinky,key_pressed,key_released):
        global game_over_menu_select
        if key_released == [pygame.K_RETURN][0] and game_over_menu_select == False:
            game_over_menu_select = True
            key_released = None
        global BLINKY_DELTA_X
        global BLINKY_DELTA_Y
        global INKY_DELTA_X
        global INKY_DELTA_Y
        global CLYDE_DELTA_X
        global CLYDE_DELTA_Y
        global PINKY_DELTA_X
        global PINKY_DELTA_Y
        global PACMAN_DELTA_Y
        global PACMAN_DELTA_X
        global Pacman_image
        global BLINKY_HOUSE
        global CLYDE_HOUSE
        global INKY_HOUSE
        global PINKY_HOUSE
        global Eaten_Blinky
        global Eaten_Clyde
        global Eaten_Inky
        global Eaten_Pinky
        global POWER_UP
        global TIMER
        global ROUND_START
        global Blinky_Body
        global Blinky_Eyes
        global Clyde_Body
        global Clyde_Eyes
        global Inky_Body
        global Inky_Eyes
        global Pinky_Body
        global Pinky_Eyes
        #all ghosts stop
        BLINKY_DELTA_Y = 0
        BLINKY_DELTA_X = 0
        CLYDE_DELTA_Y = 0
        CLYDE_DELTA_X = 0
        INKY_DELTA_Y = 0
        INKY_DELTA_X = 0
        PINKY_DELTA_Y = 0
        PINKY_DELTA_X = 0
        PACMAN_DELTA_X = 0
        PACMAN_DELTA_Y = 0

        blinky.y = BLINKY_START_Y
        blinky.x = BLINKY_START_X
        pacman.x = PACMAN_STARTING_X
        pacman.y = PACMAN_STARTING_Y
        Eaten_Pinky = False
        Eaten_Blinky = False
        Eaten_Clyde = False
        Eaten_Inky = False
        POWER_UP = False
        #makes  C, P and I bounce while on the game over menu
        bounce_in_ghost_house(inky,0)
        bounce_in_ghost_house(pinky,0)
        bounce_in_ghost_house(clyde,15)
        #chose ghost sprites
        seconds = int(TIMER/60)
        sprite_flip = int(seconds/7)
        sprite_flip = int(sprite_flip%2)
        #pick eye direction based on d_x/d_y
        if sprite_flip == 1:
            Inky_Body = Inky_Image_1
            Blinky_Body = Blinky_Image_1
            Inky_Body = Inky_Image_1
            Clyde_Body = Clyde_Image_1
        else:
            Inky_Body = Inky_Image_2
            Blinky_Body = Blinky_Image_2
            Inky_Body = Inky_Image_2
            Clyde_Body = Clyde_Image_2
        
        i = 0
        #scale up ghost sprites
        while i < 4:
            ghost_body = [Blinky_Body, Clyde_Body, Inky_Body, Pinky_Body]
            ghost_eyes = [Blinky_Eyes, Clyde_Eyes, Inky_Eyes, Pinky_Eyes]
            ghost_body[i] = pygame.transform.scale(ghost_body[i],(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))
            ghost_eyes[i] = pygame.transform.scale(ghost_eyes[i],(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))
            Blinky_Body = ghost_body[0]
            Blinky_Eyes = ghost_eyes[0]
            Clyde_Body = ghost_body[1]
            Clyde_Eyes = ghost_eyes[1]
            Inky_Body = ghost_body[2]
            Inky_Eyes = ghost_eyes[2]
            Pinky_Body = ghost_body[3]
            Pinky_Eyes = ghost_eyes[3]
            i = i + 1
        
        Pacman_image = Pacman_Image_Arrary[0]
        Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),0)
        TIMER = TIMER + 1
#add name to high score function
def update_high_scores(SCORE,name):
    global SUBMITTED
    # Load existing high scores from the high_scores file
    high_scores_list = High_Scores.load_high_scores()

    # Check if the new score is in the top 20
    if len(high_scores_list) < 20 or SCORE > high_scores_list[-1]['score']:
        # Prompt the player for their name
        name = name

        # Create a new entry with the player's name and score
        new_entry = {'name': name, 'score': SCORE}

        # Add the new entry to the high scores list
        high_scores_list.append(new_entry)

        # Sort the high scores list in descending order based on the score
        high_scores_list.sort(key=lambda x: x['score'], reverse=True)

        # Keep only the top 20 scores
        high_scores_list = high_scores_list[:20]

        # Save the updated high scores back to the high_scores file
        High_Scores.save_high_scores(high_scores_list)
        SUBMITTED = True
#input name for highscore  
def input_name(key_released):
    global EDITED
    global GAME_START
    global game_over_menu_select
    global PLAYER_DEATH
    global PLAYER_LIVES
    global CURRENT_LEVEL
    global LEVEL_UP
    if key_released != (False or None):
        global SCORER_NAME
        global SCORER_EDIT_COLUMN
        #if we press up, go up a letter
        if (key_released == [pygame.K_UP][0]):
            SCORER_NAME[SCORER_EDIT_COLUMN] = SCORER_NAME[SCORER_EDIT_COLUMN] + 1
            #if we are a z wrap back around to a
            if SCORER_NAME[SCORER_EDIT_COLUMN] > 25:
                SCORER_NAME[SCORER_EDIT_COLUMN] = 0
            EDITED = True
        #if we press down, go down a letter
        if (key_released == [pygame.K_DOWN][0]):
            SCORER_NAME[SCORER_EDIT_COLUMN] = SCORER_NAME[SCORER_EDIT_COLUMN] - 1 
            #if we are a a wrap back around to z
            if SCORER_NAME[SCORER_EDIT_COLUMN] > 25:
                SCORER_NAME[SCORER_EDIT_COLUMN] = 0
            EDITED = True
        #if we press left, move left, if we are all the way left, stay there
        if (key_released == [pygame.K_LEFT][0]):
            SCORER_EDIT_COLUMN = SCORER_EDIT_COLUMN - 1
            if SCORER_EDIT_COLUMN < 0:
                SCORER_EDIT_COLUMN = 0
            EDITED = True
        #if we pressed right, move right, if we are all the way right, stay there
        if (key_released == [pygame.K_RIGHT][0]):
            SCORER_EDIT_COLUMN = SCORER_EDIT_COLUMN + 1
            if SCORER_EDIT_COLUMN > 2:
                SCORER_EDIT_COLUMN = 2
            EDITED = True
    #current name input
    name = ALHAPHABET[SCORER_NAME[0]]+ALHAPHABET[SCORER_NAME[1]]+ALHAPHABET[SCORER_NAME[2]]
    #draw triangles above and below selecte column
    letter_top_left_x = WIDTH/2 - 28 + SCORER_EDIT_COLUMN*18
    letter_y = 143
    letter_width = 17
    letter_height = 17
    if SUBMITTED == False:
        #show current name
        draw_text(name,text_font,WHITE,WIDTH/2,150,True)
        #draw trianges above and below letter
        #left, top, right coordinate order
        pygame.draw.polygon(WINDOW,WHITE,((letter_top_left_x,letter_y - 5),(letter_top_left_x +(letter_width/2),letter_y - 10),(letter_top_left_x + letter_width,letter_y - 5)),0)
        pygame.draw.polygon(WINDOW,WHITE,((letter_top_left_x,letter_y + letter_height + 5),(letter_top_left_x +(letter_width/2),letter_y + letter_height + 10),(letter_top_left_x + letter_width,letter_y + letter_height + 5)),0)
        #make selected column blink off for 6 ticks every 30 game ticks
        if TIMER%40>15:
            #select current column and just draw a black box over it
            pygame.draw.rect(WINDOW,BLACK,(letter_top_left_x,letter_y,letter_width,letter_height),0)
    if SUBMITTED:
        text = "Press Enter to Return to the Start Menu"    
        draw_text(text,menu_font,WHITE,WIDTH/2,letter_y,True)
        if (key_released == [pygame.K_RETURN][0]):
            GAME_START = False
            game_over_menu_select = False
            PLAYER_DEATH = False
            LEVEL_UP = True
    if EDITED and (key_released == [pygame.K_RETURN][0]) and SUBMITTED == False:
        update_high_scores(SCORE,name)        
#menu to see your score and the high score list
def game_over_menu(key_released):
    global game_over_menu_select
    global PLAYER_DEATH
    global PLAYER_LIVES
    global GAME_START
    global CURRENT_LEVEL
    global LEVEL_UP
    global TIMER
    TIMER = TIMER + 1
    if game_over_menu_select:
        #new background image Black with a white bar to show your
        high_scores_list = High_Scores.load_high_scores()
        list_length = len(high_scores_list)
        WINDOW.fill((0,0,0))
        pygame.draw.rect(WINDOW,WHITE,(30,55,WIDTH - 60,5),3)
        #show your score if you played
        if SCORE > 0:
            Score_str = str(SCORE)
            total_score = "Your Score: " + Score_str
            draw_text(total_score ,text_font,WHITE,WIDTH/2,40,True)
        #show current top scores below
        i = 0
        while i < list_length:
            #get scorers name off the list
            #look at current entry
            score_entry = high_scores_list[i]
            #print entry Postion. Name: Score
            text = f"{i + 1}. {score_entry['name']}: {score_entry['score']}"
            if SCORE == 0:
                y = 100
            else:
                y = 200
            draw_text(text ,text_font,WHITE,WIDTH/2,y + 30 * i,True)
            i = i + 1
        #check to see if you fall on the high score list
        i = 0
        scorer = False
        while i < list_length:
            #get scorers name off the list
            #look at current entry
            score_entry = high_scores_list[i]
            if SCORE > score_entry['score']:
                draw_text("You earned a high score" ,text_font,WHITE,WIDTH/2,80,True)
                scorer = True
                i = list_length
            i = i + 1
            #if there are less than 20 number on the list, you made the cut
        if list_length < 20 and SCORE > 0:
            draw_text("You earned a high score" ,text_font,WHITE,WIDTH/2,80,True)
            scorer = True
        #if you were a scorer, display your score
        if scorer:
            draw_text("Use the Arrow keys to enter your name" ,text_font,WHITE,WIDTH/2,100,True)
            input_name(key_released)
        #if we get to the end of the list, and they are not a scorer
        if i == list_length and scorer == False:
            #show your score at the top
            #if they jumped to see the list
            if SCORE == 0:
                top = "Top "
                x= str(len(high_scores_list))
                scorers = " Scorers in Pacman"
                text = top + x + scorers
                draw_text(text,text_font,WHITE,WIDTH/2,40,True)
            text = "Press Enter to Return to the Start Menu"    
            draw_text(text,menu_font,WHITE,WIDTH/2,70,True)
            if (key_released == [pygame.K_RETURN][0]):
                GAME_START = False
                game_over_menu_select = False
                PLAYER_DEATH = False 
                TIMER = 0        
#for visual debugging purposes
Active_area = PLAY_AREA
def visualize_area(Active_area):
    #Showing Activity area
        #note i = x and j = y
        num1 = (HEIGHT//38)
        num2 = (WIDTH//14.5)
        ##Draw left dots
        for i in range(len(Active_area)):
            for j in range(len(Active_area[i])):
            #Small dots on the left
                if Active_area[i][j] == 1:
                    pygame.draw.circle(WINDOW, (255,0,0), (((num2 * j//2 ) *x_scaler) + x_offset , ((num1 * i * y_scaler) + y_offset)), 3)
                if Active_area[i][j] == 2:
                    pygame.draw.circle(WINDOW, (255,0,0), (((num2 * j//2 ) *x_scaler) + x_offset , ((num1 * i * y_scaler) + y_offset)), 9)
        ##Draw right dots
            for j in range(len(Active_area[i])):
            #Small dots on the right
                if Active_area[i][j] == 1:
                    pygame.draw.circle(WINDOW, (255,0,0), (WIDTH-((num2 * j//2 ) *x_scaler) - x_offset , ((num1 * i * y_scaler) + y_offset)), 3)
                if Active_area[i][j] == 2:
                    pygame.draw.circle(WINDOW, (255,0,0), (WIDTH-((num2 * j//2 ) *x_scaler) - x_offset , ((num1 * i * y_scaler) + y_offset)), 9)
#makes the ghosts bounce in the house
def bounce_in_ghost_house(ghost,offset):
        global TIMER
        current_time = TIMER + offset
        y_shift = int(2.3 * math.sin(1 * math.pi * current_time / 15))
        ghost.y = ghost.y + y_shift
#navigates ghosts out of the hosue
def leave_ghost_house(ghost,pacman,d_x,d_y):
        #center in the ghost house
        if ghost.x < WIDTH/2 - 1 or ghost.x > WIDTH/2 + 1:
            if ghost.x < WIDTH/2 - 1:
                d_x = 1
                d_y = 0
            else:
                d_x = -1
                d_y = 0
        else:
            #start moving up out of the ghost house once I am centered
            d_y = -1
            d_x = 0
        #if my y is == blinky start line, im out and can start chasing
        house = True
        if ghost.y <= (HEIGHT//2 - (GHOST_HEIGHT/2) - 85):
            #pick the best x direction to close on pacman
            d_y = 0
            if pacman.x > ghost.x:
                d_x = 1
            else: 
                d_x = -1
            house = False
        return house,d_x,d_y
        #set ghost house to false
#navigates ghosts into the house
def enter_ghost_house(ghost,d_x,d_y):
        d_x = 0
        d_y = 1
        #if the space is huntable 2 then its a wall, pull a 180 and set eaten to false
        eaten = True
        frightened = True
        #if the ghost is over the house, it is not scared anymore
        if ghost.y > (HEIGHT//2 - (GHOST_HEIGHT/2) - 10):
                ghost.y == (HEIGHT//2 - (GHOST_HEIGHT/2) - 10)
                d_x = 0
                d_y = -1
                eaten = False
                frightened = False
        return eaten,frightened, d_x, d_y
#defines areas or tiles pacman can enter
def playable_zone(d_x, d_y,pacman,playable):
     #finds current column or row and centers pacman in that column or row
        x_offset = 3
        y_offset = 3
        #i am sure there is a much more elegant solution
        column_center = [58,104,176,250,321,395,465,539,611,657]
        row_center = [82,182,254,331,402,478,552,626,700,774]
        
        
        #note i = x and j = y
        playable = True
        view_distance = 14
        num1 = (HEIGHT//38)
        num2 = (WIDTH//14.5)
    #center of pacman sprite   
        pacman_center_x = (pacman.x + PACMAN_WIDTH/2) + x_offset
        pacman_center_y = (pacman.y + PACMAN_HEIGHT/2) + y_offset
    # get pacman I and J on tilesets for their current position
        pacman_j = int((pacman_center_y)/num2 * y_scaler)
        pacman_i = int((pacman_center_x)/num1 * x_scaler)    
    # whichever the desireed direction is, shoot a line 10 pixels from pacman center
        viewed_x = (pacman_center_x) + (d_x*(view_distance))
        viewed_y = (pacman_center_y)+ (d_y*(view_distance) + 2)
    #convert viewed coordinates into I/J values
        viewed_i = int((viewed_x)/num1 * x_scaler) - 1
        viewed_j = int((viewed_y)/num2 * y_scaler) - 2
    #convert viewed coordinates into I/J values
        
    #unsure I and J fall within array range
        #if i move to the middle flip my counter so I am counting down
        if viewed_i > (len(PLAY_AREA[0])-2):
            viewed_i = viewed_i-(2*(viewed_i-13))+1
        if pacman_i > (len(PLAY_AREA[0])-2):
            pacman_i = pacman_i-(2*(pacman_i-13))+1
        #line for tunnel jump
        if (pacman_i < 5 and viewed_j == 14):
                viewed_i = 0
                if d_y != 0:
                    return False
                if (pacman.x < -PACMAN_WIDTH) and (d_x == -1):
                    pacman.x = pacman.x + WIDTH + 60
                if (pacman.x > WIDTH + 15) and (d_x == 1):
                    pacman.x = pacman.x - WIDTH - 60
                return True
        #if i try and walk off either side the lower x bound movement is stopped
        if viewed_i < 0:
            viewed_i = 0
            return False
        #if i move to the top or bottom stop me from going further
        if (viewed_j < 0) or (viewed_j > (len(PLAY_AREA))):
            viewed_j = 0
            return False
        #scrubbing viewed_i and viewed_j for overflow
        if viewed_i < 0:
            viewed_i = 0
        if viewed_i > (len(PLAY_AREA[0])):
            viewed_i = len(PLAY_AREA[0])-1
        if viewed_j < 0:
            viewed_j = 0
        if viewed_j > (len(PLAY_AREA)-1):
            viewed_j = len(PLAY_AREA)-1

        # if that line falls inside a valid tile I can move

        if PLAY_AREA[viewed_j][viewed_i] > 0:
            #if the viewed tile is >0 then it is a valid play tile    
            #if d_x != stored d_x and d_y != stored d_y, then the player is trying to turn 90 degrees.
            if d_x != PACMAN_DELTA_X and d_y != PACMAN_DELTA_Y:
            #if pacman is not near the center of the next column, he cannot swith
                #this works great, only thing I dont like is that he kind of floats around corners
                #fudge facotr around center
                x_offset = 4
                y_offset = 4
                sprite = pacman
                if d_y != 0:
                    for i in range(len(column_center)): 
                        if sprite.centerx > (column_center[i] - x_offset) and sprite.centerx < (column_center[i] + x_offset):
                            return True
                    return False    
                if d_x != 0:
                    for i in range(len(row_center)): 
                        if sprite.centery > (row_center[i] - y_offset) and sprite.centery < (row_center[i] + y_offset):
                            return True
                    return False      
            return True
        ## if the next are is a valid play area pacman keeps moving
        return False
#centers the ghosts in their rows or columns
def ghost_center(sprite,d_x,d_y):
     #take characters current tile center vs his current center
    #ensures the ghosts are at or close to the center of their tunnels
        sprite_j = 0
        sprite_i = 0
        #center of sprite   
    # get I and J on tilesets for their current position and find the x/y at the center of that tile
        current_i = int((sprite.centery)/num2 * y_scaler) 
        current_j = int((sprite.centerx)/num1 * x_scaler)

        center_current_tile_y = int((current_i + 1)/y_scaler*num2) - 6
        center_current_tile_x = int(current_j/x_scaler*num1) +18
    
        a = sprite.centery - center_current_tile_y
        b = sprite.centerx - center_current_tile_x
        if d_y == 0:
            if a < 0:
                sprite.y = sprite.y + 1
            if a > 0:
                sprite.y = sprite.y - 1
        if d_x == 0:
            b = 0
            if b < 0:
                sprite.x = sprite.x + 1
            if b > 0:
                sprite.x = sprite.x - 1
#centers pacman in his row or column
def pacman_center(sprite,d_x,d_y):
     #trying to center pacman in the channels, but I am having a rough go of it
     #finds current column or row and centers pacman in that column or row
        x_offset = 15
        y_offset = 15
        #i am sure there is a much more elegant solution
        column_center = [58,104,176,250,321,395,465,539,610,657]
        row_center = [82,182,254,329,402,478,552,625,700,774]
        #this works great, only thing I dont like is that he kind of floats around corners
        if PACMAN_DELTA_X == 0:
            for i in range(len(column_center)): 
                if sprite.centerx > (column_center[i] - x_offset) and sprite.centerx < (column_center[i] + x_offset):
                    if sprite.centerx>column_center[i]:
                         sprite.centerx = sprite.centerx - 1
                    if sprite.centerx<column_center[i]:
                         sprite.centerx = sprite.centerx + 1
                    else:
                         sprite.centerx = sprite.centerx
                    return
        if PACMAN_DELTA_Y == 0:
            for i in range(len(row_center)): 
                if sprite.centery > (row_center[i] - y_offset) and sprite.centery < (row_center[i] + y_offset):
                    if sprite.centery>row_center[i]:
                         sprite.centery = sprite.centery - 1
                    if sprite.centery<row_center[i]:
                         sprite.centery = sprite.centery + 1
                    else:
                         sprite.centery = sprite.centery
                    return
#checks for pacman collisions
def pacman_contact(sprite,pacman,eaten,frightened):
    global PLAYER_LIVES
    global PLAYER_DEATH
    global CONTACT_TIME
    global EVENT_TIME
    global EVENT_X
    global EVENT_Y
    global EVENT_VALUE
    global EATEN_COUNTER
    #find distance betwee the two
    dist_x = pacman.centerx - sprite.centerx
    dist_y = pacman.centery - sprite.centery + 30
    #if x & y < some distance contact
    global SCORE
    if abs(dist_x) < 15 and abs(dist_y) < 15:
        #if a ghost is scared and powerup is active, eat them, they are no longer scared, but are eaten
        if POWER_UP and frightened:
            EATEN_COUNTER = EATEN_COUNTER + 1
            eaten = True
            pygame.mixer.Sound.play(eat_ghost,0)
            SCORE = SCORE + (2**EATEN_COUNTER)*100
            EVENT_TIME = TIMER
            EVENT_Y = pacman.centery
            EVENT_X = pacman.centerx
            EVENT_VALUE = (2**EATEN_COUNTER)*100
            frightened = False
        #if we arent powered up, they are not frightened
        if POWER_UP == False:
            frightened = False
        #if a ghost is not eaten or scared, meaning no powerup or they went to the house, we die
        if eaten == False and frightened == False:
            PLAYER_DEATH = True
            CONTACT_TIME = TIMER
            pygame.mixer.Sound.play(Death,0)
    return eaten, frightened
#selects pacman sprite
def pacman_sprite_select(pacman):
    global PACMAN_STEP_COUNTER
    global PACMAN_STEP_LOOPS
    global Pacman_image
    loop_counter = PACMAN_STEP_LOOPS
    step_counter = PACMAN_STEP_COUNTER + 1
    #restart cycle when it gets to high
    rotation = 0
    if PACMAN_DELTA_Y != 0:
        if PACMAN_DELTA_Y == 1:
            rotation = 270
        else:
            rotation = 90
    if step_counter > 12:
        step_counter = 1
        loop_counter = loop_counter + 1
    if loop_counter > 1:
        loop_counter = 0
        #pygame.mixer.Sound.play(chomp,1)
    #if counter 0<x<=10 pic 2
    if 0 < step_counter <= 3 or 15 < step_counter <= 18:
        Pacman_image = Pacman_Image_Arrary[0]
        Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),rotation)
    #if counter 10<x<=20 pic 2
    if 3 < step_counter <= 6 or 12 < step_counter <= 15:
        Pacman_image = Pacman_Image_Arrary[1]
        Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),rotation)
    #if counter 20<x<=30 pic 3
    if 6 < step_counter <= 12:
        Pacman_image = Pacman_Image_Arrary[2]
        Pacman_image = pygame.transform.rotate(pygame.transform.scale(Pacman_image,(PACMAN_WIDTH,PACMAN_HEIGHT)),rotation)
    if PACMAN_DELTA_X == -1:
        Pacman_image = pygame.transform.flip(Pacman_image,True,False)
    PACMAN_STEP_COUNTER = step_counter
    PACMAN_STEP_LOOPS = loop_counter
    return Pacman_image
#player pacman input
def pacman_movement(key_pressed,pacman):      
        #Declaring vector variables
        playable = True
        global PACMAN_DELTA_X
        global PACMAN_DELTA_Y
        global TIMER
        starting_d_x = PACMAN_DELTA_X
        starting_d_y = PACMAN_DELTA_Y
        global PACMAN_STEP_COUNTER
        global PACMAN_STEP_LOOPS
        global Pacman_image
        d_x = PACMAN_DELTA_X
        d_y = PACMAN_DELTA_Y
        sprite = pacman
        TIMER = TIMER + 1       
        #left input
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            d_x = -1             
            d_y = 0
        #right input
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            d_x = 1  
            d_y = 0
        #up input
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]: 
            d_x = 0
            d_y = -1
        #down input
        if key_pressed[pygame.K_s]or key_pressed[pygame.K_DOWN]: 
            d_x = 0
            d_y = 1      
        if playable_zone(d_x,d_y,pacman,playable):
            PACMAN_DELTA_X = d_x
            PACMAN_DELTA_Y= d_y
        else:
            PACMAN_DELTA_X = d_x = starting_d_x
            PACMAN_DELTA_Y = d_y = starting_d_y

        pacman_center(sprite,d_x,d_y)
        velx = ((VEL * PACMAN_DELTA_X) * PACMAN_SPEED)
        vely = ((VEL * PACMAN_DELTA_Y) * PACMAN_SPEED)
        if vely < 0 or velx < 0:
            velx = velx * VEL_BANDAID
            vely = vely * VEL_BANDAID

#        step_counter = PACMAN_STEP_COUNTER
#        loop_counter = PACMAN_STEP_LOOPS

        if playable_zone(d_x,d_y,pacman,playable) and PLAYER_DEATH == False:
            pacman.x = (pacman.x + velx)
            pacman.y = (pacman.y + vely) 
            #pacman_image_select(pacman)
            Pacman_image = pacman_sprite_select(pacman)
            #take one extra step every 20 frames
            if TIMER % 20==0:
                pacman.x = (pacman.x + velx)
                pacman.y = (pacman.y + vely)          
#ghost pretimed scatters
def scatter(TIMER,blinky,clyde,inky,pinky):
     #pacman is powered up scatter is active
    global SCATTER
    global FRIGHTENED
    global POWER_UP
    global GHOST_SPEED
    global CLYDE_DELTA_X
    global CLYDE_DELTA_Y
    global BLINKY_DELTA_X 
    global BLINKY_DELTA_Y 
    global INKY_DELTA_X 
    global INKY_DELTA_Y 
    global PINKY_DELTA_X 
    global PINKY_DELTA_Y
    global INKY_HOUSE
    global BLINKY_HOUSE
    global PINKY_HOUSE
    global CLYDE_HOUSE
    global EATEN_COUNTER
    global Node_Blinky
    global Node_Clyde
    global Node_Inky
    global Node_Pinky

     #if the time is under 7 seconds, between 27-34 seconds, 54-59 seconds or 120-124 seconds, 
    seconds = int(TIMER/60)
    if POWER_UP == False:
        FRIGHTENED = False
        BLINKY_FRIGHTENED = False
        CLYDE_FRIGHTENED = False
        INKY_FRIGHTENED  = False
        PINKY_FRIGHTENED = False
        GHOST_SPEED = 1
        #if time is under 16 seconds between 36 and 43, between 53 and 68, or 129 and 133
        if (seconds < 16) or (36 < seconds < 43) or (53 < seconds < 68) or (129 < seconds < 133):
            if SCATTER == False:
                #if we are starting a scatter, check huntables, and that we are not already eaten
                if Eaten_Blinky == False:
                    node = True
                    fright = True
                    d_x = BLINKY_DELTA_X = BLINKY_DELTA_X * -1
                    d_y = BLINKY_DELTA_Y = BLINKY_DELTA_Y * -1
                    Node_Blinky = False
                    ghost = blinky
                    hunt = huntable_zone(d_x,d_y,ghost)
                    if  hunt == 4:
                        ghost, BLINKY_DELTA_X, BLINKY_DELTA_Y, node = ghost_node_vectoring(ghost,d_x,d_y,0,0,node,fright)
                if Eaten_Clyde == False:
                    d_x = CLYDE_DELTA_X = CLYDE_DELTA_X * -1
                    d_y = CLYDE_DELTA_Y = CLYDE_DELTA_Y * -1
                    Node_Clyde = False
                    ghost = clyde
                    hunt = huntable_zone(d_x,d_y,ghost)
                    if  hunt == 4:
                        ghost, CLYDE_DELTA_X, CLYDE_DELTA_Y, node = ghost_node_vectoring(ghost,d_x,d_y,0,0,node,fright)
                if Eaten_Inky == False:
                    d_x = INKY_DELTA_X = INKY_DELTA_X * -1
                    d_y = INKY_DELTA_Y = INKY_DELTA_Y * -1
                    Node_Inky = False
                    ghost = inky
                    hunt = huntable_zone(d_x,d_y,ghost)
                    if  hunt == 4:
                        ghost, INKY_DELTA_X, INKY_DELTA_Y, node = ghost_node_vectoring(ghost,d_x,d_y,0,0,node,fright)
                if Eaten_Pinky == False:
                    d_x = PINKY_DELTA_X = PINKY_DELTA_X * -1
                    d_y = PINKY_DELTA_Y = PINKY_DELTA_Y * -1 
                    Node_Pinky = False
                    ghost = pinky
                    hunt = huntable_zone(d_x,d_y,ghost)
                    if  hunt == 4:
                        ghost, PINKY_DELTA_X, PINKY_DELTA_Y, node = ghost_node_vectoring(ghost,d_x,d_y,0,0,node,fright)
            SCATTER = True
        else:
            SCATTER = False
    else:
        FRIGHTENED = True
        GHOST_SPEED = 0.5
        powered_time = int((TIMER- POWER_UP_TIMER)/60)
        if powered_time > 5:
            POWER_UP = False
            EATEN_COUNTER = 0
#similar to pacmans playable zone, just makes sure ghosts are at a valid space                  
def huntable_zone(d_x, d_y,ghost):
        #note i = Y and j = X
        huntable = 0
        view_distance = 18
        sprite_j = 0
        sprite_i = 0
        #center of sprite   
        sprite_center_x = (ghost.x + GHOST_WIDTH/2) -26
        sprite_center_y = (ghost.y + GHOST_HEIGHT/2) - 50
    # get I and J on tilesets for their current position
        current_i = int((sprite_center_y)/num2 * y_scaler) -1
        current_j = int((sprite_center_x)/num1 * x_scaler)
        next_i = current_i + d_y
        next_j = current_j + d_x
        after_i = current_i + d_y
        after_j = current_j + d_x 
    #convert viewed coordinates into I/J values
        viewed_i = int((((sprite_center_y + (d_y*view_distance))/num2 * y_scaler))) - 1
        viewed_j = int(((sprite_center_x + (d_x*view_distance))/num1 * x_scaler) )
        #if ghost move or looks past the middle flip my counter so I am counting down
        # flips the x axis for viewing and placement assessment
        if viewed_j > (len(GHOST_AREA[0])-2):
            viewed_j = viewed_j-(2*(viewed_j-13))+1
        if current_j > (len(GHOST_AREA[0])-2):
            current_j = current_j-(2*(current_j-13))+1
        if next_j > (len(GHOST_AREA[0])-2):
            next_j = next_j-(2*(next_j-13))+1
        if after_j > (len(GHOST_AREA[0])-2):
            after_j = after_j-(2*(after_j-13))+1
        #line for tunnel jump
        if (viewed_j<0 and viewed_i == 14):
                viewed_j = 0
                if (ghost.x < -GHOST_WIDTH) and (d_x == -1):
                    ghost.x = ghost.x + WIDTH + 60
                if (ghost.x > WIDTH + 15) and (d_x == 1):
                    ghost.x = ghost.x - WIDTH - 60
                return True
        #if i try and walk off either side the lower x bound movement is stopped
        if viewed_j < 0:
            viewed_j = 0
        #if i move to the top or bottom stop me from going further
        if (viewed_i < 0) or (viewed_i > (len(GHOST_AREA))):
            viewed_i = 0
        #scrubbing viewed_i, viewed_j, next_j and after_j for overflow
        if viewed_j < 0:
            viewed_j = 0
        if viewed_j > (len(GHOST_AREA[0])):
            viewed_j = len(GHOST_AREA[0])-1
        if viewed_i < 0:
            viewed_i = 0
        if viewed_i > (len(GHOST_AREA)-1):
            viewed_i = len(GHOST_AREA)-1
        if next_j < 0:
            next_j = 0
        if next_j > (len(GHOST_AREA[0])):
            next_j = len(GHOST_AREA[0])-1
        if after_j < 0:
            after_j = 0
        if after_j > (len(GHOST_AREA[0])):
            after_j = len(GHOST_AREA[0])-1
        
        viewed_tile = GHOST_AREA[viewed_i][viewed_j]
        current_tile = GHOST_AREA[current_i][current_j]
        next_tile = GHOST_AREA[next_i][next_j]
        after_tile = GHOST_AREA[after_i][after_j]
        
        #grabs the next to tiles if we are in a node and either are a wall this will stop bumping         
        next_tile = next_tile * after_tile
        
        #huntable 1 the next tile I can see is fine to move into and im not at an intersection
        #huntable 1 I am in a node but not centered and need to keep going
        #huntable 2 the next tile infront of me is a wall and I am not at an intersection
        #huntable 3 I am in a node and the next tile infront of me is open
        #huntable 4 I am in a node and the next tile infron of me is a wall
        
        #my next tile is open
        if viewed_tile == 1 or viewed_tile == 2:
            huntable = 1
        #my next tile is a wall
        if viewed_tile == 0:
            huntable = 2
        #if my current tile is a node
        if current_tile == 2:
            #and the tile i am looking at is not the one I am in, meaning I am centered in the node
            if viewed_tile != current_tile:
            #if the next tile is open
                if next_tile == 1:
                    huntable = 3
            #if the next tile or the one after it is a wall
                if next_tile == 0:
                    huntable = 4
            
            else:
                huntable = 1

        return huntable
#tells ghost which way to go when at a node with a choice
def ghost_node_vectoring (ghost, d_x, d_y , x, y, node,frightened):
            #store ghost starting directions
            starting_d_x = d_x 
            starting_d_y = d_y

            #huntable 1 the next tile I can see is fine to move into and im not at an intersection
            #huntable 1 I am in a node but not centered and need to keep going
            #huntable 2 the next tile infront of me is a wall and I am not at an intersection
            #huntable 3 I am in a node and the next tile infront of me is open
            #huntable 4 I am in a node and the next tile infron of me is a wall
            
            #find the best heading for each vector
            best_d_x = 0
            best_d_y = 0
            # if i am moving y, findthe best x
            if d_x == 0:
                if x < 0:
                    best_d_x = -1
                if x > 0:
                    best_d_x = 1
                if x == 0:
                    best_d_x = random.choice([1,-1])
            #if i am moving x find the best y 
            if d_y == 0:
                if y < 0:
                    best_d_y = -1
                if y > 0:
                    best_d_y = 1
                if y == 0:
                    best_d_y = random.choice([1,-1])
            if frightened:
                #if my heading was y, see which outputs are valic
                if starting_d_x == 0:
                    vectors = [1,0,-1]
                    shuffled_options = random.sample(vectors, 3)
                    for option in shuffled_options:
                        if shuffled_options == 0:
                            huntable = huntable_zone(0,starting_d_y,ghost)
                            if huntable == 1 or huntable == 3:
                                d_y = starting_d_y
                                d_x = 0
                                return ghost, d_x, d_y, node
                        if shuffled_options == 1:
                            huntable = huntable_zone(1,0,ghost)
                            if huntable == 1 or huntable == 3:
                                d_y = 0
                                d_x = 1
                                return ghost, d_x, d_y, node
                        if shuffled_options == -1:
                            huntable = huntable_zone(1,0,ghost)
                            if huntable == 1 or huntable == 3:
                                d_y = 0
                                d_x = -1
                                return ghost, d_x, d_y, node     

                if starting_d_y == 0:
                    vectors = [1,0,-1]
                    shuffled_options = random.sample(vectors, 3)
                    for option in shuffled_options:
                        if shuffled_options == 0:
                            huntable = huntable_zone(starting_d_x,0,ghost)
                            if huntable == 1 or huntable == 3:
                                d_x = starting_d_x
                                d_y = 0
                                return ghost, d_x, d_y, node
                        if shuffled_options == 1:
                            huntable = huntable_zone(0,1,ghost)
                            if huntable == 1 or huntable == 3:
                                d_x = 0
                                d_y = 1
                                return ghost, d_x, d_y, node
                        if shuffled_options == -1:
                            huntable = huntable_zone(0,-1,ghost)
                            if huntable == 1 or huntable == 3:
                                d_x = 0
                                d_y = -1
                                return ghost, d_x, d_y, node
            
            if starting_d_x == 0:
                #if i was moving y, y is still greater, and it is huntable, keep going
                huntable = huntable_zone(0,starting_d_y,ghost)
                if abs(y)>abs(x) and huntable == 3 and y * starting_d_y > 0:
                    d_y = starting_d_y
                    d_x = 0
                    return ghost, d_x, d_y, node
                #BUT if i was moving y, and x is greater, check if that is huntable
                huntable = huntable_zone(best_d_x,0,ghost)
                if huntable == 3 or huntable == 1:
                    d_y = 0
                    d_x = best_d_x
                    return ghost, d_x, d_y, node
                if huntable == 4:
                    d_y = 0
                    d_x = best_d_x * -1
                    return ghost, d_x, d_y, node
            
            if starting_d_y == 0:
                #if i was moving x, x is still greater, huntable, and doesn't have me moving away keep going
                huntable = huntable_zone(starting_d_x,0,ghost)
                if abs(x)>abs(y) and huntable == 3 and x * starting_d_x > 0:
                    d_x = starting_d_x
                    d_y = 0
                    return ghost, d_x, d_y, node
                if huntable == 1:
                    d_x = starting_d_x
                    d_y = 0
                    return ghost, d_x, d_y, node
                #BUT if i was moving x, moving x would put me further away into a wall or y is greater check if that is huntable
                huntable = huntable_zone(0,best_d_y,ghost)
                if huntable == 3 or huntable == 1:
                    d_x = 0
                    d_y = best_d_y
                    return ghost, d_x, d_y, node
                if huntable == 4:
                    d_x = 0
                    d_y = best_d_y * -1
                    return ghost, d_x, d_y, node

def blinky_movement(blinky,pacman):
        #Declaring vector variables
        huntable = 0
        #ghost vector varibales
        global BLINKY_DELTA_X
        global BLINKY_DELTA_Y      
        #ghost node bools
        global Node_Blinky
        #ghost eaten bool
        global Eaten_Blinky
        global BLINKY_HOUSE
        global BLINKY_FRIGHTENED
        global Blinky_Body
        global Blinky_Eyes
        #choosing blinky to assess
        d_x = BLINKY_DELTA_X
        d_y = BLINKY_DELTA_Y
        #center blinky
        sprite = blinky
        ghost_center(sprite,d_x,d_y)
        eaten = Eaten_Blinky
        frightened = BLINKY_FRIGHTENED               
        if eaten == False:
            Eaten_Blinky, BLINKY_FRIGHTENED = pacman_contact(sprite,pacman,eaten,frightened)
        else:
            BLINKY_FRIGHTENED = False
        #define zone as huntable or node
        huntable = huntable_zone(d_x,d_y,blinky)
        
        #huntable 1 the next tile I can see is fine to move into and im not at an intersection
        #huntable 1 I am in a node but not centered and need to keep going
        #huntable 2 the next tile i can see infront of me is a wall and I am not at an intersection
        #huntable 3 I am in a node and the next tile infront of me is open
        #huntable 4 I am in a node and the next tile infron of me is a wall
        if huntable < 3:
            Node_Blinky = False
        if huntable > 2:
            d_x, d_y, Node_blinky = blinky_AI(blinky,pacman,d_x,d_y,Node_Blinky)
            huntable = huntable_zone(d_x,d_y,blinky)
        #I am at a wall that is not also a node
        if huntable == 2:
            #if the ghost was moving up/down, look right
            if d_y != 0:            
                d_y = 0
                d_x = 1
                huntable = huntable_zone(d_x,d_y,blinky)
                #if we cannot go right, go left
                if huntable == 2:
                    d_x = -1
            #if the ghost was moving left/right, look down
            else:
                d_x = 0
                d_y = 1
                huntable = huntable_zone(d_x,d_y,blinky)
                #if we cannot go down, go up
                if huntable == 2:
                    d_y = -1
            BLINKY_DELTA_X = d_x
            BLINKY_DELTA_Y = d_y 
        #check to insure the area I am moving into is open or moving me into the center of a node
        huntable = huntable_zone(d_x,d_y,blinky)
        if BLINKY_HOUSE:
            if (WIDTH/2 -4) < blinky.x < (WIDTH/2 + 4):
                d_x = 0
                d_y = 0
                if Eaten_Blinky:
                    Eaten_Blinky, BLINKY_FRIGHTENED, d_x,d_y = enter_ghost_house(blinky,d_x,d_y)
            if Eaten_Blinky == False:
                BLINKY_HOUSE, d_x, d_y = leave_ghost_house(blinky,pacman,d_x,d_y)
        if huntable < 4 or (Eaten_Blinky == False and BLINKY_HOUSE == True):
            velx = ((VEL * d_x) * GHOST_SPEED)
            vely = ((VEL * d_y) * GHOST_SPEED)
            if POWER_UP and BLINKY_FRIGHTENED == False:
                velx = velx * 2
                vely = vely * 2
            if Eaten_Blinky:
                velx = velx * EATEN_MULTIPLIER
                vely = vely * EATEN_MULTIPLIER
            blinky.x = (blinky.x + velx)
            blinky.y = (blinky.y + vely)
        BLINKY_DELTA_X = d_x
        BLINKY_DELTA_Y = d_y
        #Pic Blinky Body
        #pick default ghost image 1 or two based on time
        seconds = int(TIMER/60)
        sprite_flip = int(seconds/7)
        sprite_flip = int(sprite_flip%2)
        #pick eye direction based on d_x/d_y
        if sprite_flip == 1:
            Blinky_Body = Blinky_Image_1
        else:
            Blinky_Body = Blinky_Image_2
        if BLINKY_DELTA_X == 0:
            if BLINKY_DELTA_Y == 1:
                Blinky_Eyes = Ghost_Eyes_Down
            else:
                Blinky_Eyes = Ghost_Eyes_Up
        else:
            if BLINKY_DELTA_X == 1:
                Blinky_Eyes = Ghost_Eyes_Right
            else:
                Blinky_Eyes = Ghost_Eyes_Left
        #if powerup scared
        if POWER_UP and Eaten_Blinky == False and BLINKY_FRIGHTENED == True:
            Blinky_Eyes = Eaten_Image
            powered_time = int((TIMER- POWER_UP_TIMER)/60)
            #blue image until a few seconds have passed
            if int(TIMER- POWER_UP_TIMER)/60 < 4: 
                if sprite_flip == 1:
                    Blinky_Body = Frightened_Image_1
                else:
                    Blinky_Body = Frightened_Image_2
            #if powerup is running low, flip between white and blue
            if int(TIMER- POWER_UP_TIMER)/30 > 6:
                time = int((TIMER - POWER_UP_TIMER)/20)
                if time%2 == 0:
                    if sprite_flip == 1:
                        Blinky_Body = Frightened_Image_3
                    else:
                        Blinky_Body = Frightened_Image_4
                else:
                    if sprite_flip == 1:
                        Blinky_Body = Frightened_Image_1
                    else:
                        Blinky_Body = Frightened_Image_2
        if Eaten_Blinky:
            Blinky_Body = Eaten_Image
        
        #scale up eye and body image
        Blinky_Body = pygame.transform.scale(Blinky_Body,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))
        Blinky_Eyes = pygame.transform.scale(Blinky_Eyes,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))

def blinky_AI(blinky,pacman,d_x,d_y,node_count):
            global BLINKY_DELTA_X
            global BLINKY_DELTA_Y
            global Node_Blinky
            global Eaten_Blinky
            global BLINKY_HOUSE
            global BLINKY_FRIGHTENED
            if Node_Blinky:
                return d_x,d_y,Node_Blinky
            node = Node_Blinky
            #Declare local variables
            num1 = (HEIGHT//38)
            num2 = (WIDTH//14.5)
            d_x = d_x
            d_y = d_y
            #center of pacman sprite   
            pacman_center_x = (pacman.x + PACMAN_WIDTH/2) + x_offset
            pacman_center_y = (pacman.y + PACMAN_HEIGHT/2) + y_offset
            # get pacman I and J on tilesets for their current position
            pacman_i = int((pacman_center_y)/num2 * y_scaler)
            pacman_j = int((pacman_center_x)/num1 * x_scaler) 

            #get ghost i(y) and j(x) location
            #center of sprite      
            sprite_center_x = (blinky.x + GHOST_WIDTH/2) + x_offset
            sprite_center_y = (blinky.y + GHOST_HEIGHT/2) + y_offset
            # get I and J on tilesets for their current position
            ghost_i = int((sprite_center_y)/num2 * y_scaler) -1
            ghost_j = int((sprite_center_x)/num1 * x_scaler) 

            #if scatter is active target is -3y, 25x
            if SCATTER:
                pacman_i = -5
                pacman_j = 26
            
            if Eaten_Blinky:
                pacman_i = 11
                pacman_j = 14
                if ghost_i == pacman_i and (pacman_j + 3 > ghost_j > pacman_j - 3):
                    BLINKY_HOUSE = True

            #find the vector from Blinky to pacman
            y = pacman_i - ghost_i
            x = pacman_j - ghost_j
            
            ghost = blinky
            frightened = BLINKY_FRIGHTENED
            ghost, d_x, d_y, node = ghost_node_vectoring (ghost, d_x, d_y, x, y,node, frightened)
            Node_Blinky = True
            return d_x, d_y,Node_Blinky

def clyde_movement(clyde,pacman):
        #Declaring vector variables
        huntable = 0
        #ghost vector varibales
        global CLYDE_DELTA_X
        global CLYDE_DELTA_Y      
        #ghost node bools
        global Node_Clyde
        global Eaten_Clyde
        global CLYDE_HOUSE
        global CLYDE_FRIGHTENED
        #clyde images
        global Clyde_Body
        global Clyde_Eyes
        #choosing Clyde to assess
        d_x = CLYDE_DELTA_X
        d_y = CLYDE_DELTA_Y
        #center clyde
        sprite = clyde
        ghost_center(sprite,d_x,d_y)        
        eaten = Eaten_Clyde
        player_death = PLAYER_DEATH
        frightened = CLYDE_FRIGHTENED
        if eaten == False:
            Eaten_Clyde, CLYDE_FRIGHTENED = pacman_contact(sprite,pacman,eaten,frightened)
        else:
            CLYDE_FRIGHTENED = False     
        #define zone as huntable or node
        huntable = huntable_zone(d_x,d_y,clyde)
        
        #huntable 1 the next tile I can see is fine to move into and im not at an intersection
        #huntable 1 I am in a node but not centered and need to keep going
        #huntable 2 the next tile i can see infront of me is a wall and I am not at an intersection
        #huntable 3 I am in a node and the next tile infront of me is open
        #huntable 4 I am in a node and the next tile infron of me is a wall
        if huntable < 3:
            Node_Clyde = False
        if huntable > 2:
            d_x, d_y, Node_Clyde = clyde_AI(clyde,pacman,d_x,d_y,Node_Clyde)
            huntable = huntable_zone(d_x,d_y,clyde)
        #I am at a wall that is not also a node
        if huntable == 2:
            #if the ghost was moving up/down, look right
            if d_y != 0:            
                d_y = 0
                d_x = 1
                huntable = huntable_zone(d_x,d_y,clyde)
                #if we cannot go right, go left
                if huntable == 2:
                    d_x = -1
            #if the ghost was moving left/right, look down
            else:
                d_x = 0
                d_y = 1
                huntable = huntable_zone(d_x,d_y,clyde)
                #if we cannot go down, go up
                if huntable == 2:
                    d_y = -1
            CLYDE_DELTA_X = d_x
            CLYDE_DELTA_Y = d_y 
        #check to insure the area I am moving into is open or moving me into the center of a node
        huntable = huntable_zone(d_x,d_y,clyde)
        #roundstart is set so at game start clyde leaves at 9 seconds
        frightened = CLYDE_FRIGHTENED
        if CLYDE_HOUSE and ((TIMER - ROUND_START)/60> 5):
            if (WIDTH/2 -4) < clyde.x < (WIDTH/2 + 4):
                d_x = 0
                d_y = 0
                if Eaten_Clyde:
                    Eaten_Clyde, frightened, d_x,d_y = enter_ghost_house(clyde,d_x,d_y)
            if Eaten_Clyde == False:
                CLYDE_HOUSE, d_x, d_y = leave_ghost_house(clyde,pacman,d_x,d_y)
        CLYDE_FRIGHTENED = frightened
        if CLYDE_HOUSE == True and ((TIMER - ROUND_START)/60< 5):
            offset = 15
            bounce_in_ghost_house(clyde,offset)
        if huntable < 4 or (Eaten_Clyde == False and CLYDE_HOUSE == True):
            velx = ((VEL * d_x) * GHOST_SPEED)
            vely = ((VEL * d_y) * GHOST_SPEED)
            #if powerup is active, take an extra step to move normal
            if POWER_UP and frightened == False:
                velx = velx * 2
                vely = vely * 2
            if Eaten_Clyde:
                velx = velx * EATEN_MULTIPLIER
                vely = vely * EATEN_MULTIPLIER
            clyde.x = (clyde.x + velx)
            clyde.y = (clyde.y + vely)
        CLYDE_DELTA_X = d_x
        CLYDE_DELTA_Y = d_y
        
                #Pic inky Body
        #pick default ghost image 1 or two based on time
        seconds = int(TIMER/60)
        sprite_flip = int(seconds/7)
        sprite_flip = int(sprite_flip%2)
        #pick eye direction based on d_x/d_y
        if sprite_flip == 1:
            Clyde_Body = Clyde_Image_1
        else:
            Clyde_Body = Clyde_Image_2
        if CLYDE_DELTA_X == 0:
            if CLYDE_DELTA_Y == 1:
                Clyde_Eyes = Ghost_Eyes_Down
            else:
                Clyde_Eyes = Ghost_Eyes_Up
        else:
            if CLYDE_DELTA_X == 1:
                Clyde_Eyes = Ghost_Eyes_Right
            else:
                Clyde_Eyes = Ghost_Eyes_Left
        #if powerup scared
        if POWER_UP and Eaten_Clyde == False and frightened == True:
            Clyde_Eyes = Eaten_Image
            powered_time = int((TIMER- POWER_UP_TIMER)/60)
            #blue image until a few seconds have passed
            if int(TIMER- POWER_UP_TIMER)/60 < 4: 
                if sprite_flip == 1:
                    Clyde_Body = Frightened_Image_1
                else:
                    Clyde_Body = Frightened_Image_2
            #if powerup is running low, flip between white and blue
            if int(TIMER- POWER_UP_TIMER)/30 > 6:
                time = int((TIMER - POWER_UP_TIMER)/20)
                if time%2 == 0:
                    if sprite_flip == 1:
                        Clyde_Body = Frightened_Image_3
                    else:
                        Clyde_Body = Frightened_Image_4
                else:
                    if sprite_flip == 1:
                        Clyde_Body = Frightened_Image_1
                    else:
                        Clyde_Body = Frightened_Image_2
            
        if Eaten_Clyde:
            Clyde_Body = Eaten_Image
        #scale up eye and body image
        Clyde_Body = pygame.transform.scale(Clyde_Body,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))
        Clyde_Eyes = pygame.transform.scale(Clyde_Eyes,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))

def clyde_AI(clyde,pacman,d_x,d_y,node_count):
            global CLYDE_DELTA_X
            global CLYDE_DELTA_Y
            global Node_Clyde
            global Eaten_Clyde
            global CLYDE_HOUSE
            global CLYDE_FRIGHTENED
            ghost = clyde
            if Node_Clyde:
                return d_x,d_y,Node_Clyde
            node = Node_Clyde
            #Declare local variables
            num1 = (HEIGHT//38)
            num2 = (WIDTH//14.5)
            d_x = d_x
            d_y = d_y
            #center of pacman sprite   
            pacman_center_x = (pacman.x + PACMAN_WIDTH/2) + x_offset
            pacman_center_y = (pacman.y + PACMAN_HEIGHT/2) + y_offset
            # get pacman I and J on tilesets for their current position
            pacman_i = int((pacman_center_y)/num2 * y_scaler)
            pacman_j = int((pacman_center_x)/num1 * x_scaler) 

            #get ghost i(y) and j(x) location
            #center of sprite      
            sprite_center_x = (clyde.x + GHOST_WIDTH/2) + x_offset
            sprite_center_y = (clyde.y + GHOST_HEIGHT/2) + y_offset
            # get I and J on tilesets for their current position
            ghost_i = int((sprite_center_y)/num2 * y_scaler) -1
            ghost_j = int((sprite_center_x)/num1 * x_scaler) 
            
            #finds hypotenuse squared to pacman dont bother with sqrt because we just need to know if
            #the hypotenuse is less than 8 or 8^2 or 64
            #vector to pacman
            y = pacman_i - ghost_i
            x = pacman_j - ghost_j
            distance_to_pacman = (x*x)+(y*y)
            if distance_to_pacman < 64 or SCATTER:
                #if too close to pacman or scatter is active, our target position is our scatter point
                pacman_i = 32
                pacman_j = -6
                y = pacman_i - ghost_i
                x = pacman_j - ghost_j
            if Eaten_Clyde:
                pacman_i = 11
                pacman_j = 14
                y = pacman_i - ghost_i
                x = pacman_j - ghost_j
                if ghost_i == pacman_i and (pacman_j + 3 > ghost_j > pacman_j - 3):
                    CLYDE_HOUSE = True

            #find the vector from Clyde to pacman
            frightened = CLYDE_FRIGHTENED
            ghost, d_x, d_y, node = ghost_node_vectoring (ghost, d_x, d_y, x, y,node,frightened)
            Node_Clyde = True
            return d_x, d_y,Node_Clyde

def pinky_movement(pinky,pacman):
        #Declaring vector variables
        huntable = 0
        #ghost vector varibales
        global PINKY_DELTA_X
        global PINKY_DELTA_Y      
        #ghost node bools
        global Node_Pinky
        global Eaten_Pinky
        global PINKY_HOUSE
        global PINKY_FRIGHTENED
        #pinky images
        global Pinky_Body
        global Pinky_Eyes
        #choosing blinky to assess
        d_x = PINKY_DELTA_X
        d_y = PINKY_DELTA_Y
        #center pinky
        sprite = pinky
        ghost_center(sprite,d_x,d_y)
        eaten = Eaten_Pinky
        frightened = PINKY_FRIGHTENED
        if eaten == False:
            Eaten_Pinky, PINKY_FRIGHTENED = pacman_contact(sprite,pacman,eaten,frightened)
        else:
            PINKY_FRIGHTENED = False
        #define zone as huntable or node
        huntable = huntable_zone(d_x,d_y,pinky)
        
        #huntable 1 the next tile I can see is fine to move into and im not at an intersection
        #huntable 1 I am in a node but not centered and need to keep going
        #huntable 2 the next tile i can see infront of me is a wall and I am not at an intersection
        #huntable 3 I am in a node and the next tile infront of me is open
        #huntable 4 I am in a node and the next tile infron of me is a wall
        if huntable < 3:
            Node_Pinky = False
        if huntable > 2:
            d_x, d_y, Node_Pinky = pinky_AI(pinky,pacman,d_x,d_y,Node_Pinky)
            huntable = huntable_zone(d_x,d_y,pinky)
        #I am at a wall that is not also a node
        if huntable == 2:
            #if the ghost was moving up/down, look right
            if d_y != 0:            
                d_y = 0
                d_x = 1
                huntable = huntable_zone(d_x,d_y,pinky)
                #if we cannot go right, go left
                if huntable == 2:
                    d_x = -1
            #if the ghost was moving left/right, look down
            else:
                d_x = 0
                d_y = 1
                huntable = huntable_zone(d_x,d_y,pinky)
                #if we cannot go down, go up
                if huntable == 2:
                    d_y = -1
            PINKY_DELTA_X = d_x
            PINKY_DELTA_Y = d_y 
        #check to insure the area I am moving into is open or moving me into the center of a node
        huntable = huntable_zone(d_x,d_y,pinky)
        frightened = PINKY_FRIGHTENED
        #initial round start is set so at start of game pinky leaves at 7
        if PINKY_HOUSE and ((TIMER - ROUND_START)/60> 3):
            if (WIDTH/2 -4) < pinky.x < (WIDTH/2 + 4):
                d_x = 0
                d_y = 0
                if Eaten_Pinky:
                    Eaten_Pinky, frightened, d_x,d_y = enter_ghost_house(pinky,d_x,d_y)
            if Eaten_Pinky == False:
                PINKY_HOUSE, d_x, d_y = leave_ghost_house(pinky,pacman,d_x,d_y)
        PINKY_FRIGHTENED = frightened
        if PINKY_HOUSE == True and ((TIMER - ROUND_START)/60< 3):
            offset = 0
            bounce_in_ghost_house(pinky,offset)
        if huntable < 4 or (Eaten_Pinky == False and PINKY_HOUSE == True):
            velx = ((VEL * d_x) * GHOST_SPEED)
            vely = ((VEL * d_y) * GHOST_SPEED)
            if POWER_UP and frightened == False:
                velx = velx * 2
                vely = vely * 2
            if Eaten_Pinky:
                velx = velx * EATEN_MULTIPLIER
                vely = vely * EATEN_MULTIPLIER
            pinky.x = (pinky.x + velx)
            pinky.y = (pinky.y + vely)
        PINKY_DELTA_X = d_x
        PINKY_DELTA_Y = d_y
        PINKY_FRIGHTENED = frightened
        #Pick Pinky Body
        #pick default ghost image 1 or two based on time
        seconds = int(TIMER/60)
        sprite_flip = int(seconds/7)
        sprite_flip = int(sprite_flip%2)
        #pick eye direction based on d_x/d_y
        if sprite_flip == 1:
            Pinky_Body = Pinky_Image_1
        else:
            Pinky_Body = Pinky_Image_2
        if PINKY_DELTA_X == 0:
            if PINKY_DELTA_Y == 1:
                Pinky_Eyes = Ghost_Eyes_Down
            else:
                Pinky_Eyes = Ghost_Eyes_Up
        else:
            if PINKY_DELTA_X == 1:
                Pinky_Eyes = Ghost_Eyes_Right
            else:
                Pinky_Eyes = Ghost_Eyes_Left
        #if powerup scared
        if POWER_UP and Eaten_Pinky == False and frightened:
            Pinky_Eyes = Eaten_Image
            powered_time = int((TIMER- POWER_UP_TIMER)/60)
            #blue image until a few seconds have passed
            if int(TIMER- POWER_UP_TIMER)/60 < 4: 
                if sprite_flip == 1:
                    Pinky_Body = Frightened_Image_1
                else:
                    Pinky_Body = Frightened_Image_2
            #if powerup is running low, flip between white and blue
            if int(TIMER- POWER_UP_TIMER)/30 > 6:
                time = int((TIMER - POWER_UP_TIMER)/20)
                if time%2 == 0:
                    if sprite_flip == 1:
                        Pinky_Body = Frightened_Image_3
                    else:
                        Pinky_Body = Frightened_Image_4
                else:
                    if sprite_flip == 1:
                        Pinky_Body = Frightened_Image_1
                    else:
                        Pinky_Body = Frightened_Image_2
        if Eaten_Pinky:
            Pinky_Body = Eaten_Image

        #scale up eye and body image
        Pinky_Body = pygame.transform.scale(Pinky_Body,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))
        Pinky_Eyes = pygame.transform.scale(Pinky_Eyes,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))

def pinky_AI(pinky,pacman,d_x,d_y,node_count):
            global PINKY_DELTA_X
            global PINKY_DELTA_Y
            global Node_Pinky
            global Eaten_Pinky
            global PINKY_HOUSE
            global PINKY_FRIGHTENED
            if Node_Pinky:
                return d_x,d_y,Node_Pinky
            node = Node_Pinky
            #Declare local variables
            num1 = (HEIGHT//38)
            num2 = (WIDTH//14.5)
            d_x = d_x
            d_y = d_y
            #center of pacman sprite   
            pacman_center_x = (pacman.x + PACMAN_WIDTH/2) + x_offset
            pacman_center_y = (pacman.y + PACMAN_HEIGHT/2) + y_offset
            # get pacman I and J on tilesets for their current position
            pacman_i = int((pacman_center_y)/num2 * y_scaler)
            pacman_j = int((pacman_center_x)/num1 * x_scaler) 

            #if scatter is active target is -3y,2x
            if SCATTER:
                 pacman_i = -3
                 pacman_j = -3
            #get ghost i(y) and j(x) location
            
            #center of sprite      
            sprite_center_x = (pinky.x + GHOST_WIDTH/2) + x_offset
            sprite_center_y = (pinky.y + GHOST_HEIGHT/2) + y_offset
            # get I and J on tilesets for their current position
            ghost_i = int((sprite_center_y)/num2 * y_scaler) -1
            ghost_j = int((sprite_center_x)/num1 * x_scaler) 

            #find the find the spot four spaces infront of pacman
            y = (pacman_i + (4*PACMAN_DELTA_Y)) - ghost_i
            x = (pacman_j +(4*PACMAN_DELTA_X))- ghost_j
            if SCATTER:
                 pacman_i = -3
                 pacman_j = -3
                 y = pacman_i - ghost_i
                 x = pacman_j - ghost_j
            if Eaten_Pinky:
                pacman_i = 11
                pacman_j = 14
                y = pacman_i - ghost_i
                x = pacman_j - ghost_j
                if ghost_i == pacman_i and (pacman_j + 3 > ghost_j > pacman_j - 3):
                    PINKY_HOUSE = True
            ghost = pinky
            frightened = PINKY_FRIGHTENED
            ghost, d_x, d_y, node = ghost_node_vectoring (ghost, d_x, d_y, x, y,node,frightened)
            Node_Pinky = True
            return d_x, d_y,Node_Pinky

def inky_movement(inky,pacman,blinky):
        #Declaring vector variables
        huntable = 0
        #ghost vector varibales
        global INKY_DELTA_X
        global INKY_DELTA_Y      
        #ghost node bools
        global Node_Inky
        global Eaten_Inky
        global INKY_HOUSE
        global INKY_FRIGHTENED
        #inky images
        global Inky_Body
        global Inky_Eyes
        #choosing blinky to assess
        d_x = INKY_DELTA_X
        d_y = INKY_DELTA_Y
        #center inky
        sprite = inky
        ghost_center(sprite,d_x,d_y)
        eaten = Eaten_Inky
        frightened = INKY_FRIGHTENED
        if eaten == False:
            Eaten_Inky, INKY_FRIGHTENED = pacman_contact(sprite,pacman,eaten,frightened)
        else:
            INKY_FRIGHTENED = False
        #define zone as huntable or node
        huntable = huntable_zone(d_x,d_y,inky)
        node = Node_Inky
        #huntable 1 the next tile I can see is fine to move into and im not at an intersection
        #huntable 1 I am in a node but not centered and need to keep going
        #huntable 2 the next tile i can see infront of me is a wall and I am not at an intersection
        #huntable 3 I am in a node and the next tile infront of me is open
        #huntable 4 I am in a node and the next tile infron of me is a wall
        if huntable < 2:
            Node_Inky = False
        if huntable > 2:
            d_x, d_y, Node_Inky = inky_AI(blinky,inky,pacman,d_x,d_y,node)
            huntable = huntable_zone(d_x,d_y,inky)
        #I am at a wall that is not also a node
        if huntable == 2:
            #if the ghost was moving up/down, look right
            if d_y != 0:            
                d_y = 0
                d_x = 1
                huntable = huntable_zone(d_x,d_y,inky)
                #if we cannot go right, go left
                if huntable == 2:
                    d_x = -1
            #if the ghost was moving left/right, look down
            else:
                d_x = 0
                d_y = 1
                huntable = huntable_zone(d_x,d_y,inky)
                #if we cannot go down, go up
                if huntable == 2:
                    d_y = -1
            INKY_DELTA_X = d_x
            INKY_DELTA_Y = d_y 
        #check to insure the area I am moving into is open or moving me into the center of a node
        huntable = huntable_zone(d_x,d_y,inky)
        #initial round start is set so inky leaves at 5 seconds
        if INKY_HOUSE and ((TIMER - ROUND_START)/60> 1):
            #inky is centered over the house and needs to go in
            if (WIDTH/2 -4) < inky.x < (WIDTH/2 + 4):
                d_x = 0
                d_y = 0
                if Eaten_Inky:
                    Eaten_Inky, INKY_FRIGHTENED , d_x,d_y = enter_ghost_house(inky,d_x,d_y)
            #innky is in the house and now needs to leave
            if Eaten_Inky == False:
                INKY_HOUSE, d_x, d_y = leave_ghost_house(inky,pacman,d_x,d_y)
        frightened = INKY_FRIGHTENED
        if INKY_HOUSE == True and ((TIMER - ROUND_START)/60< 1) :
            offset = 0
            bounce_in_ghost_house(inky,offset)
        if huntable < 4 or (Eaten_Inky == False and INKY_HOUSE == True):
            velx = ((VEL * d_x) * GHOST_SPEED)
            vely = ((VEL * d_y) * GHOST_SPEED)
            if POWER_UP and frightened == False:
                velx = velx * 2
                vely = vely * 2
            if Eaten_Inky:
                velx = velx * EATEN_MULTIPLIER
                vely = vely * EATEN_MULTIPLIER
            inky.x = (inky.x + velx)
            inky.y = (inky.y + vely)
        INKY_DELTA_X = d_x
        INKY_DELTA_Y = d_y

        #Pic inky Body
        #pick default ghost image 1 or two based on time
        seconds = int(TIMER/60)
        sprite_flip = int(seconds/7)
        sprite_flip = int(sprite_flip%2)
        #pick eye direction based on d_x/d_y
        if sprite_flip == 1:
            Inky_Body = Inky_Image_1
        else:
            Inky_Body = Inky_Image_2
        if INKY_DELTA_X == 0:
            if INKY_DELTA_Y == 1:
                Inky_Eyes = Ghost_Eyes_Down
            else:
                Inky_Eyes = Ghost_Eyes_Up
        else:
            if INKY_DELTA_X == 1:
                Inky_Eyes = Ghost_Eyes_Right
            else:
                Inky_Eyes = Ghost_Eyes_Left
        #if powerup scared
        if POWER_UP and Eaten_Inky == False and frightened == True:
            Inky_Eyes = Eaten_Image
            powered_time = int((TIMER- POWER_UP_TIMER)/60)
            #blue image until a few seconds have passed
            if int(TIMER- POWER_UP_TIMER)/60 < 4: 
                if sprite_flip == 1:
                    Inky_Body = Frightened_Image_1
                else:
                    Inky_Body = Frightened_Image_2
            #if powerup is running low, flip between white and blue
            if int(TIMER- POWER_UP_TIMER)/30 > 6:
                time = int((TIMER - POWER_UP_TIMER)/20)
                if time%2 == 0:
                    if sprite_flip == 1:
                        Inky_Body = Frightened_Image_3
                    else:
                        Inky_Body = Frightened_Image_4
                else:
                    if sprite_flip == 1:
                        Inky_Body = Frightened_Image_1
                    else:
                        Inky_Body = Frightened_Image_2
        if Eaten_Inky:
            Inky_Body = Eaten_Image

        #scale up eye and body image
        Inky_Body = pygame.transform.scale(Inky_Body,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))
        Inky_Eyes = pygame.transform.scale(Inky_Eyes,(GHOST_SPRITE_HEIGHT,GHOST_SPRITE_WIDTH))

def inky_AI(blinky,inky,pacman,d_x,d_y,node):
            global INKY_DELTA_X
            global INKY_DELTA_Y
            global Node_Inky
            global Eaten_Inky
            global INKY_HOUSE
            global INKY_FRIGHTENED
            if Node_Inky:
                return d_x,d_y,Node_Inky
            node = Node_Inky
            #Declare local variables
            num1 = (HEIGHT//38)
            num2 = (WIDTH//14.5)
            d_x = d_x
            d_y = d_y
            #center of pacman sprite   
            pacman_center_x = (pacman.x + PACMAN_WIDTH/2) + x_offset
            pacman_center_y = (pacman.y + PACMAN_HEIGHT/2) + y_offset
            # get pacman I and J on tilesets for their current position
            pacman_i = int((pacman_center_y)/num2 * y_scaler)
            pacman_j = int((pacman_center_x)/num1 * x_scaler) 

            #get ghost i(y) and j(x) location
            #center of sprite      
            sprite_center_x = (blinky.x + GHOST_WIDTH/2) + x_offset
            sprite_center_y = (blinky.y + GHOST_HEIGHT/2) + y_offset
            # get I and J on tilesets for their current position
            ghost_i = int((sprite_center_y)/num2 * y_scaler) -1
            ghost_j = int((sprite_center_x)/num1 * x_scaler) 

            #find the vector from Blinky to pacman
            y = pacman_i - ghost_i
            x = pacman_j - ghost_j
            #double the vector
            y = pacman_i + y
            x = pacman_j + x

            #get inky i(y) and j(x) location
            #center of sprite      
            sprite_center_x = (inky.x + GHOST_WIDTH/2) + x_offset
            sprite_center_y = (inky.y + GHOST_HEIGHT/2) + y_offset
            # get I and J on tilesets for their current position
            ghost_i = int((sprite_center_y)/num2 * y_scaler) -1
            ghost_j = int((sprite_center_x)/num1 * x_scaler) 

            #find inky vector to target location
            #if scatter is active target is bottom right
            if SCATTER:
                y = 32
                x = 32
            if Eaten_Inky:
                x = 13
                y = 11
                if ghost_i == y and (x + 3 > ghost_j > x - 3):
                    INKY_HOUSE = True
            y = y - ghost_i
            x = x - ghost_j
            ghost = inky
            frightened = INKY_FRIGHTENED
            ghost, d_x, d_y, node = ghost_node_vectoring (ghost, d_x, d_y, x, y,node, frightened)
            Node_Inky = True
            return d_x, d_y,Node_Inky 
    
def draw_window(inky,pinky,blinky,clyde,pacman,key_pressed,key_released):
    if GAME_START and game_over_menu_select == False:
        WINDOW.blit(Background_image,(IMAGE_OFFSET_X,IMAGE_OFFSET_Y))
        clear_dots(dots_left,dots_right,pacman)
        draw_dots(Dots)
        #Draw blinky and his eyes
        draw_ghosts(pacman,blinky,clyde,inky,pinky)
        #draw high score and 1up on screen
        draw_text("HIGH SCORE",text_font,WHITE,WIDTH/2,10,True)
        draw_text("1UP",text_font,WHITE,5,0,False)
        High_Score_string = str(HIGH_SCORE)
        draw_text(High_Score_string,text_font,WHITE,WIDTH/2,32,True)
        #draw current score
        Score_string = str(SCORE)
        draw_text(Score_string,text_font,WHITE,5,22,False)
        draw_lives()
        draw_fruit(pacman)
        WINDOW.blit(Pacman_image,(pacman.x -25, pacman.y + 5))
        show_scoring_event()
#### unsure if this if is needed
    if game_over_menu_select:
        game_over_menu(key_released)
        key_released = None
    if GAME_START == False:
        starting_menu(key_released,blinky,clyde,inky,pinky,pacman)
        key_released = None
    #toggle on and off to see playable area for an entity
    #visualize_area(Active_area)
    pygame.display.update()  

def main():
    pacman = pygame.Rect((PACMAN_STARTING_X, PACMAN_STARTING_Y, PACMAN_WIDTH, PACMAN_HEIGHT))
    blinky = pygame.Rect((BLINKY_START_X, BLINKY_START_Y, GHOST_WIDTH, GHOST_HEIGHT))
    pinky = pygame.Rect((PINKY_START_X, PINKY_START_Y, GHOST_WIDTH, GHOST_HEIGHT))
    inky = pygame.Rect((INKY_START_X, INKY_START_Y, GHOST_WIDTH, GHOST_HEIGHT))
    clyde = pygame.Rect((CLYDE_START_X, CLYDE_START_Y, GHOST_WIDTH, GHOST_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        
        clock.tick(FPS)
        key_released = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                #gives me the key number
                key_released = event.key
                a = pygame.key.key_code("return")
        key_pressed = pygame.key.get_pressed()
        mute_sounds(key_released)
        if GAME_START:   
            if PLAYER_LIVES > 0:
                pacman_movement(key_pressed,pacman)
                blinky_movement(blinky,pacman,)
                pinky_movement(pinky,pacman)
                inky_movement(inky,pacman,blinky)
                clyde_movement(clyde,pacman)
                scatter(TIMER,blinky,clyde,inky,pinky)
                level_up(pacman,blinky,clyde,inky,pinky)
                board_rest(pacman,blinky,clyde,inky,pinky)
                intro(pacman)
            if PLAYER_LIVES == 0 and game_over_menu_select == False:
                key_pressed = pygame.key.get_pressed()
                game_over(pacman,blinky,clyde,inky,pinky,key_pressed,key_released)
                board_rest(pacman,blinky,clyde,inky,pinky)
                key_released = None  
        draw_window(inky,pinky,blinky,clyde,pacman,key_pressed,key_released)    
    pygame.quit()

if __name__ == "__main__":
    main()