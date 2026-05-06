import pygame
import os

from fonts import get_font, get_font_glitch, draw_text_spacing
from config import screen_width, screen_height
# from game import

class StartMenu():
    def __init__(self):
        self.active = True
        self.current_screen = "main"
        
        self.options = ["Play", "Mechanics", "Developers", "Quit"]
        self.selected = 0 #for options
        
        self.door_nav_mode = False
        self.selected_door_index = 0
        
        #fonts
        self.title_font = get_font(80) #change maya
        self.option_font = get_font(32)
        self.title_glitch = get_font_glitch(100)
        
        #bgd
        self.dark_topd = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "dark_top.png")), (screen_width, 250))
        self.pathways = pygame.transform.scale(pygame.image.load(os.path.join("image_s", "pathway_all.png")), (875, 303))
        
        #doorlevels
        self.door_img = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "door_spiker.png")).convert_alpha(), 
            (100, 80)
        )
        
        #arrow
        self.arrow_img = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "arrow.png")).convert_alpha(), 
            (32, 32)
        )
        
        #tomb
        self.tomb_img = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "tomb_menu.png")).convert_alpha(), 
            (65, 65)
        )
        
        #options arrow
        self.options_arrow = pygame.transform.scale(
            pygame.image.load(os.path.join("image_s", "options_arrow.png")).convert_alpha(), 
            (20, 20)
        )
        
        
        #PROGRESSION
        self.unlocked = 1
        self.selected_level = 0
        
        #arrowblink
        self.arrow_visible = True
        self.arrow_timer = 0
        #up=-
        #left=-
        #rects of doors
        self.doors = [#rect = x,y,w,h
            {"rect": pygame.Rect(467, 554, 100, 90), "level": 1},
            {"rect": pygame.Rect(277, 495, 100, 90), "level": 2},
            {"rect": pygame.Rect(213, 372, 100, 90), "level": 3},
            {"rect": pygame.Rect(404, 295, 100, 90), "level": 4},
            {"rect": pygame.Rect(590, 320, 100, 90), "level": 5},
            {"rect": pygame.Rect(690, 430, 100, 90), "level": 6},
            {"rect": pygame.Rect(857, 497, 100, 90), "level": 7},
            {"rect": pygame.Rect(1015, 440, 100, 90), "level": 8}
        ]
        
    def complete_level(self, level_idx):
        next_level = level_idx + 1
        if next_level >= self.unlocked and next_level <= len(self.doors):
            self.unlocked = next_level + 1 #one new door
            
            unlocked = self.get_unlocked_door_indices()
            self.selected_door_index = len(unlocked) - 1
    
    def get_unlocked_door_indices(self): #list of unlocked doors
        unlocked = []
        for i, door in enumerate(self.doors):
            if door["level"] <= self.unlocked:
                unlocked.append(i)
        return unlocked
    
    def range_door_selection(self):
        unlocked = self.get_unlocked_door_indices()
        
        if not unlocked:
            return
        
        max_index = len(unlocked) - 1
        
        if self.selected_door_index < 0:
            self.selected_door_index = 0
        
        if self.selected_door_index > max_index:
            self.selected_door_index = max_index
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            
            #door nav
            if self.door_nav_mode:
                unlocked = self.get_unlocked_door_indices()
                
                if event.key == pygame.K_RIGHT: #for previous door
                    if unlocked:
                        self.selected_door_index = (self.selected_door_index - 1) % len(unlocked)
                
                elif event.key == pygame.K_LEFT:
                    if unlocked:
                        self.selected_door_index = (self.selected_door_index + 1) % len(unlocked)
                
                elif event.key == pygame.K_RETURN:
                    if unlocked:
                        door_index = unlocked[self.selected_door_index]
                        self.selected_level = self.doors[door_index]["level"] - 1
                        self.active = False
                
                elif event.key == pygame.K_ESCAPE:
                    self.door_nav_mode = False
            
            #menus
            else:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options) #to movr
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    choice = self.options[self.selected]
                    
                    if choice == "Quit":
                        pygame.quit()
                        exit()
                    
                    if choice == "Play":
                        unlocked = self.get_unlocked_door_indices()
                        if unlocked:
                            self.selected_door_index = len(unlocked) - 1
                        self.door_nav_mode = True
                        
                        
                        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            for door in self.doors:
                 if door["rect"].collidepoint(mouse_pos):
                    idx = door["level"]
                    if idx <= self.unlocked:
                        self.selected_level = idx - 1
                        self.active = False
        
    
    def update(self, dt):
        if self.door_nav_mode:
            self.arrow_timer += dt
            if self.arrow_timer >= 0.33: #for like 30frames(lower means faster)
                self.arrow_visible = not self.arrow_visible
                self.arrow_timer = 0
        else:
            self.arrow_visible = False
            
    
    def draw(self, screen, total_deaths=0):
        screen.fill("#0088aa")
        #tomb
        screen.blit(self.tomb_img, (1140, 580)) #positin adjust maya
        death_text = self.option_font.render(str(total_deaths), True, (127, 159, 176))
        screen.blit(death_text, (1130, 595))
        
        screen.blit(self.dark_topd, (0, 0))
        
        #title
        font = self.title_glitch
        draw_text_spacing(screen, "NOT A TRAP", font, (0, 136, 170), screen.get_width() // 2 - 420, 20, spacing=20)

        # title = self.title_glitch.render("NOT A TRAP", True, (0, 136, 170))
        # title_rect = title.get_rect(midtop=(screen_width // 2, 30))
        # screen.blit(title, (title_rect))
        
        #tint for options
        if not self.door_nav_mode:
            overlay_tint = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay_tint.fill((0, 0, 0, 100))
            screen.blit(overlay_tint, (0, 0))
        
        #bgd-leave to
        screen.blit(self.pathways, (224, 331))
        
        
        #options
        for i, option in enumerate(self.options):
            if i == self.selected:
                color = (255, 255, 255)
            else:
                color = (127, 159, 176)
            text = self.option_font.render(option, True, color)
            text_x = 75
            text_y = 480 + i * 45
            screen.blit(text, (text_x, text_y))
            
            #arrow sa doors
            if i == self.selected and not self.door_nav_mode:
                arrow_x = text_x - self.options_arrow.get_width() - 10
                arrow_y = text_y + (text.get_height() - self.options_arrow.get_height()) // 2
                screen.blit(self.options_arrow, (arrow_x, arrow_y))
            
        if self.door_nav_mode:
            hint_font = get_font(20)
            hint = hint_font.render("\"L/R\" to select level            \"ENTER\" to play           \"ESC\" to menu", True, (200, 220, 230))
            screen.blit(hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 40))
        
        unlocked_indices = self.get_unlocked_door_indices()
        
        for i,door in enumerate(self.doors):
            level_num = door["level"]
            
            is_unlocked = level_num <=self.unlocked
            is_next = level_num == self.unlocked #????
            
            is_key_seleceted = False
            if self.door_nav_mode and unlocked_indices:
                key_door_index = unlocked_indices[self.selected_door_index]
                is_key_seleceted = (i == key_door_index)
            
            if not is_unlocked:
                tinted_doors = self.door_img.copy()
                tinted_doors.fill((50, 50, 80, 180), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted_doors, door["rect"].topleft)
            else:
                screen.blit(self.door_img, door["rect"].topleft)
            
            if self.door_nav_mode:
                if is_key_seleceted and self.arrow_visible:
                    arrow_x = door["rect"].centerx - self.arrow_img.get_width() // 2
                    arrow_y = door["rect"].top - self.arrow_img.get_height() - 5
                    screen.blit(self.arrow_img, (arrow_x, arrow_y))
                    
                    #arrow label
                    label_font = get_font(20)
                    label = label_font.render(f"Level {level_num}", True, (255, 255, 180))
                    label_x = door["rect"].centerx - label.get_width() // 2
                    label_y = door["rect"].top - self.arrow_img.get_height() - 28
                    screen.blit(label, (label_x, label_y))
            
            else:
                if is_next and self.arrow_visible:
                    arrow_x = door["rect"].centerx - self.arrow_img.get_width() // 2
                    arrow_y = door["rect"].top - self.arrow_img.get_height() - 5
                    screen.blit(self.arrow_img, (arrow_x, arrow_y))
                
        
        
        
        