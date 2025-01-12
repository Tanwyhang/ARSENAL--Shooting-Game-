import pygame
import random
import json
import math
import sys
import os


# Base colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (25, 25, 25)
WHITE = (255, 255, 255)
GOLD = (255, 223, 0)


colors = {
    "green": {
        1: "#F0F7F0", 2: "#E7F0E7", 3: "#DDE8DD", 4: "#D4E1D4", 
        5: "#CBD9CB", 6: "#C2D2C2", 7: "#B9CDB9", 8: "#B0C7B0",
        9: "#A7C2A7", 10: "#9EBCA0", 11: "#95B69B", 12: "#8CB196",
        13: "#84AC91", 14: "#7BA78C", 15: "#72A387", 16: "#699E83",
        17: "#60987F", 18: "#57937A", 19: "#4E8D75", 20: "#458870",
        21: "#03543c"
    },
    "blue": {
        1: "#F0F4F7", 2: "#E7EDF0", 3: "#DDE5E8", 4: "#D4DEE1", 
        5: "#CBD6D9", 6: "#C2CFD2", 7: "#B9C7CD", 8: "#B0C0C7",
        9: "#A7B9C2", 10: "#9EB2BC", 11: "#95ABB6", 12: "#8CA4B1",
        13: "#849DAC", 14: "#7B96A7", 15: "#728FA2", 16: "#69889D",
        17: "#608198", 18: "#577A93", 19: "#4E738E", 20: "#456C89",
        21: "#033c54"
    },
    "purple": {
        1: "#F5F0F7", 2: "#EDE7F0", 3: "#E4DDE8", 4: "#DCD4E1", 
        5: "#D3CBD9", 6: "#CBC2D2", 7: "#C2B9CD", 8: "#BAB0C7",
        9: "#B1A7C2", 10: "#A99EBC", 11: "#A095B6", 12: "#988CB1",
        13: "#8F84AC", 14: "#877BA7", 15: "#7E72A2", 16: "#76699D",
        17: "#6D6098", 18: "#655793", 19: "#5C4E8E", 20: "#544589",
        21: "#3c0354"
    },
    "pink": {
        1: "#FFF0F5", 2: "#FFF5F8", 3: "#FFEAF2", 4: "#FFDFEB", 
        5: "#FFD4E4", 6: "#FFC9DD", 7: "#FFBFD6", 8: "#FFB4CF",
        9: "#FFA9C8", 10: "#FF9EC1", 11: "#FF93BA", 12: "#FF88B3",
        13: "#FF7DAC", 14: "#FF72A5", 15: "#FF679E", 16: "#FF5C97",
        17: "#FF5190", 18: "#FF4689", 20: "#FF3B82", 
        21: "#FF307B"
    },
    "red": {
        1: "#F7F0F0", 2: "#F0E7E7", 3: "#E8DDDD", 4: "#E1D4D4", 
        5: "#D9CBCB", 6: "#D2C2C2", 7: "#CDB9B9", 8: "#C7B0B0",
        9: "#C2A7A7", 10: "#BC9E9E", 11: "#B69595", 12: "#B18C8C",
        13: "#AC8484", 14: "#A77B7B", 15: "#A27272", 16: "#9D6969",
        17: "#986060", 18: "#935757", 19: "#8E4E4E", 20: "#894545",
        21: "#540303"
    },
    "brown": {
        1: "#F7F4F0", 2: "#F0EDE7", 3: "#E8E5DD", 4: "#E1DED4", 
        5: "#D9D6CB", 6: "#D2CEC2", 7: "#CDC7B9", 8: "#C7C0B0",
        9: "#C2B9A7", 10: "#BDB2A0", 11: "#B8AC9B", 12: "#B3A696",
        13: "#AEA091", 14: "#A9998C", 15: "#A49387", 16: "#9F8C82",
        17: "#9A867D", 18: "#958078", 19: "#907A73", 20: "#8B746E",
        21: "#633C33"
    },
    "orange": {
        1: "#FFF5F0", 2: "#FFF0E7", 3: "#FFE8DD", 4: "#FFE1D4", 
        5: "#FFD9CB", 6: "#FFD2C2", 7: "#FFC9B9", 8: "#FFC0B0", 
        9: "#FFB7A7", 10: "#FFAE9E", 11: "#FFA595", 12: "#FF9C8C", 
        13: "#FF9384", 14: "#FF8A7B", 15: "#FF8172", 16: "#FF7869", 
        17: "#FF6F60", 18: "#FF6657", 19: "#FF5D4E", 20: "#FF5445", 
        21: "#993629"
    }
}

# Add near your other constants (near RED, GREEN, BLUE etc.)
SNAP_RADIUS = 150
SNAP_SPEED = 0.5

# Initialize Pygame
pygame.mixer.init(buffer=512)
pygame.mixer.set_num_channels(10000)
pygame.init()
monitor_size = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode(monitor_size)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
width, height = monitor_size
scale_width = (width / 1536)
scale_height = (height / 864)


# Create surfaces for effects
glow_canvas = pygame.Surface(monitor_size)
glow_canvas.set_alpha(100)

# Constants
x = 0
y = 1
floor = height * 0.85
game_speed = 1



# Load font
font_name = os.path.join('assets\\font.TTF')
font = pygame.font.Font(font_name, int(width / 50))

# Load images
def load_game_image(filename, scale=None, convert_alpha=True):
    image = pygame.image.load(os.path.join('assets', filename))
    if convert_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# Game assets
weaponshop_image = load_game_image('weaponshop.png', [height / 2, height / 2])
weaponshopselect_image = load_game_image('weaponshop_s.png', [height / 2, height / 2])
stargazer_image = load_game_image('weapon-stargazer.png')
shotgun_image = load_game_image('weapon-shotgun.png')
stargazer_bullet_image = load_game_image('bullet-stargazer.png', [width / 30, width / 30])
shotgun_bullet_image = load_game_image('bullet-shotgun.png', [width / 30, width / 30])
player_image = load_game_image('player.png', [width / 10, width / 10])
hip = player_image.get_height() * 0.65

# Tile images
basic_tile_image = load_game_image('tile-basic.png', [width / 10, width / 10], False)
basic_tile_image_night = load_game_image('tile-basic-night.png', [width / 10, width / 10], False)
grass_tile_image = load_game_image('tile-grass.png', [width / 10, width / 10])
grass_tile_image_night = load_game_image('tile-grass-night.png', [width / 10, width / 10])
mushroom_image_idle = load_game_image('mushroom-idle.png', [width / 10, width / 10])
mountain_image = load_game_image('mountains.png', monitor_size)
mountain_image_night = load_game_image('mountains-night.png', monitor_size)

# Load sounds
shoot_sound = pygame.mixer.Sound('assets\\sound-shoot.wav')
explode_sound = pygame.mixer.Sound('assets\\sound-explode.wav')
select_sound = pygame.mixer.Sound('assets\\sound-select.wav')
hit_sound = pygame.mixer.Sound('assets\\sound-hit.wav')
die_sound = pygame.mixer.Sound('assets\\sound-die.wav')

# Create fade effects
fades = []
blacksurf = pygame.Surface(monitor_size)
blacksurf.fill(BLACK)
flashes = []
whitesurf = pygame.Surface(monitor_size)
whitesurf.fill(WHITE)

for i in range(255):
    blacksurf.set_alpha(i)
    whitesurf.set_alpha(i)
    fades.append(blacksurf.copy())
    flashes.append(whitesurf.copy())

def delta_to_modifier(delta):
    return delta / 1000 * 60

def get_centered(image):
    return [image.get_width() / 2, image.get_height() / 2]

def draw_text(string, x, y, color=WHITE):
    text = font.render(string, True, color)
    textRect = text.get_rect()
    textRect.topleft = [x, y]
    screen.blit(text, textRect)

def draw_circle(pos):
    pygame.draw.circle(screen, WHITE, pos, width / 50, int(width / 200))

def draw_bar(pos, a, b, size=1, color=colors['red'][19], border=1, line=False):
    if a >= b:
        a = b
    if a != 1:
        r = pygame.Rect(pos[x], pos[y], width / 20 * (a / b) * size, height / 50 * size)
    else:
        r = pygame.Rect(pos[x] + 2.5 * border, pos[y], width / 20 * (a / b) * size, height / 50 * size)
    r_fixed = pygame.Rect(pos[x], pos[y], width / 20 * size, height / 50 * size)
    pygame.draw.rect(screen, color, r)
    pygame.draw.rect(screen, BLACK, r_fixed, 3)
    
    if line:
        n = size * ((width / 20) / b)
        for i in range(b - 1):
            pygame.draw.line(screen, BLACK,
                           [pos[x] + n * (1 + i), pos[y]],
                           [pos[x] + n * (1 + i), pos[y] + height / 50 * size - 2.5 * border],
                           1 + int(7 / b))

