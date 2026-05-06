import pygame
import os

from config import tile_size

class Tile(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = rect_x #builtin attribute (.x)
        self.rect.y = rect_y #same here
        
    # def draw(self, screen): #puts tile on the screen
    #     screen.blit(self.image, self.rect)
        

class Falling_Block(Tile):
    def __init__(self, rect_x, rect_y, image, fall_speed):
        super().__init__(rect_x, rect_y, image)
        self.fall_speed = fall_speed
        self.falling = False
        self.trigger_range = 50 #how many pixels away the trigger
        self.start_y = rect_y
        
    def update(self, player, dt):
        if abs(player.rect.centerx - self.rect.centerx) <= self.trigger_range:
            self.falling = True

        if self.falling:
            self.rect.y += self.fall_speed * dt * 60


class Spike(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image):
        super().__init__()
        self.image = image
        
        self.rect = pygame.Rect(rect_x, rect_y + (40 - 7), 40, 7)
    
    def update(self, player):
        self.check_player_hit(player)
        
    def check_player_hit(self, player):
        if self.rect.colliderect(player.rect):
            player.dead = True


class Ceiling_Spike(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image):
        super().__init__()
        self.image = pygame.transform.flip(image, False, True)
        
        self.rect = pygame.Rect(rect_x, rect_y, 40, 7)
    
    def update(self, player):
        self.check_player_hit(player)
        
    def check_player_hit(self, player):
        if self.rect.colliderect(player.rect):
            player.dead = True


class Door(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "door.png")), (tile_size, 36))
        
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y - (self.rect.height - tile_size)
        self.active = True
        self.enter_range = 10 #how close the player and door
    
    def update(self, player, door_with_player):
        if not self.active:
            return
        
        distance_x = abs(player.rect.centerx - self.rect.centerx)
        distance_y = abs(player.rect.centery - self.rect.centery)
        if distance_x <= self.enter_range and distance_y  <= self.enter_range and player.rect.bottom <= self.rect.bottom:
            self.active = False
            player.alpha = 0
            door_with_player.activate(self.rect.x, self.rect.y)
    
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)


class DoorWithPlayer():
    def __init__(self):
        
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "door_player.png")), (tile_size,  36))
        
        self.rect = self.image.get_rect()
        
        self.active = False
        self.sinking = False
        
        self.sink_speed = 0.8
        self.sink_target = 0
        
        self.done = False
    
    def activate(self, rect_x, rect_y):
        #positon
        self.rect.x = rect_x
        self.rect.y = rect_y
        
        self.active = True
        self.sinking = True
        
        self.sink_target = self.rect.y + self.rect.height
        
        self.done = False
    
    def update(self, dt):
        if not self.active:
            return
        if self.sinking:
            self.rect.y += self.sink_speed * dt * 60
            if self.rect.y >= self.sink_target:
                self.rect.y = self.sink_target
                self.sinking = False
                self.done = True
    
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
    
    def reset(self):
        self.active = False
        self.sinking = False
        self.done = False
        

class Sliding_Block(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image, direction="right"):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        
        self.slide_speed = 300
        self.sliding = False
        self.trigger_range = 50
        self.start_x = rect_x
        
        if direction == "right":
            self.direction = 1
        else:
            self.direction = -1
        
        self.gone = False
    
    def update(self, player, dt):
        if not self.sliding and not self.gone:
            if abs(player.rect.centerx - self.rect.centerx) <= self.trigger_range:
                self.sliding = True
        
        if self.sliding:
            self.rect.x += self.slide_speed * self.direction * dt
            if abs(player.rect.centerx - self.rect.centerx) > self.rect.width * 2:
                self.gone = True
                self.sliding = False
    
    def draw(self, screen):
        if not self.gone:
            screen.blit(self.image, self.rect)
    
    def reset(self):
        self.rect.x = self.start_x
        self.sliding = False
        self.gone = False


class Moving_Spike(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image, speed=5, move_range=20):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(rect_x, rect_y + (40 - 7), 40, 7)
        
        self.speed = speed
        self.move_range = move_range
                
        self.start_x = rect_x
        self.start_y = rect_y
        self.moving = 1 #forward, negative for backwrad
        
        self.trigger_range = 40
        self.triggered = False
    
    def update(self, player, dt):
        if not self.triggered:
            if abs(player.rect.centerx - self.rect.centerx) <= self.trigger_range:
                self.triggered = True
        
        if self.triggered:
            if abs(self.rect.x - self.start_x) < self.move_range:
                self.rect.x += self.speed * self.moving * dt * 60

            
        self.check_player_hit(player)
    
    def check_player_hit(self, player):
        if self.rect.colliderect(player.rect):
            player.dead = True
    
    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y + (40 - 7)
        self.moving = 1
        self.triggered = False


class Hidden_Spike(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(rect_x, rect_y + (40 - 7), 40, 7)
        self.trigger_range = 50
        self.visible = False
        self.start_x = rect_x
        self.start_y = rect_y
    
    def update(self, player, dt):
        if not self.visible:
            if abs(player.rect.centerx - self.rect.centerx) <= self.trigger_range:
                self.visible = True
                
        self.check_player_hit(player)
    
    def check_player_hit(self, player):
        if self.rect.colliderect(player.rect):
            player.dead = True
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
    
    def reset(self):
        self.visible = False


class Hidden_Ceiling_Spike(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image):
        super().__init__()
        self.image = pygame.transform.flip(image, False, True)
        self.rect = pygame.Rect(rect_x, rect_y, 40, 7)
        self.trigger_range = 50
        self.visible = False
        self.start_x = rect_x
        self.start_y = rect_y
    
    def update(self, player, dt):
        if not self.visible:
            if abs(player.rect.centerx - self.rect.centerx) <= self.trigger_range:
                self.visible = True
                
        self.check_player_hit(player)
    
    def check_player_hit(self, player):
        if self.rect.colliderect(player.rect):
            player.dead = True
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
    
    def reset(self):
        self.visible = False


class Saw(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, image, direction="horizontal", speed=50, move_range=100):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y + self.image.get_height() // 2
        
        self.speed = speed
        self.move_range = move_range
        self.direction = direction
        self.moving = 1
        
        self.start_x = rect_x
        self.start_y = self.rect.y
    
    def update(self, player, dt):
        if self.direction == "horizontal":
            self.rect.x += self.speed * self.moving * dt * 60
            if abs(self.rect.x - self.start_x) >= self.move_range:
                self.moving *= -1
        
        elif self.direction == "vertical":
            self.rect.y += self.speed * self.moving * dt * 60
            if abs(self.rect.y - self.start_y) >= self.move_range:
                self.moving *= -1
        
        self.check_player_hit(player)
    
    def check_player_hit(self, player):
        if self.rect.colliderect(player.rect):
            player.dead = True
    
    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.moving = 1