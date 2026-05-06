import pygame
import os
import random
import math

from config import screen_width, screen_height


class DeathParticle():
    def __init__(self, x, y, angle, speed):
        #position
        self.x = x
        self.y = y
        
        #random movemnt
        self.VELOCITY_X = math.cos(angle) * speed
        self.VELOCITY_Y = math.sin(angle) * speed
        
        #size of chunk
        self.chunk_size = random.randint(3, 5)
        
        self.color = (0, 0, 0)
        
        self.active = True
        
        # #gravity
        # self.gravity = 0.25
        
    def update(self, platforms, dt):
        if not self.active:
            return #di gagamitin daw ay
        
        #particle move
        self.x += self.VELOCITY_X * dt * 60 #position += velocity_x * dt * 60
        particle_rect = pygame.Rect(int(self.x), int(self.y), self.chunk_size, self.chunk_size)
        for tile in platforms:
            if particle_rect.colliderect(tile.rect): #if particlesrect collides with tilerect
                if self.VELOCITY_X > 0: #moves to the right
                    self.x = tile.rect.left - self.chunk_size #width of the particle
                elif self.VELOCITY_X < 0: #moves to left
                    self.x = tile.rect.right #self.x is alrdy the left
                break
        
        #same notes
        self.y += self.VELOCITY_Y * dt * 60
        particle_rect = pygame.Rect(int(self.x), int(self.y), self.chunk_size, self.chunk_size)
        for tile in platforms:
            if particle_rect.colliderect(tile.rect):
                # Land on top of tile — stop vertical movement, slide horizontal
                if self.VELOCITY_Y > 0:
                    self.y = tile.rect.top - self.chunk_size
                    self.VELOCITY_Y = 0
                    self.VELOCITY_X *= 0.6  #friction when landing
                elif self.VELOCITY_Y < 0:
                    self.y = tile.rect.bottom
                    self.VELOCITY_Y = 0
                break
        
        #GRAVTIY ON PARTICLES
        self.VELOCITY_Y += 0.6 * dt * 60
        if self.VELOCITY_Y > 12:
            self.VELOCITY_Y = 12
        
        #air resistance
        self.VELOCITY_X *= 1.1
        
        if self.y > screen_height + 50: #if pos_y > s_h + 50, off
            self.active = False
    
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.chunk_size, self.chunk_size))        