class Game:
    def __init__(self):
        with open('assets\\game.json', 'r') as f:
            self.gamedata = json.load(f)
        self.exp = self.gamedata["exp"]
        self.gold = self.gamedata["gold"]
        self.expd = 0
        self.expc = 0
        self.goldd = 0
        self.goldc = 0

    def render_ui(self):
        # Display FPS at top right
        fps = int(clock.get_fps())  # Assuming you have a pygame clock object
        # Draw right-aligned stats at top right
        performance_stats_text = [
            f"FPS: {fps}",
            f"Render Load: {len(effects_array) + len(render_array) + len(entities_array)}"
        ]
        draw_multiline_text_right(performance_stats_text, width * 0.99, height * 0.01, color=(255, 255, 255))
        
        # Original UI elements
        self.expd += (self.exp - self.expd) / 10 * dt
        self.expc += (255 - self.expc) / 30 * dt
        self.goldd += (self.gold - self.goldd) / 10 * dt
        self.goldc += (255 - self.goldc) / 30 * dt
        draw_text(f'EXP: {round(self.expd)}', width * 0.01, height / 4, 
                color=(255, 255, self.expc))
        draw_text(f'GOLD: {round(self.goldd)}', width * 0.01, height / 4 + 90, 
                color=(self.goldc, self.goldc, 255))

    def save_progress(self):
        self.expc = 0
        self.goldc = 0
        self.gamedata['exp'] = self.exp
        self.gamedata['gold'] = self.gold
        with open('assets\\game.json', 'w') as f:
            json.dump(self.gamedata, f)

