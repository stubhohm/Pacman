#Pacman

import pygame, sys

#general setup
pygame.init()
clock = pygame.time.Clock()

#Pacman Character Class
class Pacman(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        #pacman image         
        self.image = pygame.image.load("Sprites\Pacman\Pacman.png")
        self.rect = self.image.get_rect()
        starting_position_x = 210
        starting_position_y = 285
        self.pos_x = starting_position_x
        self.pos_y = starting_position_y
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
  

#Game Screen
screen_width = 448
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
background = pygame.image.load("Background\pacman-game.png")

#Pacman Group for sprite
#TODO find a way to cycle the sprites
pacman = Pacman(0,0,"Sprites\Pacman\Pacman.png")
pacman_group = pygame.sprite.Group()
pacman_group.add(pacman)

# TODO Add Dots



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        
    screen.blit(background,(-277,-60))
    pacman_group.draw(screen)
    pacman_group.update()
    
    screen.display.flip()
    clock.tick(60)