class Player(pygame.sprite.Sprite):
    def __init__(self, PLAYER_X, PLAYER_Y): #POSITION X, Y
        super().__init__()
        self.start_x = PLAYER_X
        self.start_y = PLAYER_Y
        
        #IMAGES
        self.player_static_r = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "static.png")), (32, 36)
        )
        
        self.player_moving_r = [#list
            pygame.transform.scale(pygame.image.load(os.path.join("image_s", "move_1.png")), (32, 36)),
            pygame.transform.scale(pygame.image.load(os.path.join("image_s", "move_2.png")), (32, 36)),
            pygame.transform.scale(pygame.image.load(os.path.join("image_s", "move_3.png")), (32, 36)),
            pygame.transform.scale(pygame.image.load(os.path.join("image_s", "move_4.png")), (32, 36)),
        ]
        
        #FLIP THR RIGHT TO LEFT HAHAHAHAHAHAHAHAHAHAHAHAHAHAHA JK
        self.player_static_l = pygame.transform.flip(self.player_static_r, True, False)
        self.player_moving_l = [
            pygame.transform.flip(img, True, False) for img in self.player_moving_r
        ]
        
        #IMAGE CONTAINER
        self.image = self.player_moving_r[1] #1 for moving
        
        #FOR POSITIONING/RECT
        self.rect = pygame.Rect(0, 0, 17, 36) #x,y,w,h
        
        self.rect.x = PLAYER_X #x position
        self.rect.y = PLAYER_Y #y position
        self.width = self.image.get_width() #x position of img
        self.height = self.image.get_height() #y positon
        
        #FOR PHYSICS AY/SPEED FOR X AND Y
        self.VELOCITY_Y = 0
        self.VELOCITY_X = 0

        
        self.direction = "right"
        self.state = "static"
        
        self.frame_index = 0 #which frame is currently showing
        self.animation_speed = 0.20 #how fast the sprite frames for every loop (for the player lang)
        
        #deads
        self.dead = False
        self.death_triggered = False
        self.particles = []
        
        #transparency
        self.alpha = 255
        self.fading = False
    
    def spawn_particles(self):
        num_particles = 20
        
        for i in range(num_particles):
            #spread
            angle = (2 * math.pi / num_particles) * i 
            angle += random.uniform(-0.15, 0.15)
            
            speed = random.uniform(2.5, 9.0) #range
            
            spawn_x = self.rect.x + random.randint(0, self.rect.width - 1) #(0, x-y player position-1)
            spawn_y = self.rect.y + random.randint(0, self.rect.height - 1)
            
            particle = DeathParticle(spawn_x, spawn_y, angle, speed)
            
            self.particles.append(particle)
    
    def movement(self, world, dt):
        if self.dead:
            if not self.death_triggered:
                self.spawn_particles() #magboom?
                self.death_triggered = True
                self.alpha = 0 #player disappears
            
            return
        
        keys = pygame.key.get_pressed() #smooth movement (continuous)
        self.moving = False #reset every frame
        self.VELOCITY_X = 0 #reset so player doesnt accelerate forever
        
        #for keys
        if keys[pygame.K_LEFT]:
            self.VELOCITY_X -= 3.5 #-5
            self.direction = "left"
            self.moving = True
            
        if keys[pygame.K_RIGHT]:
            self.VELOCITY_X += 3.5 #+5
            self.direction = "right"
            self.moving = True
        
        #move x first then check collisions
        self.rect.x += self.VELOCITY_X * dt * 60 #e.g. 150 + (-+5) = ? *delta?
        self.check_collision_x(world)
        
        #GRAVITY
        self.VELOCITY_Y += 0.8 * dt * 60  #velocity gets down(since positive)----> what pulls the velocity down
        if self.VELOCITY_Y > 10: #for jump
            self.VELOCITY_Y = 10 #limit fall speed
        #y collis
        self.rect.y += self.VELOCITY_Y * dt * 60
        self.check_collision_y(world)
        
        #boundary dead
        if self.rect.bottom > screen_height:
            self.dead = True
        
        #state
        if self.VELOCITY_Y != 0:
            self.state = "jump"
        elif self.moving:
            self.state = "walk"
        else:
            self.state = "static"
        
        #frame animation
        if self.state != "walk":
            self.frame_index = 0 #static
            
            
        #CONDITION FOR MOVEMENT(WALKING)
        if self.state == "walk":
            self.frame_index += self.animation_speed #0 + 0.15 if moving
            
            #if frame sprite is >= number in list(4), it resets to 0----> to reset the frames
            if self.frame_index >= len(self.player_moving_r): #len() for getting the list from the player_moving_r sa taas #if 0.15 >= 2 -> so false
                self.frame_index = 0 #goes back
            
            if self.direction == "right":
                self.image = self.player_moving_r[int(self.frame_index)] #uses int ngani
            else:
                self.image = self.player_moving_l[int(self.frame_index)]
                
        #jumping flips-frame animation
        elif self.state == "jump":
            if self.direction == "right":
                self.image = self.player_moving_r[1]
            else:
                self.image = self.player_moving_l[1]

        #static
        else:
            self.frame_index = 0
            
            if self.direction == "right":
                self.image = self.player_static_r
            else:
                self.image = self.player_static_l
                
          
        
    def check_collision_x(self, world):
        for tile in world.platforms:
            if self.rect.colliderect(tile.rect):
                if self.VELOCITY_X > 0:
                    self.rect.right = tile.rect.left #if sa collision, right si player, si rect ni block is left, so di mag overlap sila
                elif self.VELOCITY_X < 0:
                    self.rect.left = tile.rect.right #likewise here
        
    def check_collision_y(self, world):
        for tile in world.platforms:
            if self.rect.colliderect(tile.rect):
                if self.VELOCITY_Y > 0:
                    self.rect.bottom = tile.rect.top #same rin dito
                    self.VELOCITY_Y = 0
                elif self.VELOCITY_Y < 0:
                    self.rect.top = tile.rect.bottom #and dito
                    self.VELOCITY_Y = 0
    

#---------->
    
    def draw(self, screen):
        image_x = self.rect.x - (self.image.get_width() - self.rect.width) // 2
        image_y = self.rect.y - (self.image.get_height() - self.rect.height) // 2
        
        #for transpercy
        img = self.image.copy()
        img.set_alpha(self.alpha)
        
        screen.blit(img, (image_x, image_y))
    
    def reset(self): #call this function kapag mag-rereset si player
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.VELOCITY_X = 0
        self.VELOCITY_Y = 0
        self.state = "static"
        
        
        self.dead = False
        self.death_triggered = False
        self.particles = []
        
        self.alpha = 255
        self.fading = False