class Environment:
    def __init__(self):
        self.border_image = 0
        self.sky_color = colors['green'][5]
        self.night_sky_color = colors['blue'][21]
        self.background_color = BLACK
        self.soil = basic_tile_image
        self.soil_night = basic_tile_image_night
        self.grass = grass_tile_image
        self.grass_night = grass_tile_image_night
        self.maintiles = [self.grass, self.soil]
        self.tile_width = self.soil.get_width()
        self.floor_modded = floor - player.height / 8
        self.tile_count = 60
        self.mountains = mountain_image
        self.mountain_pos_x = 0
        self.mountain_pos_x_base = 0
        
        # Effect states
        self.fading_in = False
        self.fading_out = False
        self.flashing_in = False
        self.flashing_out = False
        self.daynight_tswitch = True
        
        # Initialize tile array
        self.tile_array = []
        self.tile_array_alt = []
        q = 0
        for i in range(self.tile_count):
            q += 1
            for s in range(4):
                if s == 0:
                    self.tile_array.append([[self.tile_width * i - width * (self.tile_count / 30),
                                           self.floor_modded], 'grass'])
                else:
                    self.tile_array.append([[self.tile_width * i - width * (self.tile_count / 30),
                                           self.floor_modded + self.tile_width * s], 'soil'])
        
        # Initialize environment state
        self.current_day = 0 # start from zero since cutscene auto +1
        self.daynight_value = 4
        self.daynight = math.sin(self.daynight_value)
        self.daynight_inverse = math.cos(self.daynight_value)
        
        # Mushroom spawning
        self.mushroom_counts = 6
        self.mushroom_spawn_cd = 80
        self.mushroom_spawned = False
        self.mushroom_ticker = 0
        self.mushroom_die_cd = 7
        self.mushroom_die_ticker = 0
        self.mushroom_area_a = 0
        self.mushroom_area_b = 0
        
        # Effect timing
        self.game_time = 1
        self.shake_time = 0
        self.slow_time = 0
        self.fade = 0
        self.flash = 0
        
        # Initialize mushrooms
        for i in range(self.mushroom_counts):
            self.spawn_mushrooms()
        
        self.meteor_timer = 0
        self.meteor_spawn_rate = 20
        self.targeted_attack_timer = 0
        self.targeted_attack_rate = 300
        self.targeted_attack_count = 10

        self.sequence_active = False
        self.sequence_timer = 0
        self.sequence_interval = 15  # 0.5 second between meteors
        self.sequence_count = 0
        self.sequence_target = None
        self.max_sequence = 10

        # Cutscene settings
        self.night_cutscene_activated = False
        self.day_cutscene_activated = False


        self.cutscene_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    def play_day_cutscene(self):
        cutscene_running = True
        last_time = pygame.time.get_ticks()
        cutscene_start_time = last_time

        # Create text surfaces
        self.current_day = getattr(self, 'current_day', 1) + 1  # Increment day counter
        day_text = font.render(f"Day {self.current_day}", True, colors['blue'][2])
        text_pos = [width/2 - day_text.get_width()/2, height/2 - day_text.get_height()/2]

        # Timing constants 
        FADE_IN_TIME = 60   # 1 second fade in
        PAUSE_TIME = 60     # 1 second pause
        FADE_OUT_TIME = 60  # 1 second fade out
        TOTAL_TIME = FADE_IN_TIME + PAUSE_TIME + FADE_OUT_TIME

        while cutscene_running and not self.day_cutscene_activated:
            current_time = pygame.time.get_ticks()
            cutscene_dt = (current_time - last_time) / 1000.0 * 60
            last_time = current_time

            # Handle events during cutscene
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.save_progress()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cutscene_running = False

            # Clear screen
            screen.fill(BLACK)

            # Update elapsed time
            elapsed_time = current_time - cutscene_start_time
            frames_elapsed = elapsed_time / 16.67  # Convert to frames

            # Calculate alpha based on phase
            if frames_elapsed < FADE_IN_TIME:
                # Fade in
                alpha = int((frames_elapsed / FADE_IN_TIME) * 255)
            elif frames_elapsed < FADE_IN_TIME + PAUSE_TIME:
                # Hold
                alpha = 255
            elif frames_elapsed < TOTAL_TIME:
                # Fade out
                remaining = TOTAL_TIME - frames_elapsed
                alpha = int((remaining / FADE_OUT_TIME) * 255)
            else:
                cutscene_running = False
                self.day_cutscene_activated = True
                break

            # Draw text with current alpha
            text_surface = pygame.Surface(day_text.get_size(), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, alpha))
            text_surface.blit(day_text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(text_surface, text_pos)

            pygame.display.update()
            clock.tick(60)

    
    def play_night_cutscene(self):
        cutscene_running = True
        last_time = pygame.time.get_ticks()
        cutscene_start_time = last_time

        # Create text surface
        text = font.render("Night Falls", True, colors['red'][3])
        text_pos = [width/2 - text.get_width()/2, height/2 - text.get_height()/2]

        # Timing constants 
        FADE_IN_TIME = 60  # 1 second fade in
        PAUSE_TIME = 60    # 1 second pause
        FADE_OUT_TIME = 60 # 1 second fade out
        TOTAL_TIME = FADE_IN_TIME + PAUSE_TIME + FADE_OUT_TIME

        while cutscene_running and not self.night_cutscene_activated:
            current_time = pygame.time.get_ticks()
            cutscene_dt = (current_time - last_time) / 1000.0 * 60
            last_time = current_time

            # Handle events during cutscene
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.save_progress()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cutscene_running = False

            # Clear screen
            screen.fill(BLACK)

            # Update elapsed time
            elapsed_time = current_time - cutscene_start_time
            frames_elapsed = elapsed_time / 16.67  # Convert to frames

            # Calculate alpha based on phase
            if frames_elapsed < FADE_IN_TIME:
                # Fade in
                alpha = int((frames_elapsed / FADE_IN_TIME) * 255)
            elif frames_elapsed < FADE_IN_TIME + PAUSE_TIME:
                # Hold
                alpha = 255
            elif frames_elapsed < TOTAL_TIME:
                # Fade out
                remaining = TOTAL_TIME - frames_elapsed
                alpha = int((remaining / FADE_OUT_TIME) * 255)
            else:
                cutscene_running = False
                self.night_cutscene_activated = True
                break

            # Draw text with current alpha
            text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, alpha))
            text_surface.blit(text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(text_surface, text_pos)

            pygame.display.update()
            clock.tick(60)


    def update(self):
        self.game_time = 1
        
        if self.shake_time > 0:
            self.shake_time -= 1 * dt
            screen_shake(15)
        if self.slow_time > 0:
            self.slow_time -= 1 * dt
            self.game_time = 0.005
            
        self.daynight_value += 1 / 1000 * dt
        self.daynight = math.sin(self.daynight_value)
        
        if self.daynight > 0:

            # set false for next cutscene
            if self.night_cutscene_activated:
                self.night_cutscene_activated = False
            
            # one time activator
            if not self.day_cutscene_activated:
                meteor_array.clear()
                self.background_color = self.sky_color
                self.mountains = mountain_image
                self.play_day_cutscene()
                
            
            if len(mushroom_array) < self.mushroom_counts:
                self.mushroom_ticker += 1 * dt

            if self.mushroom_ticker > self.mushroom_spawn_cd:
                self.spawn_mushrooms()
                self.mushroom_ticker = 0

            if not self.daynight_tswitch:
                self.flash_in()
                self.maintiles = [self.grass, self.soil]
                self.daynight_tswitch = True

        else:

            # set false for next cutscene
            if self.day_cutscene_activated:
                self.day_cutscene_activated = False

            # one time activator
            if not self.night_cutscene_activated:
                self.background_color = self.night_sky_color
                self.mountains = mountain_image_night
                self.play_night_cutscene()
            
            '''

            # Regular meteor spawning
            # NEED PERFORMANCE IMPROVEMENT, NOT RENDER PROBLEM BUT DATA LOAD CALCULATED OUTSIDE OF VISIBLE RANGE IS DRAGGING PERFORMANCE
            self.meteor_timer += dt * environment.game_time
            if self.meteor_timer >= self.meteor_spawn_rate:
                self.meteor_timer = 0
                meteor_array.append(Meteor())
            '''

            # Sequence attack handling
            if self.sequence_active:
                self.sequence_timer += dt * environment.game_time
                if self.sequence_timer >= self.sequence_interval:
                    self.sequence_timer = 0
                    self.spawn_sequence_meteor()
                    self.sequence_count += 1
                    
                    if self.sequence_count >= self.max_sequence:
                        self.sequence_active = False
                        self.sequence_count = 0

            # Start new sequence
            elif self.targeted_attack_timer >= self.targeted_attack_rate:
                self.targeted_attack_timer = 0
                self.sequence_active = True
                self.sequence_timer = 0
                self.sequence_count = 0
                self.sequence_target = [player_pos_raw[0], player_pos_raw[1]]
                # Spawn first meteor immediately
                self.spawn_sequence_meteor()
                
            else:
                self.targeted_attack_timer += dt
            
            # kill mushrooms area 1
            self.mushroom_die_ticker += 1 * dt
            for i in mushroom_array:
                if self.mushroom_die_ticker > self.mushroom_die_cd:
                    i.end()
                    self.mushroom_die_ticker = 0

            # kill mushrooms area 2
            for i in mushroom_array_2:
                if self.mushroom_die_ticker > self.mushroom_die_cd:
                    i.end()
                    self.mushroom_die_ticker = 0
            
            if self.daynight_tswitch:
                self.fade_in()
                self.maintiles = [self.grass_night, self.soil_night]
                self.daynight_tswitch = False
            
            
            self.daynight_inverse = math.cos(self.daynight_value)

    def render(self):
        screen.fill(self.background_color)
        for i in range(5):
            screen.blit(self.mountains, 
                       [offset[x] / 10 - width + width * i + self.mountain_pos_x, 
                        offset[y] / 3])

    def spawn_mushrooms(self):
        a = [-width, -width / 3]
        b = [width / 3, width]
        
        m = min([len(mushroom_array), len(mushroom_array_2)])

        if m == len(mushroom_array):
            mushroom_array.append(Mushroom(range=a))
        if m == len(mushroom_array_2):
            mushroom_array_2.append(Mushroom(range=b))
    
    def spawn_sequence_meteor(self):
        meteor_array.append(Meteor(self.sequence_target, True, self.sequence_count))


    def tile_render(self):
            for tile in self.tile_array:
                if tile[1] == 'grass':
                    screen.blit(self.maintiles[0], [tile[0][x] + offset[x], tile[0][y] + offset[y]])
                else:
                    screen.blit(self.maintiles[1], [tile[0][x] + offset[x], tile[0][y] + offset[y]])

    def fade_in(self):
        self.fading_in = True
        self.fade = 255
        self.fading_out = False

    def fade_out(self):
        self.fading_out = True
        self.fade = 0
        self.fading_in = False

    def flash_in(self):
        self.flashing_in = True
        self.flash = 255
        self.flashing_out = False

    def flash_out(self):
        self.flashing_out = True
        self.flash = 0
        self.flashing_in = False

    def kill_flash(self):
        self.flashing_in = True
        self.flash = 255 // 5
        self.flashing_out = False

    def render_effects(self):
        if self.fading_in or self.fading_out:
            if self.fading_in and self.fade > 0:
                self.fade -= 1 * dt
            else:
                self.fading_in = False
            if self.fading_out and self.fade < 255:
                self.fade += 1 * dt
            else:
                self.fading_out = False
            screen.blit(fades[int(self.fade)], [0, 0])

        if self.flashing_in or self.flashing_out:
            if self.flashing_in and self.flash > 0:
                self.flash -= 1 * dt
            else:
                self.flashing_in = False
            if self.flashing_out and self.flash < 255:
                self.flash += 1 * dt
            else:
                self.flashing_out = False
            screen.blit(flashes[int(self.flash)], [0, 0])

    def slow_motion(self, time=15):
        if self.slow_time < 1:
            self.slow_time += time

    def shake(self, time=20):
        self.shake_time += time

class KillStreak:
    def __init__(self):
        self.kill_timer = 0
        self.kill_count = 0
        self.kill_window = 50
        self.roman_numerals = {
            3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII',
            8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI',
            12: 'XII', 13: 'XIII', 14: 'XIV', 15: 'XV'
        }
        self.MAX_ALPHA = int(255 * 0.85)
        self.fade_duration = 8
        self.font_size = height * 0.5
        self.display_timer = 0
        self.streak_font = pygame.font.Font(font_name, int(self.font_size))
        self.current_message = None
        
        # Pre-render all possible text surfaces and find max size
        self.text_surfaces = {}
        max_width = 0
        max_height = 0
        for num, roman in self.roman_numerals.items():
            text_surface = self.streak_font.render(roman, True, (255, 255, 255))
            max_width = max(max_width, text_surface.get_width())
            max_height = max(max_height, text_surface.get_height())
            self.text_surfaces[num] = {
                'surface': text_surface,
                'x': (width - text_surface.get_width()) // 2,
                'y': height * 0.16
            }
        
        # Create temp surface for blending
        self.temp_surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
        
        # Pre-calculate alpha frames
        self.alpha_frames = []
        num_frames = 60  # Number of transition frames
        for i in range(num_frames + 1):
            progress = i / num_frames
            eased_alpha = self.cubic_ease_out(progress)
            alpha_value = int(eased_alpha * self.MAX_ALPHA)
            
            # Create alpha surface for this frame
            alpha_surf = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
            alpha_surf.fill((255, 255, 255, alpha_value))
            self.alpha_frames.append(alpha_surf)

    def cubic_ease_out(self, t):
        return 1 - (1 - t) ** 2

    def add_kill(self):
        if self.kill_timer > 0:
            self.kill_count += 1
            if self.kill_count >= 3:
                self.show_streak_message()
        else:
            self.kill_count = 1
        
        self.kill_timer = self.kill_window

    def show_streak_message(self):
        kill_count = min(self.kill_count, max(self.roman_numerals.keys()))
        self.current_message = kill_count
        self.display_timer = self.fade_duration

    def render(self):
        if self.kill_timer > 0:
            self.kill_timer = max(0, self.kill_timer - dt)
        
        if self.display_timer > 0 and self.current_message:
            self.display_timer = max(0, self.display_timer - dt)
            
            # Calculate which alpha frame to use
            frame_index = int((self.display_timer / self.fade_duration) * len(self.alpha_frames))
            frame_index = min(len(self.alpha_frames) - 1, max(0, frame_index))
            
            text_data = self.text_surfaces[self.current_message]
            
            # Reuse temp surface
            self.temp_surface.fill((0, 0, 0, 0))  # Clear temp surface
            self.temp_surface.blit(text_data['surface'], (0, 0))
            self.temp_surface.blit(self.alpha_frames[frame_index], (0, 0), 
                            (0, 0, text_data['surface'].get_width(), text_data['surface'].get_height()), 
                            special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(self.temp_surface, (text_data['x'], text_data['y']))

class Player:
    def __init__(self):

        self.max_health = 100
        self.current_health = self.max_health
        self.is_hit = False
        self.hit_timer = 0
        self.hit_recover_time = 20  # Invincibility frames

        self.image_raw = player_image.copy()
        self.weapons = []
        self.current_weapon = 0
        self.weapon = 0
        self.rotation_target = 0
        self.rotation = 0
        self.image = self.image_raw
        self.pos = [width / 3, 0]
        self.steps = self.pos[x]
        self.attitude = self.pos[y]
        self.gravity = 20
        self.jump_count = 0
        self.jumping = False
        self.velo_x = 0
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.centered = self.width / 2, self.height / 2
        self.flipped = False

        # Add map constraints
        self.map_start = -width * 2  # Left boundary
        self.map_end = width * 3  # Right boundary
        self.last_safe_y = self.pos[y]  # For void fall recovery
    

    def take_damage(self, damage):
        if not self.is_hit:
            self.current_health -= damage
            self.is_hit = True
            self.hit_timer = 0
            if self.current_health <= 0:
                self.current_health = 0
                # Add death handling here if needed
            effects_array.append(Particles(
                [player_pos_raw[x], player_pos_raw[y]], 
                count=15, 
                color=[255, 0, 0], 
                size=6,
                gravity=True
            ))
    
    def update(self):
        # Add this to your existing update method
        if self.is_hit:
            self.hit_timer += 1 * dt
            if self.hit_timer >= self.hit_recover_time:
                self.is_hit = False
                self.hit_timer = 0
        
        self.centered = self.image.get_width() / 2, self.image.get_height() / 2
        self.pos[y] += self.gravity * dt
        self.attitude += self.gravity * dt
        if self.gravity < 20 and self.pos[y] < floor - self.height:
            self.gravity += 2 * dt
        

        # Handle map wrapping
        if self.steps < self.map_start:
            # If player goes too far left, wrap to right
            self.steps = self.map_end - 100

        elif self.steps > self.map_end:
            # If player goes too far right, wrap to left
            self.steps = self.map_start + 100

        # Handle void falling
        if self.pos[y] > height * 1.5:  # If fallen too far
            self.pos[y] = floor - self.height  # Reset to floor level
            self.steps = width / 2  # Center horizontally
            self.gravity = 0  # Reset gravity
            self.jump_count = 0  # Reset jumps

        # Update last safe Y position when on ground
        if self.pos[y] == floor - self.height:
            self.last_safe_y = self.pos[y]
            
        self.pos[x] += self.velo_x * dt
        self.steps += self.velo_x * dt
        self.velo_x = 0

        if self.pos[y] > floor - self.height:
            self.gravity = 0
            self.jump_count = 0

        if moving_L:
            self.velo_x = -10
            self.rotation_target = 20
        elif moving_R:
            self.velo_x = 10
            self.rotation_target = -20

        if cursor_angle > 0:
            if self.flipped:
                self.image_raw = pygame.transform.flip(self.image_raw, True, False)
                self.flipped = False
        else:
            if not self.flipped:
                self.image_raw = pygame.transform.flip(self.image_raw, True, False)
                self.flipped = True

        if not moving_L and not moving_R:
            self.rotation_target = 0

        self.rotation += ((self.rotation_target - self.rotation) / 10) * dt
        self.image = pygame.transform.rotate(self.image_raw, self.rotation)

    def jump(self):
        if self.jump_count < 3:
            self.gravity = -30
            self.jump_count += 1
            effects_array.append(Particles([player_pos_raw[x], player_pos_raw[y] + player.height], 5))

    def switch_weapon(self, con):
        if con == 1 and self.current_weapon < len(self.weapons) - 1:
            effects_array.append(Particles(weapon_pos, 15, size=6, speed=0.8, color=[255, 0, 255], size_change=3))
            self.current_weapon += con
            environment.slow_motion()
        elif con == -1 and self.current_weapon > 0:
            effects_array.append(Particles(weapon_pos, 15, size=6, speed=0.8, color=[255, 255, 0], size_change=3))
            self.current_weapon += con
            environment.slow_motion()
        self.weapon = self.weapons[self.current_weapon]
        select_sound.play()

    def render(self):
        # Health bar
        health_width = ((self.width * self.current_health) / self.max_health)
        health_pos = [player_pos[x] - self.centered[x], player_pos[y] - 20]
        pygame.draw.rect(screen, (255, 0, 0), 
                        (health_pos[0], health_pos[1] - 10, self.width, 10))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (health_pos[0], health_pos[1] - 10, health_width, 10))
        
        screen.blit(self.image, [player_pos[x] - self.centered[x], player_pos[y]])

class Meteor:
    def __init__(self, target_pos=None, is_targeted=False, sequence_index=0):
        self.image = mushroom_image_idle.copy()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.centered = [self.width/2, self.height/2]  # Add this line
        self.is_targeted = is_targeted
        self.blood = colors['red'][20]  # For particle effects
        
        # Health properties
        self.hp = 20
        self.max_hp = 20
        self.hitted = False
        self.tpos = [0, 0]
        self.exp = 150
        
        # Sequence attack properties
        self.sequence_index = sequence_index
        sequence_offset = sequence_index * 100 # Space between sequential meteors
        
        if target_pos and is_targeted:
            self.target_x = target_pos[0] + sequence_offset
            spawn_x = self.target_x + random.randint(-100, 100)
        else:
            spawn_x = random.randint(int(-width* 2), int(width * 3))
            self.target_x = spawn_x

        # Projectile motion properties
        self.pos = [spawn_x, -height]
        self.velocity = [0, 0]
        self.gravity = 0.1
        self.damage = 20
        
        # Calculate initial velocity for projectile motion
        if is_targeted:
            target_y = target_pos[1]
            dx = self.target_x - self.pos[0]
            dy = target_y - self.pos[1]
            # Adjust these values to change projectile arc
            self.velocity[0] = dx * 0.05
            self.velocity[1] = dy * 0.05 - 10  # Initial upward velocity for arc
        else:
            self.velocity = [random.uniform(-5, 5), random.uniform(-15, -10)]

        self.angle = 0
        
        # Trail particles
        self.trail_timer = 0
        self.trail_interval = 0.5

        # Add these new attributes for destruction sequence
        self.has_hit_player = False  # Add this to track if already hit player
        self.hit_radius = self.width * 0.5  # Adjust this value to change hit detection area

        if target_pos and is_targeted:
            # All meteors aim for same target point
            self.target_x = target_pos[0]
            self.target_y = target_pos[1]
            
            # Calculate spawn position along a line
            spawn_distance = 1000  # Distance from target to first spawn point
            spawn_angle = random.choice((math.pi * 1/2, math.pi * 1/3 / 1.2, math.pi * 2/3 * 1.2))  # degrees: 90, 60, 120 steepened
            
            # Space meteors along the line based on index
            self.pos = [
                self.target_x - spawn_distance * math.cos(spawn_angle),
                -height/2 - sequence_index * 200  # Higher spawn for later meteors
            ]
            
            # Calculate velocity to hit target
            dx = self.target_x - self.pos[0]
            dy = self.target_y - self.pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Fixed speed for consistent timing
            speed = 20
            self.velocity = [
                dx / distance * speed,
                dy / distance * speed
            ]


    def get_hit(self, obj):
        self.tpos[x] = self.pos[x] + (math.sin(weapon_angle)) * obj.damage * 10
        self.tpos[y] = self.pos[y] + (math.cos(weapon_angle)) * obj.damage * 10
        self.hp -= obj.damage
        hit_sound.play()
        self.hitted = True

    def create_explosion(self):

        # Remove from render array if present
        if self in render_array:
            render_array.remove(self)
        if self in meteor_array:
            meteor_array.remove(self)

        effects_array.append(Explosion(self.pos, color_base=[255, 100, 0], count=15))


        
        screen_shake(30)
        explode_sound.play()
    
    def end(self):
        # Same as mushroom's end method
        for i in entities_array:
            if self in i:
                i.remove(self)
        
        self.create_explosion()
        die_sound.play()
        game.exp += self.exp
        game.gold += (self.exp * random.randint(5, 15) / 10)
        environment.slow_motion(time=10)
        environment.kill_flash()
        game.save_progress()


    def update(self):

        # Check if meteor is destroyed by damage
        if self.hp <= 0:
            killstreak.add_kill()
            self.end()  # Use end() instead of just create_explosion()
            screen_shake(100)
            return True

        # Apply gravity and update position
        self.velocity[1] += self.gravity * dt
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        
        # Update angle based on velocity
        self.angle = math.atan2(self.velocity[1], self.velocity[0])
        
        # Create trail particles
        self.trail_timer += dt
        if self.trail_timer >= self.trail_interval and (0 < self.pos[x] + offset[x] < width and 0 < self.pos[y] + offset[y]):
            self.trail_timer = 0
            effects_array.append(GlowingParticles(
                self.pos,
                count=1,
                size=15,
                color="#d20d15",
                speed=0.5,
                size_change=5,
                gravity=False
            ))

        # Handle hit states
        if self.hitted:
            self.pos[x] += (self.tpos[x] - self.pos[x]) / 6 * dt
            if self.tpos[x] - 10 < self.pos[x] < self.tpos[x] + 10:
                self.hitted = False


        # Check collision with player - only if haven't hit player yet
        # Check collision with player using position
        if not self.has_hit_player:
            # Calculate distance between meteor and player
            dx = self.pos[0] - player_pos_raw[0]
            dy = self.pos[1] - player_pos_raw[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            # If within hit radius
            if distance < self.hit_radius + player.width/3:
                player.take_damage(self.damage)
                self.has_hit_player = True
                self.create_explosion()
                screen_shake(160)
                
                return True

        # Ground collision check
        if self.pos[1] > floor:
            self.create_explosion()
            self.velocity = [0, 0]
            return False
            
        return False

    def render(self):
        # Draw health bar
        p = [self.pos[x] - self.width/2 + offset[x],
             self.pos[y] - self.height + offset[y]]
        draw_bar([p[x] + self.width/2, p[y] - 30], self.hp, self.max_hp)
        
        # Draw meteor
        rotated = pygame.transform.rotate(
            self.image, 
            -math.degrees(self.angle) - 90
        )
        screen.blit(
            rotated,
            [self.pos[0] - rotated.get_width()/2 + offset[0],
             self.pos[1] - rotated.get_height()/2 + offset[1]]
        )

class Mushroom:
    def __init__(self, range=[width / 2, width / 1.5]):
        self.blood = colors['red'][16]
        self.range = range
        self.image = mushroom_image_idle.copy()
        self.pos = [random.randint(int(self.range[0]), int(self.range[1])), floor * 0.8]
        self.tpos = [0, 0]
        self.gravity = 20
        self.hp = 100
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.centered = self.width / 2, self.height / 2
        self.target_pos = random.randint(int(range[0]), int(range[1]))
        self.linear_motion = (self.target_pos - self.pos[x]) / 100
        self.switched_target = False
        self.rested_time = 0
        self.rest_time = 500
        self.rest = False
        self.displacement = self.target_pos - self.pos[x]
        self.touch_down = False
        self.jumping = False
        self.cd = 0
        self.cded = False
        self.cdtime = random.randint(40, 80)
        self.hitted = False
        self.exp = 10
        effects_array.append(Particles(self.pos, count=10, size=9, color=colors['red'][18], size_change=3))

    def get_target(self):
        self.target_pos = random.randint(int(self.range[0]), int(self.range[1]))
        self.displacement = self.target_pos - self.pos[x]
        self.linear_motion = self.displacement / 100
        a = random.randint(1, 3)
        if a == 3:
            self.rest = True

    def update(self):
        if self.hp < 1:
            self.end()
            if player.current_health <= 95:
                player.current_health += 5
            else:
                player.current_health = 100
            effects_array.append(HealthText(5, player_pos_raw))

            game.exp += self.exp
            game.gold += (self.exp * random.randint(5, 15) / 10)
        if self.jumping and self.pos[y] == floor:
            self.pos[y] += self.gravity * dt
        if self.gravity < 20:
            self.gravity += 0.8 * dt
        if self.pos[y] < floor:
            self.pos[y] += self.gravity * dt
        else:
            self.jumping = False
            self.pos[y] = floor
            if not self.touch_down:
                effects_array.append(Particles(self.pos, count=10, size=9, color=colors['red'][21], size_change=3))
                if is_on_screen(self):
                    screen_shake(30)
                self.touch_down = True
        if not self.rest and self.jumping:
            self.pos[x] += self.linear_motion * dt
        if self.displacement > 0:
            if self.pos[x] > self.target_pos:
                self.get_target()
        else:
            if self.pos[x] < self.target_pos:
                self.get_target()
        if self.rest:
            self.rested_time += 1 * dt
            if self.rested_time > self.rest_time:
                self.rested_time = 0
                self.rest = False
        elif self.cd > self.cdtime and self.pos[y] == floor:
            self.cd = 0
            self.jump()
            self.touch_down = False
        self.cd += 1 * dt
        if self.hitted:
            self.pos[x] += (self.tpos[x] - self.pos[x]) / 6 * dt
            if self.tpos[x] - 10 < self.pos[x] < self.tpos[x] + 10:
                self.hitted = False

    def get_hit(self, obj):
        self.tpos[x] = self.pos[x] + (math.sin(weapon_angle)) * obj.damage * 10
        self.tpos[y] = self.pos[y] + (math.cos(weapon_angle)) * obj.damage * 10
        self.hp -= obj.damage
        hit_sound.play()
        self.hitted = True

    def jump(self):
        self.jumping = True
        self.gravity = -16

    def end(self):
        
        for i in entities_array:
            if self in i:
                i.remove(self)
        effects_array.append(Explosion(self.pos, color_base=colors['red'][21], count=20))
        die_sound.play()
        game.save_progress()

    def render(self):
        p = [self.pos[x] - self.centered[x] + offset[x],
             self.pos[y] - self.height + offset[y]]
        screen.blit(self.image, [p[x], p[y]])
        draw_bar([p[x] + self.centered[x] / 2, p[y] - 30], self.hp, 100)

class Stargazer:
    def __init__(self):
        self.name = 'StarGazer'
        self.capacity = 40
        self.unit = self.capacity
        self.damage = 7
        self.check = 3
        self.reset_time = 2
        self.cd_time = 40
        self.cd = 0
        self.ready = False
        self.image_raw = stargazer_image.copy()
        self.image_raw = pygame.transform.scale(self.image_raw, [width * 0.1, width * 0.1])
        self.image = pygame.transform.rotate(self.image_raw, weapon_rotation)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.centered = self.image_raw.get_width() / 2, self.image_raw.get_height() / 2
        self.pos = weapon_pos
        self.flipped = False
        self.image_base = self.image_raw

    def update(self):
        self.check += 1 * dt
        self.pos = weapon_pos
        self.image = pygame.transform.rotate(self.image_raw, weapon_rotation)
        self.centered = self.image.get_width() / 2, self.image.get_height() / 2
        if cursor_angle < 0:
            if not self.flipped:
                self.image_raw = pygame.transform.flip(self.image_raw, False, True)
                self.flipped = True
        elif self.flipped:
            self.image_raw = pygame.transform.flip(self.image_raw, False, True)
            self.flipped = False
        if self.check > self.reset_time:
            self.ready = True
        if self.unit == 0:
            self.cd += 1 * dt
            if self.cd >= self.cd_time:
                self.unit = self.capacity
                self.cd = 0

    def render(self):
        screen.blit(self.image, [self.pos[x] - self.centered[x] + offset[x],
                                self.pos[y] - self.centered[y] + offset[y]])

    def render_hud(self):
        draw_bar([20 * scale_width, 20 * scale_height], self.unit,
                 self.capacity, size=2.5, color=colors['blue'][18], line=True)
        draw_bar([20 * scale_width, 70 * scale_height], self.cd,
                 self.cd_time, size=2.5, color=colors['green'][18])
        screen.blit(self.image_base, [30 * scale_width, 70 * scale_height])
        draw_text(f'{self.unit} / {self.capacity}', 230 * scale_width, 30 * scale_height)

    def attack(self):
        if self.ready and self.unit > 0:
            dmg = self.damage
            a = random.randint(1, 7)
            c = False
            if a == 5:
                dmg **= 1.2
                c = True
            render_array.append(Bullet(
                                image=stargazer_bullet_image, 
                                speed=60, 
                                damage=dmg, 
                                critical=c,
                                )
                            )
            shoot_sound.play()
            self.check = 0
            self.ready = False
            screen_shake(15)
            self.unit -= 1

class Shotgun:
    def __init__(self):
        self.name = 'Hades'
        self.capacity = 3
        self.unit = self.capacity
        self.damage = 20
        self.check = 60
        self.ready = False
        self.cd_time = 80
        self.cd = 0
        self.reset_time = 10
        self.image_raw = shotgun_image.copy()
        self.image_raw = pygame.transform.scale(self.image_raw, [width * 0.1, width * 0.1])
        self.image = pygame.transform.rotate(self.image_raw, weapon_rotation)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.centered = self.image_raw.get_width() / 2, self.image_raw.get_height() / 2
        self.pos = weapon_pos
        self.flipped = False
        self.image_base = self.image_raw

    def update(self):
        self.check += 1 * dt
        self.pos = weapon_pos
        self.image = pygame.transform.rotate(self.image_raw, weapon_rotation)
        self.centered = self.image.get_width() / 2, self.image.get_height() / 2
        if cursor_angle < 0:
            if not self.flipped:
                self.image_raw = pygame.transform.flip(self.image_raw, False, True)
                self.flipped = True
        elif self.flipped:
            self.image_raw = pygame.transform.flip(self.image_raw, False, True)
            self.flipped = False
        if self.check > self.reset_time and not self.ready:
            self.ready = True
        if self.unit == 0:
            self.cd += 1 * dt
            if self.cd >= self.cd_time:
                self.cd = 0
                self.unit = self.capacity

    def render(self):
        screen.blit(self.image, [self.pos[x] - self.centered[x] + offset[x],
                    self.pos[y] - self.centered[y] + offset[y]])

    def render_hud(self):
        draw_bar([20 * scale_width, 20 * scale_height], self.unit,
                self.capacity, size=2.5, color=colors['blue'][19], line=True)
        draw_bar([20 * scale_width, 70 * scale_height], self.cd,
                self.cd_time, size=2.5, color=colors['red'][19])
        screen.blit(self.image_base, [30 * scale_width, 70 * scale_height])
        draw_text(f'{self.unit} / {self.capacity}', 230 * scale_width, 30 * scale_height)

    def attack(self):
        if self.ready and self.unit > 0:
            for i in range(5):
                dmg = self.damage
                a = random.randint(1, 7)
                c = False
                if a == 5:
                    c = True
                    dmg **= 1.2
                render_array.append(Bullet(recoil=200, exploded_color=[255, 0, 0],
                                        shake=30, speed=30, damage=dmg, critical=c))
            screen_shake(50)
            shoot_sound.play()
            self.check = 0
            self.ready = False
            self.unit -= 1

class WeaponShop:
    def __init__(self, pos):
        self.weapon_arr = [Stargazer(), Shotgun()]
        self.weapons_d = self.weapon_arr.copy()
        self.weapons_centered = get_centered(self.weapons_d[0].image_raw)
        for i in range(len(self.weapons_d)):
            self.weapons_d[i].image_raw = pygame.transform.scale(self.weapons_d[i].image_raw, [width / 5] * 2)
        self.image_arr = [weaponshop_image, weaponshopselect_image]
        self.image = self.image_arr[0]
        self.centered = get_centered(self.image)
        self.pos = [pos[x] - self.centered[x], pos[y] - self.centered[y] * 2]
        self.ready = False
        self.choice = 0
        self.scroll = 0
        for i in range(len(self.weapons_d)):
            if i != self.choice:
                self.weapons_d[i].image_raw.set_alpha(100)
            else:
                self.weapons_d[i].image_raw.set_alpha(255)

    def update(self):
        self.ready = False
        self.image = self.image_arr[0]
        if self.pos[x] <= player_pos_raw[x] <= self.pos[x] + self.centered[x] * 2:
            if player_pos_raw[y] > self.pos[y] - self.centered[y]:
                self.image = self.image_arr[1]
                draw_text('Press E to enter', self.pos[x] + offset[x], self.pos[y] + offset[y])
                self.ready = True
        if self.ready and pygame.key.get_pressed()[pygame.K_e]:
            self.run()

    def render(self):
        screen.blit(self.image, [self.pos[x] + offset[x], self.pos[y] + offset[y]])

    def run(self):
        global dt, last_frame
        last_frame = pygame.time.get_ticks()
        dt = 0
        r = True
        while r:
            dt = delta_to_modifier(pygame.time.get_ticks() - last_frame)
            last_frame = pygame.time.get_ticks()
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.save_progress()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        r = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if self.choice - 1 >= 0:
                            self.choice -= 1
                    elif event.button == 5:
                        if self.choice + 1 <= len(self.weapons_d) - 1:
                            self.choice += 1
                    for i in range(len(self.weapons_d)):
                        if i != self.choice:
                            self.weapons_d[i].image_raw.set_alpha(100)
                        else:
                            self.weapons_d[i].image_raw.set_alpha(255)
            screen.fill(BLACK)
            tposy = height * 3 / 4 / 2
            draw_text_sizeable(self.weapons_d[self.choice].name, width * 3 / 4, tposy, size=width / 20)
            draw_text(f'DMG {self.weapons_d[self.choice].damage}', width * 2 / 3, tposy + 100)
            draw_text(f'RELOAD {self.weapons_d[self.choice].reset_time}', width * 2 / 3, tposy + 170)
            self.posy = height / 3 * self.choice
            self.scroll += (self.posy - self.scroll) / 10 * dt
            for i in range(len(self.weapons_d)):
                p = height / 2 - self.scroll + height / 3 * i - self.weapons_centered[y] * 2
                screen.blit(self.weapons_d[i].image_raw, [width / 4, p])
            game.render_ui()
            draw_circle(mouse_pos)
            pygame.display.update()
            clock.tick(-1)

class Bullet:
    def __init__(self, recoil=50, damage=10, speed=50, image=shotgun_bullet_image,
                exploded_color=[255, 255, 255], shake=15, critical=False):
        self.image_raw = image.copy()
        self.angle = recoil_angle(recoil)
        self.shake = shake
        self.exploded_color = exploded_color
        self.damage = damage
        self.critical = critical
        self.rotation = (180 / math.pi) * self.angle - 90
        self.image = pygame.transform.rotate(self.image_raw, self.rotation)
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.centered = self.width / 2, self.height / 2
        self.pos = [weapon.image.get_width() * 0.5 * math.sin(weapon_angle) + weapon_pos[x],
                    weapon.image.get_height() * 0.5 * math.cos(weapon_angle) + weapon_pos[y]]
        self.speed = speed
        if player.gravity > 0:
            player.gravity /= 2

    def update(self):
        self.rect = self.image.get_rect()
        self.pos[x] += math.sin(self.angle) * self.speed * dt
        self.pos[y] += math.cos(self.angle) * self.speed * dt
        if not self.pos[y] < floor:
            self.end(effect=Explosion(self.pos))
        elif not is_on_screen(self):
            self.end(sound=False, shake=False)
        effects_array.append(Particles(self.pos, 1, size=6, speed=0.8, color=[255, 255, 255], size_change=6))

    def render(self):
        screen.blit(self.image, [self.pos[x] - self.centered[x] + offset[x],
                                    self.pos[y] - self.centered[y] + offset[y]])

    def end(self, effect=None, sound=True, shake=True):
        render_array.remove(self)
        effects_array.append(Explosion(pos=self.pos, color_base=self.exploded_color, count=3, size=0.9))

        if sound:
            explode_sound.play()
        if shake:
            screen_shake(self.shake)

class Explosion:
    def __init__(self, pos, color_base=[255, 255, 255], count=5, size=1, angle=1):
        self.pos = pos
        self.size = size
        self.particles = []
        self.angle = angle
        
        for i in range(count):
            subbed = random.randint(0, 70)
            
            # Convert base color to RGB if it's a hex string
            color_base_rgb = hex_to_rgb(color_base) if isinstance(color_base, str) else color_base
            
            particle_size = random.randint(int(width * 0.008 * self.size),
                                         int(width * 0.03 * self.size * self.size))
            
            self.particles.append([
                [pos[x], pos[y]],  # Position
                [random.randint(int(-width / 200), int(width / 200)),  # Velocity X
                 random.randint(int(-height / 200), int(height / 200))],  # Velocity Y
                particle_size,  # Size
                [max(0, min(255, abs(color_base_rgb[0] - subbed))),  # Color with variation
                 max(0, min(255, abs(color_base_rgb[1] - subbed))),
                 max(0, min(255, abs(color_base_rgb[2] - subbed))),
                 255]  # Full alpha for main particle
            ])

    def render(self):
        position = 0
        velocity = 1
        size = 2
        color = 3
        
        # If no particles left, remove effect from effects_array
        if not self.particles:
            effects_array.remove(self)
            return True
            
        for i in self.particles[:]:  # Create a copy for safe iteration
            # Update position
            i[position][x] += i[velocity][x] * self.angle * dt
            i[position][y] += i[velocity][y] * self.angle * dt
            i[size] -= height / 1000 * dt
            
            if i[size] <= 0:
                self.particles.remove(i)
            else:
                # Create surface for the glowing particle
                glow_surface = pygame.Surface((int(i[size] * 3), int(i[size] * 3)), pygame.SRCALPHA)
                
                # Draw outer glow (larger, very transparent)
                glow_color = (*i[color][:3], 30)  # Low alpha for outer glow
                pygame.draw.circle(glow_surface, glow_color,
                                (int(i[size] * 1.5), int(i[size] * 1.5)),
                                int(i[size] * 1.5))
                
                # Draw middle glow (medium transparency)
                middle_color = (*i[color][:3], 180)  # Medium alpha for middle glow
                pygame.draw.circle(glow_surface, middle_color,
                                (int(i[size] * 1.5), int(i[size] * 1.5)),
                                int(i[size] * 1.2))
                
                # Draw main particle
                pygame.draw.circle(glow_surface, i[color],
                                (int(i[size] * 1.5), int(i[size] * 1.5)),
                                i[size])
                
                # Blit the combined surface
                screen.blit(glow_surface,
                        (i[position][x] + offset[x] - i[size] * 1.5,
                            i[position][y] + offset[y] - i[size] * 1.5))
        
        return False

class Particles:
    def hex_to_rgb(self, hex_color):
        """
        Convert a hex color to RGB.
        
        Args:
            hex_color (str or list): Hex color string or RGB list
        
        Returns:
            list: RGB color values (0-255)
        """
        # If already an RGB list, return as-is
        if isinstance(hex_color, list) and len(hex_color) == 3:
            return hex_color
        
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Convert hex to RGB
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    def __init__(self, pos, count, size=3, speed=1, color='#000000', size_change=1, gravity=False):
        self.pos = pos
        self.particles = []
        self.sc = size_change
        self.gravity = gravity
        
        # Convert color to RGB
        color_rgb = self.hex_to_rgb(color)
        
        for i in range(count):
            subbed = random.randint(0, 40)
            self.particles.append([[pos[x], pos[y]],
                                [random.randint(int(-width / 200 * speed), int(width / 200 * speed)),
                                 random.randint(int(-height / 200 * speed), int(height / 200 * speed))],
                                random.randint(int(width / 1000 * size), int(width / 1000 * 2 * size)),
                                [max(0, min(255, abs(color_rgb[0] - subbed))), 
                                 max(0, min(255, abs(color_rgb[1] - subbed))), 
                                 max(0, min(255, abs(color_rgb[2] - subbed)))]])

    def render(self):
        position = 0
        velocity = 1
        size = 2
        color = 3

        if not self.particles:
            effects_array.remove(self)

        for i in self.particles[:]:  # Create a copy of the list to safely modify during iteration
            i[position][x] += i[velocity][x] * dt
            i[position][y] += i[velocity][y] * dt
            i[size] -= height / 5000 * self.sc * dt
            if self.gravity:
                i[position][y] += height / 500 * dt
            if not 0 < i[position][x] + offset[x] < width or not 0 < i[position][y] + offset[y] < height:
                self.particles.remove(i)
            elif i[size] <= 0:
                self.particles.remove(i)
            pygame.draw.circle(screen, i[color], [i[0][0] + offset[x],
                                            i[0][1] + offset[y]], i[2])               

class GlowingParticles:
    def hex_to_rgb(self, hex_color):
        """
        Convert a hex color to RGB.
        
        Args:
            hex_color (str or list): Hex color string or RGB list
        
        Returns:
            list: RGB color values (0-255)
        """
        if isinstance(hex_color, list) and len(hex_color) == 3:
            return hex_color
        
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    def __init__(self, pos, count, size=3, speed=1, color='#000000', size_change=1, gravity=False):
        self.pos = pos
        self.particles = []
        self.sc = size_change
        self.gravity = gravity
        
        # Convert color to RGB
        color_rgb = self.hex_to_rgb(color)
        
        for i in range(count):
            subbed = random.randint(0, 40)
            particle_size = random.randint(int(width / 1000 * size), int(width / 1000 * 2 * size))
            
            # Create particle with same structure as original, but add alpha value
            self.particles.append([
                [pos[x], pos[y]],  # Position
                [random.randint(int(-width / 200 * speed), int(width / 200 * speed)),  # Velocity X
                 random.randint(int(-height / 200 * speed), int(height / 200 * speed))],  # Velocity Y
                particle_size,  # Size
                [max(0, min(255, abs(color_rgb[0] - subbed))), 
                 max(0, min(255, abs(color_rgb[1] - subbed))), 
                 max(0, min(255, abs(color_rgb[2] - subbed))),
                 255]  # Color with alpha
            ])

    def render(self):
        position = 0
        velocity = 1
        size = 2
        color = 3

        
        
        # If no particles left, remove effect from effects_array
        if not self.particles:
            effects_array.remove(self)
            return True
        
        for i in self.particles[:]:  # Create a copy for safe iteration
            # Update position
            i[position][x] += i[velocity][x] * dt
            i[position][y] += i[velocity][y] * dt
            i[size] -= height / 5000 * self.sc * dt
            
            if self.gravity:
                i[position][y] += height / 500 * dt
            
            if not 0 < i[position][x] + offset[x] < width or not 0 < i[position][y] + offset[y] < height:
                effects_array.remove(self)
                return True
            elif i[size] <= 0.1:
                self.particles.remove(i)
            else:
                # Create single surface for both circles
                glow_surface = pygame.Surface((int(i[size] * 3), int(i[size] * 3)), pygame.SRCALPHA)
                
                # Calculate color that's 20% closer to white for main circle
                main_color = []
                for c in i[color][:3]:
                    # Lerp 20% towards white (255)
                    whitened = int(c + (255 - c) * 0.5)  # Move 20% of the distance to white
                    main_color.append(whitened)
                
                # Draw outer glow
                glow_color = (*i[color][:3], 5)  # Low alpha for outer glow
                pygame.draw.circle(glow_surface, glow_color,
                                (int(i[size] * 1.5), int(i[size] * 1.5)),
                                int(i[size] * 1.2))
                
                # Draw main particle with brightened color
                pygame.draw.circle(glow_surface, (*main_color, 255),
                                (int(i[size] * 1.5), int(i[size] * 1.5)),
                                i[size] * 0.7)
                
                # small inner circle as white core
                pygame.draw.circle(glow_surface, (*WHITE, 255),
                                (int(i[size] * 1.5), int(i[size] * 1.5)),
                                i[size] * 0.45)
                
                # Blit the combined surface with blend
                screen_x = i[position][x] + offset[x] - i[size] * 1.5
                screen_y = i[position][y] + offset[y] - i[size] * 1.5
                screen.blit(glow_surface, (screen_x, screen_y), special_flags=pygame.BLEND_RGB_ADD)
        
        return False

class Damage_text:
    def __init__(self, string, pos, color=colors['red'][20], critical=False, size=60):
        self.color = color
        self.critical = critical
        self.string = str(int(string))
        self.pos = pos
        self.tpos = self.pos[y] - 80
        self.truesize = 0
        self.size = 0
        self.tsize = size
        if critical:
            self.tsize = 130
            self.color = [255, 40, 40]

    def render(self):
        self.truesize += 12 / self.tsize * dt
        self.size = math.sin(self.truesize) * self.tsize
        draw_text_sizeable(self.string, self.pos[x] + offset[x], self.pos[y] + offset[y],
                           color=self.color, size=abs(self.size))
        self.pos[y] += ((self.tpos - self.pos[y]) / 5) * dt
        if self.size <= 0:
            effects_array.remove(self)

class HealthText:
    def __init__(self, heal_amount, pos, size=70):
        self.string = f"+{heal_amount}"
        self.pos = pos.copy()  # Make sure to copy position to not modify original
        self.tpos = self.pos[y] - 60  # Float up less than damage numbers
        self.truesize = 0
        self.size = 0
        self.tsize = size
        self.color = [40, 255, 40]  # Bright green for healing

    def render(self):
        self.truesize += 12 / self.tsize * dt * 0.5
        self.size = math.sin(self.truesize) * self.tsize
        
        # Draw text with + symbol
        draw_text_sizeable(self.string, self.pos[x] + offset[x], self.pos[y] + offset[y],
                          color=self.color, size=abs(self.size))
        
        # Float upward with smooth movement
        self.pos[y] += ((self.tpos - self.pos[y]) / 5) * dt
        
        # Remove when animation complete
        if self.size <= 0:
            effects_array.remove(self)


# utility function
def hex_to_rgb(hex_color):
    """
    Convert a hex color to RGB.
    
    Args:
        hex_color (str): Hex color string (with or without '#')
    
    Returns:
        list: RGB color values (0-255)
    """
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

def rgb_to_hex(rgb_color):
    """
    Convert RGB color to hex.
    
    Args:
        rgb_color (list): RGB color values (0-255)
    
    Returns:
        str: Hex color string
    """
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, int(rgb_color[0]))), 
        max(0, min(255, int(rgb_color[1]))), 
        max(0, min(255, int(rgb_color[2])))
    )

