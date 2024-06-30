import pygame
import sys

pygame.init()

#set up game variables
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
TICK_RATE = 60
run = True
level = 0 #loading screen
start_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 - 100, 100,100)
level_start = True
enemy_vel = 1

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,player_surf):
        pygame.sprite.Sprite.__init__(self) #required so that Player is a pygame Sprite object.
        self.x = x
        self.y = y
        self.image = player_surf #surface that holds Player surface. needs to be called self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    def movement(self):
        keys = pygame.key.get_pressed()
        
        # Left and right movement
        # feature idea: tilt left and right?    
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-8,0)

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(8,0)
    

    def wall_prevention(self):
        #prevent player from leaving screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH: 
            self.rect.right = WIDTH
            
    #laser being shot creates instance of bullet
    def shoot_laser(self):
        self.pos = self.rect.midtop
        self.laser = Bullet(self.pos[0],self.pos[1],bullet_surf)
        return self.laser

    def destruction(self):
        #future code to handle if player is destroyed. currently handled through enemy class
        pass

    def update(self):
        self.movement()
        self.wall_prevention()
        

class Bullet(pygame.sprite.Sprite):
    #currently only for player, could be extended to include enemy bullets
    def __init__(self,x,y,bullet_surf):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_surf
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        #moves bullet up the screen, destroys when it goes outside screen
        self.rect.move_ip(0,-5) #literal should be replaced with variable
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    #creates enemy based on the surface passed in
    def __init__(self,x,y,enemy_surf, enemy_vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surf
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.enemy_vel = enemy_vel
    
    def update(self):
        #enemies move down at a constant speed
        self.rect.move_ip(0,self.enemy_vel)
        
        bullet_collision = pygame.sprite.spritecollide(self,bullet_grp, True) #list of enemy collisions with bullet
        for enemy in bullet_collision:
            self.kill()
            
        player_collision = pygame.sprite.spritecollide(self,player_grp,False) #list of enemy collisions with player
        if player_collision:
            #Future: add explosion animation
            print("col")

def level_control(level, level_start):
    if level == 0:
        #start menu
        #should be updated to include some text
        screen.fill("yellow")
        pygame.draw.rect(screen,pygame.Color("blue"),start_rect)
    else:    
        screen.fill("black")
        if level == 1:
            #screen.blit(bg,(0,0))
            if len(enemy_grp) == 0 and level_start == True:
                #spawns enemy ships
                add_enemy_ships(level, level1_enemy_surf, enemy_vel) 
                level_start = False
            
            if len(enemy_grp) == 0 and level_start == False: 
                #checks if we are out of enemies, then moves to next level
                level = 2
                bullet_grp.empty() #despawn any bullets still on screen
                level_start = True
            
        if level == 2:
            if len(enemy_grp) == 0 and level_start == True:
                add_enemy_ships(level, level2_enemy_surf, enemy_vel)
                level_start = False

            if len(enemy_grp) == 0 and level_start == False: #out of enemies
                print("game over")
                bullet_grp.empty() #despawn any bullets still on screen
                level = 3
        if level == 3:
            #game over screen, for now
            player_grp.empty()
            screen.fill("yellow")
            
            pygame.draw.rect(screen,pygame.Color("blue"),start_rect)

    return level, level_start

#function to add enemy ships to enemy group based on list of coordinates
def add_enemy_ships(level, enemy_surf, enemy_vel):
    enemy_list = enemy_ship_coords[level - 1] #level - 1 because level 0 is start menu
    for i in enemy_list:
        enemy = Enemy(i[0],i[1],enemy_surf, enemy_vel)
        enemy_grp.add(enemy)

#set up surfaces
player_surf = pygame.image.load('assets/spr_player.png').convert_alpha()
player_surf = pygame.transform.scale_by(player_surf,0.5)

bullet_surf = pygame.image.load('assets/laser.png')
bullet_surf = pygame.transform.scale_by(bullet_surf,0.5)
#bg = pygame.image.load('assets/bg.jpg')

level1_enemy_surf = pygame.image.load('assets/spr_enemy.png').convert_alpha()
level2_enemy_surf = pygame.image.load('assets/spr_enemy2.png').convert_alpha()
level2_enemy_surf = pygame.transform.scale_by(level2_enemy_surf,0.5) #would be better to have assets optimised beforehand


#create player ship
player = Player(WIDTH/2,HEIGHT-75,player_surf)

#Set up groups
player_grp = pygame.sprite.Group()
player_grp.add(player)

enemy_grp = pygame.sprite.Group()

bullet_grp = pygame.sprite.Group()

#create positions for enemy placement
level1_enemy_ship_coords = [(36, 23),(115, 22),(196, 26),(272, 25),(363, 23),(445, 31),(536, 30),(651, 29),(107, 82),(226, 90),
(331, 106),(410, 97),(510, 98),(601, 90),(682, 99)]

level2_enemy_ship_coords = [(36, 23),(115, 22),(196, 26),(272, 25),(363, 23),(445, 31),(536, 30),(651, 29),(107, 82),(226, 90),
(331, 106),(410, 97),(510, 98),(601, 90),(682, 99)] #identical to level 1, just demonstrating how this would work

enemy_ship_coords = [level1_enemy_ship_coords, level2_enemy_ship_coords] #list of enemy coordinates. keep adding as levels increase
"""
#old code for adding first level of enemies to group
for i in enemy_ship_coords:
    if len(enemy_grp) == 0:   
        for j in i:    
            enemy = Enemy(j[0],j[1],level1_enemy_surf)
            enemy_grp.add(enemy) """

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
                laser = player.shoot_laser() #shoot laser function of Player class generates new instance of Bullet
                bullet_grp.add(laser)
        
        #creates enemy at point of mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #old code to generate spawn positions
            #enemy = Enemy(pos[0],pos[1],enemy_surf)
            #enemy_grp.add(enemy)
            print(pos)
            if level == 0:
                if start_rect.collidepoint(pos): #check if start is clicked
                    level = 1
                    #level_start = True
                    #level_start has to be True beforehand
            
    level, level_start = level_control(level, level_start) #check what level we are up to
    if level != 0: #don't draw player on start menu
        player_grp.draw(screen)
        player.update() #update function includes movement

    enemy_grp.update()
    enemy_grp.draw(screen) #draws enemies

    bullet_grp.update() #moves bullets up
    bullet_grp.draw(screen) #draws bullets on screen
    
    pygame.display.update()
    clock.tick(TICK_RATE)