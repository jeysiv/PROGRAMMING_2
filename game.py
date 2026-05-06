import pygame
from pygame.locals import *
import os
import random


from config import screen_width, screen_height
from start_menu import StartMenu
from player import Player
from world import World
from levels import world_data
from fonts import get_font




class Game():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.SCALED)
        self.clock = pygame.time.Clock()
        
        self.menu = StartMenu()
        self.state = "menu"
        self.running = True

        # screen = pygame.display.set_mode((screen_width, screen_height)) #, pygame.FULLSCREEN
        pygame.display.set_caption("WHAT")#----> title


        self.player = Player(150, 200) # x, y #starting pos
        self.running = True
        
        self.current_major_level = 0
        self.current_sublevel = 0
        self.world = None
        
        self.level_tomb_img = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "tomb_level.png")).convert_alpha(), 
            (40, 40)
        )
        
        self.pause_button_img = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "pause_button.png")).convert_alpha(), 
            (32, 32)
        )
        
        self.repeat_button_img = pygame.image.load(os.path.join("image_s", "repeat_button.png")).convert_alpha()
        self.repeat_button_small = pygame.transform.scale(self.repeat_button_img, (25, 25))
        self.repeat_button_big = pygame.transform.scale(self.repeat_button_img, (50, 50))
        
        self.play_button_img = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "play_button.png")).convert_alpha(), 
            (50, 50)
        )
        
        self.exit_button_img = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "exit_button.png")).convert_alpha(), 
            (50, 50)
        )
        
        self.death_count = 0
        self.max_deaths = [10, 8, 10, 12, 15, 18, 20, 25]
        self.total_deaths = 0
        self.last_death_count = 0
        
        self.paused = False
        self.pause_button_rect = pygame.Rect(10, 10, 32, 32)
        self.repeat_small_rect = pygame.Rect(45, 13, 25, 25)
        self.play_button_rect = pygame.Rect(10, 10, 50, 50)
        self.repeat_big_rect = pygame.Rect(0, 0, 50, 50)
        self.exit_button_rect = pygame.Rect(0, 0, 50, 50).move(640, 360)
        
        self.shake_offset = [0, 0]
        self.shake_timer = 0
        self.shake_duration = 0.5
        self.shake_intensity = 5
        self.current_shake_intensity = self.shake_intensity
        

    
    def handles_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.state == "menu":
                self.menu.handle_event(event)
                
            elif self.state == "play":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.VELOCITY_Y == 0:
                        self.player.VELOCITY_Y = -8
                
                    if event.key == pygame.K_RETURN and self.player.dead:
                        self.world.reset()
                        self.player.reset()
                        self.player.dead = False
                        self.death_count += 1
                        self.total_deaths += 1
                    
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    
                    #CHEAT CODE
                    if event.key == pygame.K_c:
                        self.advance_level()
                
                
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.paused:
                    #for exit
                        if self.exit_button_rect.collidepoint(mouse_pos):
                            self.last_death_count = self.death_count
                            self.current_sublevel = 0
                            self.death_count = 0
                            self.world = None
                            self.player.reset()
                            self.state = "menu"
                            self.menu.active = True
                            self.paused = False
                        
                        
                        #reset/repeat
                        if self.repeat_big_rect.collidepoint(mouse_pos):
                            if self.player.dead:
                                self.death_count += 1
                                self.total_deaths += 1
                            self.load_sublevel()
                            self.paused = False
                        
                        #for play
                        if self.play_button_rect.collidepoint(mouse_pos):
                            self.paused = False
                    
                    else:
                        if self.pause_button_rect.collidepoint(mouse_pos):
                            self.paused = True
                        
                        if self.repeat_small_rect.collidepoint(mouse_pos):
                            if self.player.dead:
                                self.death_count += 1
                                self.total_deaths += 1
                            self.load_sublevel()
                                                
                   
    def load_sublevel(self):
        data = world_data[self.current_major_level][self.current_sublevel]
        self.world = World(data["data"])
        self.player.start_x, self.player.start_y = data["starting_position"]
        self.player.reset()
        self.player.rect.x, self.player.rect.y = data["starting_position"]
                
                        
    
    def advance_level(self):
        num_of_subs = len(world_data[self.current_major_level])
        
        if self.current_sublevel + 1 < num_of_subs:
            self.current_sublevel += 1
            self.load_sublevel()
            self.shake_timer = 0
            self.shake_offset = [0, 0]
        else:
            allowed_enter = self.max_deaths[self.current_major_level]
            
            if self.death_count <= allowed_enter:
                self.menu.complete_level(self.current_major_level)
                
            self.last_death_count = self.death_count
            self.current_sublevel = 0
            self.death_count = 0
            self.world = None
            self.player.reset()
            self.state = "menu"


        
    def update(self, dt):
        if self.state == "menu":
            self.menu.update(dt)
            if not self.menu.active:
                self.current_major_level = self.menu.selected_level
                self.current_sublevel = 0
                self.death_count = 0
                self.menu.active = True
                self.load_sublevel()
                self.state = "play"
            return
        
        
        elif self.state == "play":
            if self.paused:
                return
            
            was_dead = self.player.dead
            
            if self.shake_timer > 0: #init 0
                self.shake_timer -= dt
                intensity_shake = self.current_shake_intensity * (self.shake_timer / self.shake_duration)
                self.shake_offset = [
                    random.randint(-int(intensity_shake), int(intensity_shake)),
                    random.randint(-int(intensity_shake), int(intensity_shake))
                ]
            else:
                self.shake_offset = [0, 0]
            
            if self.world.door_with_player.active and not self.world.door_with_player.done:
                if self.shake_timer <= 0:#triggers once
                    self.shake_timer = self.shake_duration
                    self.current_shake_intensity = 3


            self.player.movement(self.world, dt)
            
            if self.player.dead and not was_dead:
                self.shake_timer = self.shake_duration
                self.current_shake_intensity = self.shake_intensity

            for p in self.player.particles[:]:
                p.update(self.world.platforms, dt)
                if not p.active:
                    self.player.particles.remove(p)
            
            self.world.update(self.player, dt)
            
            if self.world.door_with_player.done:
                self.advance_level()
        
    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen, self.last_death_count)
            
        elif self.state == "play":
            play_surface = pygame.Surface((screen_width, screen_height))
            play_surface.fill("#0088aa")
            
            self.world.draw(play_surface)
            # draw_grid()
            
            for p in self.player.particles:
                p.draw(play_surface)
            self.player.draw(play_surface)
            
            self.screen.blit(play_surface, self.shake_offset)
            
            #fortomb
            self.screen.blit(self.level_tomb_img, (1175, 8))
            death_font = get_font(24)
            allowed_enter = self.max_deaths[self.current_major_level]
            if self.death_count >= allowed_enter:
                color = (255, 80, 80)
            else:
                color = (255, 255, 255)
            death_text = death_font.render(f"{self.death_count} / {allowed_enter}", True, color)
            self.screen.blit(death_text, (1215, 15))
            
            sublevel_font = get_font(20)
            sublevel_text = sublevel_font.render(f"Level {self.current_major_level + 1} - {self.current_sublevel + 1}", True, (255, 255, 255))
            self.screen.blit(sublevel_text, (screen_width // 2 - sublevel_text.get_width() // 2, 15))
            
            self.screen.blit(self.pause_button_img, (10, 10)) 
            self.screen.blit(self.repeat_button_small, (45, 13))
            
            if self.paused:
                repeat_x = screen_width // 2 - self.repeat_button_big.get_width() // 2
                exit_x = screen_width // 2 - self.exit_button_img.get_width() // 2 - 150
                play_x = screen_width // 2 - self.play_button_img.get_width() // 2 + 150
                button_y = screen_height // 2 - self.exit_button_img.get_height() // 2
                
                self.screen.blit(self.repeat_button_big, (repeat_x, button_y))
                self.screen.blit(self.exit_button_img, (exit_x, button_y))
                self.screen.blit(self.play_button_img, (play_x, button_y))
                
                self.repeat_big_rect = pygame.Rect(repeat_x, button_y, 50, 50)
                self.exit_button_rect = pygame.Rect(exit_x, button_y, 50, 50)
                self.play_button_rect = pygame.Rect(play_x, button_y, 50, 50)
                
                 
            
            # for p in self.player.particles:
            #     p.draw(self.screen)
                
            # self.player.draw(self.screen)
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handles_events()
            self.update(dt)
            self.draw()
            
            pygame.display.update() #----> to show the content
            # self.clock.tick(60) #----> 60 frames per second
        
