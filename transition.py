import pygame
import os 
from config import screen_width, screen_height

class Transition():
    def __init__(self):
        self.top_img = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "top.png")).convert_alpha(), (screen_width, screen_height))
        self.bottom_img = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "bottom.png")).convert_alpha(), (screen_width, screen_height))
        
        self.state = "static"
        self.speed = 1200
        
        #position
        self.top_y = 0
        self.bottom_y = screen_height // 2
        
        self.top_closed = 0
        self.bottom_closed = screen_height // 2
        
        self.top_open = -screen_height // 2
        self.bottom_open = screen_height
        
        self.done = False
        self.callback = None
    
    def open(self, callback=None):
        self.top_y = self.top_closed
        self.bottom_y = self.bottom_closed
        self.state = "opening"
        self.done = False
        self.callback = callback
    
    def close(self, callback=None):
        self.top_y = self.top_open
        self.bottom_y = self.bottom_open
        self.state = "closing"
        self.done = False
        self.callback = callback
    
    def update(self, dt):
        if self.state == "opening":
            self.top_y -= self.speed * dt
            self.bottom_y += self.speed * dt
            
            if self.top_y <= self.top_open:
                self.top_y = self.top_open
                self.bottom_y = self.bottom_open
                self.state = "static"
                self.done = True
                if self.callback:
                    self.callback()
            
            elif self.state == "closing":
                self.top_y += self.speed * dt
                self.bottom_y -= self.speed * dt
                
                if self.top_y >= self.top_closed:
                    self.top_y = self.top_closed
                    self.bottom_y = self.bottom_closed
                    self.state = "static"
                    self.done = True
                    if self.callback:
                        self.callback
    
    def draw(self, screen):
        if self.state != "static" or (self.top_y == self.top_closed):
            screen.blit(self.top_img, (0, int(self.top_y)))
            screen.blit(self.bottom_img, (0, int(self.bottom_y)))
    
    @property
    def is_active(self):
        return self.state != "static"
                    
        