def blend_colors(night_sky_hex, sky_hex, daynight_factor):
    """
    Blend two hex colors based on a day/night factor.
    
    Args:
        night_sky_hex (str): Hex color for night sky
        sky_hex (str): Hex color for sky
        daynight_factor (float): Day/night blend factor (0-1)
    
    Returns:
        str: Blended hex color
    """
    # Convert hex to RGB
    night_sky_rgb = hex_to_rgb(night_sky_hex)
    sky_rgb = hex_to_rgb(sky_hex)
    
    # Blend colors
    blended_rgb = []
    for i in range(3):
        s = night_sky_rgb[i] - night_sky_rgb[i] * daynight_factor
        s += sky_rgb[i] * daynight_factor
        blended_rgb.append(max(0, min(255, int(s))))
    
    # Convert back to hex
    return rgb_to_hex(blended_rgb)


# Add with your other utility functions (near delta_to_modifier etc.)
def get_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def recoil_angle(magnitude):
    recoil = random.randint(1000 - magnitude, 1000 + magnitude)
    cursor_angle_recoiled = math.atan2(weapon_player_displacement[x], weapon_player_displacement[y])
    cursor_angle_recoiled += recoil / 1000 - 45
    return cursor_angle_recoiled

def screen_shake(magnitude):
    a = random.randint(int(width * magnitude / 10000 / 2), int(width * magnitude / 10000))
    offset[x] += random.choice([a, -a])
    b = random.randint(int(height * magnitude / 10000 / 2), int(height * magnitude / 10000))
    offset[y] += random.choice([b, -b])

