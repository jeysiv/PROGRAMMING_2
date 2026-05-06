import pygame
import os

from obstacles import Tile, Falling_Block, Spike, Door, DoorWithPlayer, Sliding_Block, Moving_Spike, Hidden_Spike, Saw, Ceiling_Spike, Hidden_Ceiling_Spike
from config import tile_size

class World():
    def __init__(self, data):
        self.data = data
        
        #initialize from obstcles
        self.door_with_player = DoorWithPlayer()
        self.door = pygame.sprite.Group()
        
        self.platforms = pygame.sprite.Group()
        self.falling_blocks = pygame.sprite.Group()
        
        self.spikes = pygame.sprite.Group()
        self.hidden_spike = pygame.sprite.Group()
        self.ceiling_spike = pygame.sprite.Group()
        self.moving_spike = pygame.sprite.Group()
        self.hidden_ceiling_spike = pygame.sprite.Group()
        
        self.sliding_blocks = pygame.sprite.Group()
        self.saw = pygame.sprite.Group()
        

        #from django.utils.translation import ugettext_lazy as _
        tile_surface = pygame.Surface((tile_size, tile_size))
        tile_surface.fill("#003a49")
        
        # #fallingblock
        # tile_surfs =  pygame.Surface((tile_size, tile_size))
        # tile_surfs.fill("#003a49")
        
        tile_spike = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "spike_static.png")), (40, 7))
        
        tile_saw = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "saw.png")), (40, 40))
        
        for row_index, row in enumerate(data): #loops through every cell in 2D grid
            for column_index, tile_type in enumerate(row): #converts the grid position into pixel coordinates, e.g. column 3 = 3×50 = 150px from left, same sa height = ((x=150, y=100))
                    
                    #pexil coord
                    rect_x = column_index * tile_size
                    rect_y = row_index * tile_size
                    
                    if tile_type == 1: #Tile
                        self.platforms.add(Tile(rect_x, rect_y, tile_surface))
                    elif tile_type == 2: #Door
                        self.door.add(Door(rect_x, rect_y))
                        
                        
                    elif tile_type == 3: #Fallingblock
                        self.falling_blocks.add(Falling_Block(rect_x, rect_y, tile_surface, 50))  #SPEED 50
                    elif tile_type == 4: #Fallingblock
                        self.falling_blocks.add(Falling_Block(rect_x, rect_y, tile_surface, 10))  #speed 2
                         
                         
                    elif tile_type == 5: #Spike
                        self.spikes.add(Spike(rect_x, rect_y, tile_spike))
                    elif tile_type == 6: #Movingspike
                        self.moving_spike.add(Moving_Spike(rect_x, rect_y, tile_spike))
                    elif tile_type == 7: #Movingspike 
                        self.moving_spike.add(Moving_Spike(rect_x, rect_y, tile_spike))
                    
                    elif tile_type == 8: #Sliding_blocks RIGHT
                        self.sliding_blocks.add(Sliding_Block(rect_x, rect_y, tile_surface, "right"))
                    elif tile_type == 9: #Sliding_blocks LEFT
                        self.sliding_blocks.add(Sliding_Block(rect_x, rect_y, tile_surface, "left"))
                    
                    elif tile_type == 10: #Hidden_spike
                        self.hidden_spike.add(Hidden_Spike(rect_x, rect_y, tile_spike))
                    elif tile_type == 11: #Ceiling_spike
                        self.spikes.add(Ceiling_Spike(rect_x, rect_y, tile_spike))
                    elif tile_type == 12: #Hidden_ceiling_spike
                        self.spikes.add(Hidden_Ceiling_Spike(rect_x, rect_y, tile_spike))
                        
                    
                    elif tile_type == 13: #Saw hori
                        self.saw.add(Saw(rect_x, rect_y, tile_saw, "horizontal", speed=5, move_range=100))
                        
                    elif tile_type == 14: #Saw verti
                        self.saw.add(Saw(rect_x, rect_y, tile_saw, "vertical", speed=5, move_range=100))
                        
                    
                    
                    
                        

    
    # def draw(self): #loops through every tile and draws it on the screen
    #     for tile in self.tile_list:
    #         tile.draw(screen)
    
    def draw(self, screen):
        self.falling_blocks.draw(screen)
        self.spikes.draw(screen)
        self.door_with_player.draw(screen)
        self.platforms.draw(screen)
        for door in self.door:
            door.draw(screen)
        for block in self.sliding_blocks:
            block.draw(screen)
        self.moving_spike.draw(screen)
        for spike in self.hidden_spike:
            spike.draw(screen)
        self.saw.draw(screen)
        self.ceiling_spike.update(screen)
        
        
    
    def update(self, player, dt):
        self.falling_blocks.update(player, dt)
        self.spikes.update(player)
        for door in self.door:
            door.update(player, self.door_with_player)
        self.door_with_player.update(dt)
        self.sliding_blocks.update(player, dt)
        self.moving_spike.update(player, dt)
        self.hidden_spike.update(player, dt)
        self.saw.update(player, dt)
        self.ceiling_spike.update(player)
        
        if self.door_with_player.done:
            return "FINISHED"
        
    
    def reset(self):
        for block in self.falling_blocks:
            block.rect.y = block.start_y
            block.falling = False
        
        for door in self.door:
            door.active = True
        self.door_with_player.reset()
        
        for block in self.sliding_blocks:
            block.reset()
            self.sliding_blocks.add(block)
        
        for spike in self.moving_spike:
            spike.reset()
        
        for spike in self.hidden_spike:
            spike.reset()
        
        for saw in self.saw:
            saw.reset()
