"""
Sprint 1 - enemies, player, lasers. basic movement, basic background.
"""


import pygame
import sys

pygame.init()

#set up game variables
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
TICK_RATE = 60
run = True

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #self.laser = Bullet(0,0)
        
    def movement(self):
        keys = pygame.key.get_pressed()
        
    # Left and right movement
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-8,0)

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(8,0)
    

    def wall_prevention(self):
        if self.rect.left <= 0:
            #self.rect.left = (0, self.rect.y)
            self.rect.left = 0
        if self.rect.right >= WIDTH: 
            self.rect.right = WIDTH
            
    #laser being shot creates instance of bullet
    def shoot_laser(self):
        self.pos = self.rect.midtop
        self.laser = Bullet(self.pos[0],self.pos[1],bullet_surf)
        return self.laser

    def destruction(self):
        pass

    def update(self):
        self.movement()
        self.wall_prevention()
        self.shoot_laser()
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,bullet_surf):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_surf
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        #moves bullet up the screen, destroys when it goes outside screen
        self.rect.move_ip(0,-5)
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,enemy_surf):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surf
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):
        self.rect.move_ip(0,1)
        bullet_collision = pygame.sprite.spritecollide(self,bullet_grp, True)
        for enemy in bullet_collision:
            self.kill()
        player_collision = pygame.sprite.spritecollide(self,player_grp,False)
        if player_collision:
            print("col")
        
#set up surfaces
ship_surf = pygame.image.load('assets/spr_player.png').convert_alpha()
ship_surf = pygame.transform.scale_by(ship_surf,0.5)

bullet_surf = pygame.image.load('assets/laser.png')
bullet_surf = pygame.transform.scale_by(bullet_surf,0.5)
#bg = pygame.image.load('assets/bg.jpg')

enemy_surf = pygame.image.load('assets/spr_enemy.png').convert_alpha()

#bg = pygame.transform.scale2x(bg)

#create player ship
player = Player(WIDTH/2,HEIGHT-75,ship_surf)

#Set up groups
player_grp = pygame.sprite.Group()
player_grp.add(player)

enemy_grp = pygame.sprite.Group()

bullet_grp = pygame.sprite.Group()

#create positions for enemy placement
enemy_ship_coords = [(36, 23),(115, 22),(196, 26),(272, 25),(363, 23),(445, 31),(536, 30),(651, 29),(107, 82),(226, 90),
(331, 106),(410, 97),(510, 98),(601, 90),(682, 99)]

for i in enemy_ship_coords:    
    enemy = Enemy(i[0],i[1],enemy_surf)
    enemy_grp.add(enemy)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            #space key creates bullet
            if event.key == pygame.K_SPACE:
                #pos = player.rect.midtop
                #laser = Bullet(pos[0],pos[1])
                laser = player.shoot_laser()
                bullet_grp.add(laser)
        
        #creates enemy at point of mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #enemy = Enemy(pos[0],pos[1],enemy_surf)
            #enemy_grp.add(enemy)

            print(pos)
            
    
    #screen.blit(bg,(0,0))
    screen.fill("black")
    
    #player_grp.update()
    player_grp.draw(screen)
    player.update() #update includes movement

    enemy_grp.update()
    enemy_grp.draw(screen)

    bullet_grp.draw(screen)
    bullet_grp.update()
    
    pygame.display.update()
    clock.tick(TICK_RATE)