def is_on_screen(obj):
    conda = 0 - obj.width < obj.pos[x] + offset[x] < width + obj.width
    condb = obj.pos[y] > -offset[y]
    return conda and condb

def collide(a, b):
    if b.pos[x] + offset[x] - b.centered[x] < a.pos[x] + offset[x] < b.pos[x] + offset[x] + b.centered[x]:
        if b.pos[y] + offset[y] - b.height < a.pos[y] + offset[y] < b.pos[y] + offset[y] + b.centered[y]:
            return True

def draw_text_sizeable(string, x, y, color=WHITE, size=10):
    s = pygame.font.Font(font_name, int(size))
    text = s.render(string, True, color)
    textRect = text.get_rect()
    textRect.center = [x, y]
    screen.blit(text, textRect)

def draw_multiline_text_right(lines, x, y, color=(255, 255, 255)):
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_width = text_surface.get_width()
        # Position from right edge (x) minus the width of current line
        screen.blit(text_surface, (x - text_width, y + i * (font.get_height() + 5)))

def draw_multiline_text_left(lines, x, y, color=(255, 255, 255)):
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        # All lines start at x position
        screen.blit(text_surface, (x, y + i * (font.get_height() + 5)))

# Initialize game objects
player = Player()
game = Game()
killstreak = KillStreak()


dt = 1
bg_pos = 0
bg_pos_targ = 0
offset_target = [0, 0]
offset = [0, height * 10]
last_frame = pygame.time.get_ticks()
moving_L = False
moving_R = False
player_pos_raw = [0, 0]
player_pos = [0, 0]
cursor_angle = 0
cursor_rotation = 0
cursor_player_displacement = 0
weapon_pos = [0, 0]
weapon_player_displacement = [0, 0]
weapon_angle = 0
weapon_rotation = 0


buildings_array = [
    WeaponShop([width / 2, floor]),

            ]

# for particles, more heavy objects
render_array = []

mushroom_array = []
mushroom_array_2 = []
meteor_array = []  # Add this new array

# for rendering entities mobs
entities_array = []
effects_array = [killstreak]


player.weapons = [Stargazer(), Shotgun()]

environment = Environment()
weapon = player.weapons[player.current_weapon]
environment.fade_in()
cam_osc_base = 0
cam_osc = [0, 0]

# Main game loop
while True:
    screen.fill(BLACK)
    dt = delta_to_modifier(pygame.time.get_ticks() - last_frame)
    environment.update()
    dt_alt = dt
    dt *= environment.game_time
    last_frame = pygame.time.get_ticks()
    cam_osc_base += 0.04 * dt
    cam_osc = [math.sin(cam_osc_base) * 4, math.cos(cam_osc_base) * 3]

    entities_array = [mushroom_array, mushroom_array_2, meteor_array]

    # Add the new cursor snapping code HERE, just after entities_array definition:
    raw_mouse_pos = pygame.mouse.get_pos()
    mouse_pos = list(raw_mouse_pos)

    # Find closest enemy within snap radius
    closest_enemy = None
    closest_dist = SNAP_RADIUS

    # snap function freezed
    """for entity_list in entities_array:
        for entity in entity_list:
            screen_pos = [entity.pos[x] + offset[x], entity.pos[y] + offset[y]]
            dist = get_distance(raw_mouse_pos, screen_pos)
            
            if dist < closest_dist:
                closest_dist = dist
                closest_enemy = screen_pos

    # Smoothly snap cursor to enemy if one is found
    if closest_enemy is not None:
        mouse_pos[0] += (closest_enemy[0] - mouse_pos[0]) * SNAP_SPEED
        mouse_pos[1] += (closest_enemy[1] + 100 - mouse_pos[1]) * SNAP_SPEED"""
    

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_progress()
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_r and weapon.unit < weapon.capacity:
                weapon.unit = 0
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                player.switch_weapon(-1)
                weapon = player.weapon
            elif event.button == 5:
                player.switch_weapon(1)
                weapon = player.weapon

    # Input handling
    if pygame.key.get_pressed()[pygame.K_d] and not moving_L:
        moving_R = True
    else:
        moving_R = False

    if pygame.key.get_pressed()[pygame.K_a] and not moving_R:
        moving_L = True
    else:
        moving_L = False

    if pygame.mouse.get_pressed()[0]:
        weapon.attack()

    # Camera and player position updates
    offset_target = [-player.steps + width / 2 - mouse_pos[0] * 0.8 + width * 0.4 + cam_osc[x],
                    -player.attitude + height * 0.8 - mouse_pos[1] * 0.8 + height * 0.4 + cam_osc[y]]
    offset[x] += ((offset_target[x] - offset[x]) / 10) * dt
    offset[y] += ((offset_target[y] - offset[y]) / 20) * dt
    player.pos[x] = player_pos[x]

    # Update positions
    player_pos_raw = [player.steps, player.attitude]
    player_pos = [player.steps + offset[x], player.attitude + offset[y]]
    
    # Calculate angles and rotations
    cursor_player_displacement = [mouse_pos[0] - player_pos[x], mouse_pos[1] - player_pos[y]]
    cursor_angle = math.atan2(cursor_player_displacement[0], cursor_player_displacement[1])
    cursor_rotation = (180 / math.pi) * cursor_angle - 90

    weapon_pos = [weapon.image.get_width() * -0.1 * math.sin(cursor_angle) + player_pos_raw[x],
                 weapon.image.get_height() * -0.2 * math.cos(cursor_angle) + player_pos_raw[y] + hip]
    weapon_player_displacement = [mouse_pos[x] - weapon_pos[x] - offset[x], 
                                mouse_pos[y] - weapon_pos[y] - offset[y]]
    weapon_angle = math.atan2(weapon_player_displacement[x], weapon_player_displacement[y])
    weapon_rotation = (180 / math.pi) * weapon_angle - 90

    # Render game world
    environment.render()
    for building in buildings_array:
        building.update()
        building.render()
    environment.tile_render()

    # Update and render entities
    for entities in entities_array:
        for entity in entities:
            entity.update()
            entity.render()
            # Check collisions with projectiles
            for projectile in render_array:
                if collide(projectile, entity):
                    effects_array.append(Damage_text(projectile.damage, projectile.pos, 
                                                   critical=projectile.critical))
                    entity.get_hit(projectile)
                    projectile.end(effect=Particles(projectile.pos, 3, size=10, 
                                                  color=entity.blood,
                                                  speed=0.5, size_change=5, gravity=True))


    # RENDER SECTION 
    
    # Update and render player and weapon
    player.update()
    player.render()
    weapon.update()
    weapon.render()

    # Render effects and UI
    draw_circle(mouse_pos)
    for obj in render_array:
        obj.update()
        obj.render()
    for effect in effects_array:
        effect.render()

    # Render HUD and UI elements
    weapon.render_hud()
    game.render_ui()
    environment.render_effects()

    # Update display
    pygame.display.update()
    clock.tick(-1)
    

if __name__ == "__main__":
    pygame.init()