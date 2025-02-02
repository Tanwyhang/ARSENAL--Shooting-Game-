import pygame
import random
import json
import math
import sys
import os

# change directory to this script to prevent dislocation
os.chdir(os.path.dirname(os.path.abspath(__file__)))


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
pygame.mixer.set_num_channels(150)
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
zeus_image = load_game_image('weapon-zeus.png')

stargazer_bullet_image = load_game_image('bullet-stargazer.png', [width / 30, width / 30])
shotgun_bullet_image = load_game_image('bullet-shotgun.png', [width / 30, width / 30])
player_image = load_game_image('player.png', [width / 10, width / 10])

main_menu_button_images = []
main_menu_button_images_count = 11
for i in range(main_menu_button_images_count):
    main_menu_button_images.append(load_game_image(f'button-{i+1 :02}.png'))

# width/height = k
# width * 0.5 / height * 0.5 = k
# 
game_logo_image = load_game_image('logo.png')

# hip calculation for weapon placement
hip = player_image.get_height() * 0.65

# env images
basic_tile_image = load_game_image('tile-basic.png', [width / 10, width / 10], False)
basic_tile_image_night = load_game_image('tile-basic-night.png', [width / 10, width / 10], False)
grass_tile_image = load_game_image('tile-grass.png', [width / 10, width / 10])
grass_tile_image_night = load_game_image('tile-grass-night.png', [width / 10, width / 10])

mountain_image_night = load_game_image('mountains-night.png', monitor_size)
mountain_image = load_game_image('mountains.png', monitor_size)

# entity images
mushroom_image_idle = load_game_image('mushroom-idle.png', [width / 14, width / 14])

# Load sounds
shoot_sound = pygame.mixer.Sound('assets\\sound-shoot.wav')
shoot_sound_2 = pygame.mixer.Sound('assets\\sound-shoot-2.wav')

explode_sound = pygame.mixer.Sound('assets\\sound-explode.wav')
weapon_select_sound = pygame.mixer.Sound('assets\\sound-select.wav')
hit_sound = pygame.mixer.Sound('assets\\sound-hit.wav')
die_sound = pygame.mixer.Sound('assets\\sound-die.wav')

mushroom_die_sound = ...
meteor_die_sound = ...

game_start_sound = pygame.mixer.Sound('assets\\sound-start.wav')
start_select_sound = pygame.mixer.Sound('assets\\start-select.wav')
select_sound = ...
click_sound = ...

teleport_sound = pygame.mixer.Sound('assets\\sound-teleport.wav')
jump_sound = ...

enter_day_sound = ...
enter_night_sound = ... 




# mixing section
teleport_sound.set_volume(0.18)
shoot_sound.set_volume(0.8)
shoot_sound_2.set_volume(0.8)


# soundtrack
music_shroom = os.path.join('assets', 'shroom.mp3')
music_day = ...
music_night  = ...

# Create fade effects (caching)
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

def play_music(path, loop):
    # bug fixing here
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1, 0, fade_ms=1500)

def play_music_long_fade(path, loops=-1):
    pygame.mixer.music.unload()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops, fade_ms=10000)


def delta_to_modifier(delta):
    return delta / 1000 * 60

def get_centered(image):
    return [image.get_width() / 2, image.get_height() / 2]

def draw_text(string, x, y, color=WHITE):
    text = font.render(string, True, color)
    textRect = text.get_rect()
    textRect.topleft = [x, y]
    screen.blit(text, textRect)

def draw_text_centered(string, x, y, color=WHITE):
    text = font.render(string, True, color)
    textRect = text.get_rect()
    textRect.center = [x, y]
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

def draw_progress_bar(pos, current, maximum, size=1, color=colors['blue'][19], border=1, line=False):
    if current >= maximum:
        current = maximum
        
    # Calculate base dimensions
    bar_width = width / 20 * size
    bar_height = height / 50 * size
    border_width = 3
    
    # Draw the outer rectangle (border)
    r_fixed = pygame.Rect(pos[x], pos[y], bar_width, bar_height)
    
    # Draw the inner progress bar
    progress = current / maximum
    if current != 1:
        r = pygame.Rect(
            pos[x], 
            pos[y], 
            min(bar_width * progress, bar_width - border_width),
            bar_height - border_width
        )
    else:
        r = pygame.Rect(
            pos[x] + 2.5 * border, 
            pos[y], 
            min(bar_width * progress, bar_width - border_width),
            bar_height - border_width
        )
        
    pygame.draw.rect(screen, color, r)
    pygame.draw.rect(screen, BLACK, r_fixed, 3)
    
    # Draw dividing lines if requested
    if line:
        segment_width = size * (bar_width / maximum)
        for i in range(maximum - 1):
            pygame.draw.line(screen, BLACK,
                           [pos[x] + segment_width * (1 + i), pos[y]],
                           [pos[x] + segment_width * (1 + i), pos[y] + bar_height - 2.5 * border],
                           1 + int(7 / maximum))


class SplashScreen:
   def __init__(self):
       self.image = game_logo_image
       self.image = pygame.transform.scale(self.image, [width * 0.6, (width * 0.6) / self.image.get_width() * self.image.get_height()])
       self.alpha = 0
       self.phase = "fade_in"
       self.timer = 0
       self.fade_speed = 2
       self.pause_duration = 200  # 1 second at 60fps

   def render(self):
       if self.phase == "fade_in":
           self.alpha = min(255, self.alpha + self.fade_speed)
           if self.alpha >= 255:
               self.phase = "pause"
               
       elif self.phase == "pause":
           self.timer += 1
           if self.timer >= self.pause_duration:
               self.phase = "fade_out"
               
       elif self.phase == "fade_out":
           self.alpha = max(0, self.alpha - self.fade_speed)
           if self.alpha <= 0:
               return True

       self.image.set_alpha(self.alpha)
       screen.blit(self.image, (width/2 - self.image.get_width()/2, height/2 - self.image.get_height()/2))
       return False


class LoreSequence:
    def __init__(self):
        self.lore_text = [
    "In an age long forgotten, the world was bathed in eternal daylight, sustained",
    "by ancient celestial crystals that hung in the sky like countless suns. These",
    "radiant crystals were the lifeblood of the realm, their glow illuminating every",
    "corner of the world, banishing shadows, and filling the air with an everlasting",
    "warmth.",
    "",
    "The people of this land lived in harmony, thriving under the benevolent light",
    "of the crystals. Their civilization blossomed, powered by the mystical energies",
    "of these celestial relics. Weapons, tools, and technology—all advanced to",
    "unparalleled heights, allowing them to forge an era of prosperity and peace.",
    "The crystals became symbols of balance, unity, and hope, their presence woven",
    "into the very fabric of life.",
    "",
    "But as with all things of great power, the allure of dominance and control",
    "grew too strong to resist. Greed seeped into the hearts of some, and they",
    "sought to exploit the boundless energy of the crystals for their own gain.",
    "In their relentless ambition, they delved deep into forbidden knowledge,",
    "attempting to harness the very essence of the crystals.",
    "",
    "This hubris came at a terrible cost. Their reckless actions disrupted the",
    "delicate balance that had sustained the world for centuries. The once-stable",
    "crystals fractured, their luminous brilliance dimmed, and chaos erupted across",
    "the realm. One by one, the celestial crystals began to fall from the heavens,",
    "their descent igniting the skies in fiery streaks of destruction.",
    "",
    "Now, these fallen crystals rain from the heavens as burning meteors, bringing",
    "devastation in their wake. Each meteor carries immense power, its energy potent",
    "enough to reshape the land upon impact. Mountains crumble, forests ignite, and",
    "rivers boil as the world faces an unrelenting barrage of celestial fury.",
    "",
    "Yet, amidst the ashes of ruin, humanity endures. The survivors, hardened by",
    "the trials of this new era, have learned to harness the power of the fallen",
    "crystals. From their remains, they forge weapons of extraordinary strength—tools",
    "capable of wielding the same energy that once sustained their world. These",
    "weapons, known as Starforged Arms, have become the last hope for survival in",
    "an ever-darkening reality.",
    "",
    "You are one of these survivors—a Starforged warrior. Your weapon, born from",
    "the remnants of celestial destruction, is both a tool of survival and a symbol",
    "of defiance against the calamity that threatens to consume everything. You walk",
    "a perilous path, wielding the power of the stars themselves, yet aware of the",
    "burden it carries.",
    "",
    "But with each passing night, the meteor showers grow more intense, their",
    "brilliance masking a growing dread. Whispers ripple through the remnants of",
    "civilization, speaking of something darker stirring in the endless void above.",
    "An ancient force, perhaps older than the crystals themselves, watches from the",
    "abyss, its presence palpable yet shrouded in mystery.",
    "",
    "Will you rise to confront this darkness, wielding the power of the stars to",
    "become the salvation of your world? Or will you, too, fall like the countless",
    "stars that once illuminated the skies, consumed by the very forces you seek to",
    "conquer?",
    "",
    "The choice is yours, Starforged warrior. The fate of the world hangs in the",
    "balance."
]

        
        self.scroll_speed = 10
        self.text_spacing = 60
        self.fade_duration = 50
        self.start_y = height * 0.7
        self.current_time = 0
        self.phase = "start"

    def render(self, screen):
        # Background effects
        if self.phase == "start":
            # Initialize fireflies in background
            self.phase = "scrolling"

        # Scroll text
        current_y = self.start_y - (self.current_time * self.scroll_speed)
        
        for i, line in enumerate(self.lore_text):
            # Calculate position and alpha
            y_pos = current_y + (i * self.text_spacing)
            
            # Only render visible text
            if height * 0.3 <= y_pos <= height:

                # Calculate fade at top and bottom edges
                distance_from_edge = min(abs(height * 0.3 - y_pos), height * 0.7 - y_pos)
                fade_zone = 150
                alpha = min(255, (distance_from_edge / fade_zone) * 255)
                
                font = pygame.font.Font(font_name, int(width/60))
                text_surface = font.render(line, True, (255, 255, 255))
                text_surface.set_alpha(int(alpha))
                
                # Center text horizontally
                text_x = (width - text_surface.get_width()) // 2
                screen.blit(text_surface, (text_x, y_pos))

        self.current_time += 1

        # Check if sequence is complete
        if current_y + (len(self.lore_text) * self.text_spacing) < height * 0.3:
            return True
        return False


class MainMenu:
    def hex_to_rgb(self, hex_color):
        if isinstance(hex_color, list) and len(hex_color) == 3:
            return hex_color
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    def __init__(self):        

        self.background = pygame.transform.scale(mountain_image.copy(), (width * 1.2, height * (width * 1.2 / width)))
        self.logo = game_logo_image

        self.button_image_index = 0
        self.button_images = main_menu_button_images.copy()
        self.button_images = [pygame.transform.scale(img, [width/5, (width / (width/5)) * img.get_height()]) for img in self.button_images]
        self.button_image = self.button_images[self.button_image_index]
        
        self.logo = pygame.transform.scale(self.logo, [width * 0.6, (width * 0.6) / self.logo.get_width() * self.logo.get_height()])
        

        self.bg_pos_ori = [width/2 - self.background.get_width()/2, height*0.65 - self.background.get_height()/2]
        self.logo_pos_ori = [width/2 - self.logo.get_width()/2, height/4]
        self.button_pos_ori = [width/2 - self.button_image.get_width()/2, height*0.6]
       
        self.bg_pos = [width/2 - self.background.get_width()/2, height/2 - self.background.get_height()/2]
        self.logo_pos = [width/2 - self.logo.get_width()/2, height/4]
        self.button_pos = [width/2 - self.button_image.get_width()/2, height*0.6]
       
        self.button_alpha = 100
        self.target_alpha = 100
        self.hover_alpha = 255

       # Initialize fade effects
        self.fade_surfaces = []
        fade_surface = pygame.Surface((width, height))
        fade_surface.fill(BLACK)

        for alpha in range(256):
            fade_surf = fade_surface.copy()
            fade_surf.set_alpha(alpha)
            self.fade_surfaces.append(fade_surf)
           
        self.fade_alpha = 255
        self.fading_in = True
        self.fading_out = False
        self.fade_in_speed = 3
        self.fade_out_speed = 30
        self.end_check = False

        self.bg_offset = [0, 0]
        self.logo_offset = [0, 0]
        self.button_offset = [0, 0]

        self.particles = []
        self.pulse_frequency = 0.1

        self.cam_osc_base = 0
        
        self.trigger = True
        

        # Initialize particles
        for i in range(100):  # Number of particles
            size_mod = 7
            particle_size = random.randint(int(width / 1500 * size_mod), int(width / 1500 * 1.5 * size_mod))
            
            self.particles.append([
                [random.randint(0, width), random.randint(0, height)],  # Position
                [0, 0],  # Velocity
                particle_size,  # Size
                self.hex_to_rgb(colors['brown'][21]),  # Color (blue)
                random.uniform(0, math.pi * 2),  # Phase
                random.uniform(0, 8 * math.pi),  # Progress
                random.uniform(0.001, 0.003),    # Speed
                random.uniform(0.8, 1.2),         # Spread
            ])
    

    def render_fireflies(self):
        position = 0
        velocity = 1
        size = 2
        color = 3
        phase = 4
        progress = 5
        speed = 6
        spread = 7

        for i in self.particles[:]:
            i[progress] += i[speed]
            t = i[progress]
            
            base_x = width/2 + (width/3) * math.sin(t/3)
            base_y = floor/2 + (height/6) * math.cos(t*2)
            
            spiral_x = math.cos(t) * t * 5
            spiral_y = math.sin(t) * t * 3
            
            i[position][0] = base_x + spiral_x + math.sin(t) * i[spread] * 50 * 60 #scale x
            i[position][1] = base_y + spiral_y + math.cos(t) * i[spread] * 30 * 10 # scale y

            if t > 8 * math.pi:
                i[progress] = 0

            wander_x = math.sin(i[phase]) * (height / 600)
            wander_y = math.cos(i[phase] * 0.5) * (height / 600)
            
            i[phase] += self.pulse_frequency
            pulse = (math.sin(i[phase]) + 1) * 0.5

            screen_x = i[position][x] + wander_x - i[size] * 1.5 + self.logo_offset[0] - width * 1.7
            screen_y = i[position][y] + wander_y - i[size] * 1.5 + self.logo_offset[1] + height * 0.1

            if 0 < screen_x < width and 0 < screen_y < height:
                small_size = 18
                small_surface = pygame.Surface((small_size, small_size), pygame.SRCALPHA)
                small_center = small_size / 2
                small_outer = max(1, int(i[size] * (0.7 + pulse * 0.3) / 2))
                small_core = max(1, int(i[size] * (0.2 + pulse * 0.3) / 2))
                
                main_color = []
                for c in i[color][:3]:
                    whitened = int(c + (255 - c) * (0.45 + pulse * 0.3))
                    main_color.append(whitened)
                
                outer_alpha = int(5 + pulse * 10)
                pygame.draw.circle(small_surface, (*i[color][:3], outer_alpha),
                                (small_center, small_center),
                                small_outer)
                
                core_alpha = int(200 + pulse * 55)
                pygame.draw.circle(small_surface, WHITE,
                                (small_center, small_center),
                                small_core)
                
                final_size = int(i[size] * 3)
                glow_surface = pygame.transform.scale(small_surface, (final_size, final_size))
                screen.blit(glow_surface, (screen_x, screen_y), special_flags=pygame.BLEND_RGB_ADD)


    def render(self):
        cam_osc = [math.sin(self.cam_osc_base * 0.05) * 50, math.cos(self.cam_osc_base * 0.05) * 50]
        self.cam_osc_base += 1
        
        screen.fill(colors['green'][5])
        screen.blit(self.background, self.bg_pos)
        screen.blit(self.logo, self.logo_pos)
       
        mouse_pos = pygame.mouse.get_pos()        
        self.offset = (mouse_pos[0] - width/2 + cam_osc[0], mouse_pos[1] - height /2 + cam_osc[1])

        # Calculate parallax offsets with different depths
        bg_offset_target = [self.offset[0] * -0.05, self.offset[1] * -0.05]  # Background moves slowest
        logo_offset_target = [self.offset[0] * -0.1, self.offset[1] * -0.1]  # Logo moves medium
        button_offset_target = [self.offset[0] * -0.15, self.offset[1] * -0.15]  # Button moves medium

        self.bg_offset[0] += (bg_offset_target[0] - self.bg_offset[0]) / 10
        self.bg_offset[1] += (bg_offset_target[1] - self.bg_offset[1]) / 10

        self.logo_offset[0] += (logo_offset_target[0] - self.logo_offset[0]) / 10
        self.logo_offset[1] += (logo_offset_target[1] - self.logo_offset[1]) / 10

        self.button_offset[0] += (button_offset_target[0] - self.button_offset[0]) / 10
        self.button_offset[1] += (button_offset_target[1] - self.button_offset[1]) / 10

        self.bg_pos[0] = self.bg_pos_ori[0] + self.bg_offset[0]
        self.bg_pos[1] = self.bg_pos_ori[1] + self.bg_offset[1]

        self.logo_pos[0] = self.logo_pos_ori[0] + self.logo_offset[0]
        self.logo_pos[1] = self.logo_pos_ori[1] + self.logo_offset[1]

        self.button_pos[0] = self.button_pos_ori[0] + self.button_offset[0]
        self.button_pos[1] = self.button_pos_ori[1] + self.button_offset[1]


        button_rect = pygame.Rect(self.button_pos[0], self.button_pos[1], 
                                self.button_image.get_width(), self.button_image.get_height())
       
        if button_rect.collidepoint(mouse_pos):
            if self.trigger:
                start_select_sound.play()
                self.trigger = not self.trigger
            self.target_alpha = self.hover_alpha
            self.button_image_index = min(main_menu_button_images_count-1, self.button_image_index + 2)
            self.button_image = self.button_images[self.button_image_index]


        else:

            self.trigger = True
            self.target_alpha = 100
            self.button_image_index = max(0, self.button_image_index - 1)
            self.button_image = self.button_images[self.button_image_index]
           
        self.button_alpha += (self.target_alpha - self.button_alpha) / 10
        
        button_surface = self.button_image.copy()
        button_surface.set_alpha(int(self.button_alpha))
        
        
        # render all layers here
        screen.blit(self.background, self.bg_pos)

        screen.blit(self.fade_surfaces[100], (0, 0))
        self.render_fireflies()

        screen.blit(self.logo, self.logo_pos)
        screen.blit(button_surface, self.button_pos)

        
        

        draw_circle(mouse_pos)

        # Handle fade effects
        if self.fading_in:
            self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
            if self.fade_alpha == 0:
                self.fading_in = False
               
        if self.fading_out:
            self.fade_alpha = min(255, self.fade_alpha + self.fade_out_speed)
            if self.fade_alpha == 255:
                self.fading_out = False
                self.end_check = True
               
        if self.fade_alpha > 0:
            screen.blit(self.fade_surfaces[int(self.fade_alpha)], (0, 0))
       
        return button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

    def fade_in(self):
        self.fade_alpha = 255
        self.fading_in = True
        self.fading_out = False

    def fade_out(self):
        self.fade_alpha = 0
        self.fading_out = True
        self.fading_in = False


class Game:
    def __init__(self):
        with open('assets\\game.json', 'r') as f:
            self.gamedata = json.load(f)
        self.stardust = self.gamedata["stardust"]
        self.stardust_d = 0


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
        self.stardust_d += (self.stardust - self.stardust_d) / 10 * dt
        draw_text(f'Stardust {round(self.stardust_d)}', width * 0.01, height / 4, 
                color=WHITE)

    def save_progress(self):
        self.stardust_d = 0
        self.gamedata['stardust'] = self.stardust
        self.gamedata['weapons'] = [weapon.id for weapon in player.weapons]
        with open('assets\\game.json', 'w') as f:
            json.dump(self.gamedata, f)

class Environment:
    def __init__(self):
        self.border_image = 0
        self.sky_color = colors['green'][5]
        self.night_sky_color = "#1f1013"
        self.background_color = BLACK
        self.soil = basic_tile_image
        self.soil_night = basic_tile_image_night
        self.grass = grass_tile_image
        self.grass_night = grass_tile_image_night
        self.maintiles = [self.grass, self.soil]
        self.tile_width = self.soil.get_width()
        self.floor_modded = floor - player.height / 8
        self.tile_count = 150
        self.mountains = mountain_image
        self.mountain_pos_x = 0
        self.offset_for_teleport = 0
        self.mount_offset = offset[x]

        self.left_boundary = 0 - 30 * self.tile_width
        self.right_boundary = 30 * self.tile_width 
        
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
        self.daynight_value = 0
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
        self.daynight = math.sin(self.daynight_value * 1 ** (-1))
        
        # DAY
        if self.daynight >= 0:

            
            # set false for next cutscene
            if self.night_cutscene_activated:
                self.night_cutscene_activated = False
            
            # one time activator
            if not self.day_cutscene_activated:
                meteor_array.clear()
                self.background_color = self.sky_color
                self.mountains = mountain_image
                self.play_day_cutscene()

                if fireflies_night in effects_array:
                    effects_array.remove(fireflies_night)
                effects_array.append(fireflies_day)
                
            
            if len(mushroom_array) < self.mushroom_counts:
                self.mushroom_ticker += 1 * dt

            if self.mushroom_ticker > self.mushroom_spawn_cd:
                self.spawn_mushrooms()
                self.mushroom_ticker = 0

            if not self.daynight_tswitch:
                self.fade_in()
                self.maintiles = [self.grass, self.soil]
                self.daynight_tswitch = True
        
        # NIGHT
        else:

            # set false for next cutscene
            if self.day_cutscene_activated:
                self.day_cutscene_activated = False

            # one time activator
            if not self.night_cutscene_activated:
                self.background_color = self.night_sky_color
                self.mountains = mountain_image_night
                self.play_night_cutscene()

                if fireflies_day in effects_array:
                    effects_array.remove(fireflies_day)

                effects_array.append(fireflies_night)
            
            

            # Regular meteor spawning
            # NEED PERFORMANCE IMPROVEMENT, NOT RENDER PROBLEM BUT DATA LOAD CALCULATED OUTSIDE OF VISIBLE RANGE IS DRAGGING PERFORMANCE
            self.meteor_timer += dt * environment.game_time
            if self.meteor_timer >= self.meteor_spawn_rate:
                self.meteor_timer = 0
                meteor_array.append(Meteor())
            

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

        mount_offset_x_target = -player.steps + width / 2 - mouse_pos[0] * 0.8 + width * 0.4 + cam_osc[x] + self.offset_for_teleport
        self.mount_offset += (mount_offset_x_target - self.mount_offset) * 0.1 * dt

        # Draw mountains
        
        for i in range(-15, 15):  # Render mountains from -15 to 15
            # Calculate the x-position for the current mountain
            x_position = width * i - width + self.mount_offset * 0.1

            # Only render mountains near the displayable screen
            if -width <= x_position <= width * 2:
                screen.blit(
                    self.mountains,
                    [x_position, offset[y] / 3]
                )

        
        # Draw boundary indicators
        left_boundary_x = environment.left_boundary # Left boundary
        right_boundary_x = environment.right_boundary # Right boundary
        

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
            screen.blit(fades[min(254, int(self.fade))], [0, 0])

        if self.flashing_in or self.flashing_out:
            if self.flashing_in and self.flash > 0:
                self.flash -= 1 * dt
            else:
                self.flashing_in = False
            if self.flashing_out and self.flash < 255:
                self.flash += 1 * dt
            else:
                self.flashing_out = False
            screen.blit(flashes[min(254, int(self.flash))], [0, 0])

    def slow_motion(self, time=15):
        if self.slow_time < 1:
            self.slow_time += time

    def shake(self, time=20):
        self.shake_time += time

class KillStreak:
    def __init__(self):
        self.kill_timer = 0
        self.kill_count = 0
        self.kill_window = 150
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

        

        self.last_safe_y = self.pos[y]  # For void fall recovery
    

    def take_damage(self, damage):
        if not self.is_hit:
            self.current_health -= damage
            self.is_hit = True
            self.hit_timer = 0
            if self.current_health <= 0:
                self.current_health = 0
        # death handling
    
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
        
        offset_delta = 0
        # Handle map wrapping
        if self.steps < environment.left_boundary:
            # If player goes too far left, wrap to right
            self.steps += environment.right_boundary - environment.left_boundary
            environment.offset_for_teleport += environment.right_boundary - environment.left_boundary

            offset_target[x] = -player.steps + width / 2 - mouse_pos[0] * 0.8 + width * 0.4 + cam_osc[x]
            offset_delta = offset_target[x] - offset[x]
            offset[x] = offset_target[x] + self.velo_x * 10
                

        elif self.steps > environment.right_boundary:
            # If player goes too far right, wrap to left
            self.steps -= environment.right_boundary - environment.left_boundary
            environment.offset_for_teleport -= environment.right_boundary - environment.left_boundary

            offset_target[x] = -player.steps + width / 2 - mouse_pos[0] * 0.8 + width * 0.4 + cam_osc[x]
            offset[x] = offset_target[x] + self.velo_x * 10        



        # Handle void falling
        if self.pos[y] > height * 1.5:  # If fallen too far
            self.pos[y] = floor - self.height # Reset to floor level
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
        if self.jump_count < 4:
            
            effects_array.append(GlowingParticles([player_pos_raw[x], player_pos_raw[y] + player.height], 5, size=6))

            if self.jump_count > 0:

                if not (moving_R or moving_L):
                    self.velo_x = [300, -300][(self.jump_count + 1) % 2] / dt if self.flipped else [300, -300][(self.jump_count) % 2] / dt
                else:
                    self.velo_x = 300 / dt if moving_R else 300 / dt * -1
                self.velo_y = 0
                teleport_sound.play()
                effects_array.append(Explosion([player_pos_raw[x], player_pos_raw[y]], count=15, size=0.9, color_base=colors['blue'][21], phase=20))
                environment.slow_motion(time=6)
            else:
                self.gravity = -30

            self.jump_count += 1


    def switch_weapon(self, con):
        if self.weapons:
            if con == 1 and self.current_weapon < len(self.weapons) - 1:
                effects_array.append(Particles(weapon_pos, 15, size=6, speed=0.8, color=[255, 0, 255], size_change=3))
                self.current_weapon += con
                environment.slow_motion()
                weapon_select_sound.play()

            elif con == -1 and self.current_weapon > 0:
                effects_array.append(Particles(weapon_pos, 15, size=6, speed=0.8, color=[255, 255, 0], size_change=3))
                self.current_weapon += con
                environment.slow_motion()
                self.weapon = self.weapons[self.current_weapon]
                weapon_select_sound.play()

    def render(self):
        # Health bar
        health_width = ((self.width * self.current_health) / self.max_health)
        health_pos = [player_pos[x] - self.centered[x], player_pos[y] - 20]
        pygame.draw.rect(screen, colors['red'][20],
                        (health_pos[0], health_pos[1] - 10, self.width, 10), border_radius=10)
        pygame.draw.rect(screen, colors['green'][7],
                        (health_pos[0], health_pos[1] - 10, health_width, 10), border_radius=10)
        
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
        self.stardust = 150
        
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
            self.velocity[0] = dx * 0.05 * environment.current_day
            self.velocity[1] = dy * 0.05 * environment.current_day - 10 # Initial upward velocity for arc
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
            speed = 2 * environment.current_day
            self.velocity = [
                dx / distance * speed,
                dy / distance * speed
            ]

    # for bullets
    def get_hit(self, obj):
        self.tpos[x] = self.pos[x] + (math.sin(weapon_angle)) * obj.damage * 10
        self.tpos[y] = self.pos[y] + (math.cos(weapon_angle)) * obj.damage * 10
        self.hp -= obj.damage
        hit_sound.play()
        self.hitted = True
    
    def take_damage(self, dmg, strength):
        self.tpos[x] = self.pos[x] + (math.sin(cursor_angle)) * 10 * strength
        self.tpos[y] = self.pos[y] + (math.cos(cursor_angle)) * 10 * strength
        self.hp -= dmg
        hit_sound.play()
        self.hitted = True

    def create_explosion(self):

        # Remove from render array if present
        if self in render_array:
            render_array.remove(self)
        if self in meteor_array:
            meteor_array.remove(self)

        effects_array.append(Explosion(self.pos, color_base=[255, 100, 0], count=25))


        
        screen_shake(30)
        explode_sound.play()
    
    def end(self):
        # Same as mushroom's end method
        for i in entities_array:
            if self in i:
                i.remove(self)
        
        self.create_explosion()
        die_sound.play()

        game.stardust += self.stardust
        # game.exp += self.exp
        # game.gold += (self.exp * random.randint(5, 15) / 10)
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
                size=16,
                color="#e02a31",
                speed=0.2,
                size_change=3,
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

        """
        # Draw health bar
        p = [self.pos[x] - self.width/2 + offset[x],
             self.pos[y] - self.height + offset[y]]
        draw_bar([p[x] + self.width/2, p[y] - 30], self.hp, self.max_hp)
        """

        # Get screen position
        screen_x = self.pos[0] + offset[0]
        screen_y = self.pos[1] + offset[1]

        # Check if meteor is on screen (including some margin for rotation)
        margin = max(self.image.get_width(), self.image.get_height())
        if -margin < screen_x < width + margin and -margin * 1.3 < screen_y < height + margin:
            # Draw meteor
            rotated = pygame.transform.rotate(self.image, -math.degrees(self.angle) - 90)
            screen.blit(
                rotated,
                [screen_x - rotated.get_width()/2,
                    screen_y - rotated.get_height()/2]
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
        self.stardust = 10
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
    
    def take_damage(self, dmg, strength):
        self.tpos[x] = self.pos[x] + (math.sin(cursor_angle)) * 10 * strength
        self.tpos[y] = self.pos[y] + (math.cos(cursor_angle)) * 10 * strength
        self.hp -= dmg
        hit_sound.play()
        self.hitted = True

    def end(self):
        
        game.stardust += self.stardust

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

        self.id = 1

        self.name = 'StarGazer'
        self.capacity = 50
        self.unit = self.capacity
        self.damage = 15
        self.cost = 10000




        self.check = 3
        self.reset_time = 3
        self.cd_time = 40
        self.cd = 0
        self.ready = False
        self.image_raw = stargazer_image.copy()
        self.image_ori = self.image_raw.copy()
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
    
    def copy(self):
        return Stargazer()

class Shotgun:
    def __init__(self):

        self.id = 2

        self.name = 'Hades'
        self.capacity = 3
        self.unit = self.capacity
        self.damage = 25
        self.cost = 10000


        self.check = 60
        self.ready = False
        self.cd_time = 80
        self.cd = 0
        self.reset_time = 10
        self.image_raw = shotgun_image.copy()
        self.image_ori = self.image_raw.copy()
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
            shoot_sound_2.play()
            self.check = 0
            self.ready = False
            self.unit -= 1
    
    def copy(self):
        return Shotgun()


class SpinningBlade:
    def __init__(self):
        self.id = 3
        self.name = 'Zeus'
        self.capacity = 1  # Number of spins before cooldown
        self.unit = self.capacity
        self.damage = 69
        self.cost = 15000

        # Spin attack properties
        self.spinning = False
        self.spin_angle = 0
        self.spin_speed = 1.2  # Complete 720 degrees in 30 frames
        self.spin_radius = 400  # Area of effect radius
        self.current_spin = 0
        
        self.check = 60
        self.ready = False
        self.cd_time = 10  # Longer cooldown than shotgun due to power
        self.cd = 0
        self.reset_time = 10
        self.image_raw = zeus_image.copy()  # Assuming you have a blade image
        self.image_ori = self.image_raw.copy()

        self.image_raw = pygame.transform.scale(self.image_raw, [width * 0.11, width * 0.11])
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
        
        if self.spinning:
            # Update spin animation
            self.spin_angle += (720 * self.spin_speed - self.spin_angle) / 10 * dt
            if self.spin_angle >= 720:
                self.spinning = False
                self.spin_angle = 0
                self.ready = False
                self.unit -= 1
            # During spin, override normal rotation with spin animation
            self.image = pygame.transform.rotate(self.image_raw, self.spin_angle + weapon_rotation)
        else:
            # Normal weapon following cursor
            self.image = pygame.transform.rotate(self.image_raw, weapon_rotation)
            
        self.centered = self.image.get_width() / 2, self.image.get_height() / 2
        
        # Handle weapon flip based on cursor angle
        if cursor_angle < 0:
            if not self.flipped:
                self.image_raw = pygame.transform.flip(self.image_raw, False, True)
                self.flipped = True
        elif self.flipped:
            self.image_raw = pygame.transform.flip(self.image_raw, False, True)
            self.flipped = False
            
        # Ready state and cooldown management
        if self.check > self.reset_time and not self.ready:
            self.ready = True
        if self.unit == 0:
            self.cd += 1 * dt
            if self.cd >= self.cd_time:
                self.cd = 0
                self.unit = self.capacity

    def render(self):
        # Draw the weapon
        screen.blit(self.image, [self.pos[x] - self.centered[x] + offset[x],
                    self.pos[y] - self.centered[y] + offset[y]])

    def render_hud(self):

        draw_progress_bar([20 * scale_width, 20 * scale_height], self.unit,
                self.capacity, size=2.5, color=colors['blue'][19], line=True)
        draw_bar([20 * scale_width, 70 * scale_height], self.cd,
                self.cd_time, size=2.5, color=colors['red'][19])
        screen.blit(self.image_base, [30 * scale_width, 70 * scale_height])
        draw_text(f'{self.unit} / {self.capacity}', 230 * scale_width, 30 * scale_height)

    def attack(self):
        if self.ready and self.unit > 0 and not self.spinning:
            self.spinning = True
            self.spin_angle = 0

            
            
            # Apply area damage to all enemies within spin radius
            for entities in entities_array:  # Assuming you have an enemies list
                for entity in entities:
                    # Calculate distance to entity
                    dx = entity.pos[x] - self.pos[x]
                    dy = entity.pos[y] - self.pos[y]
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    # If entity is within spin radius, apply damage
                    if distance <= self.spin_radius:
                        dmg = self.damage
                        # Critical hit chance
                        if random.randint(1, 7) == 5:
                            dmg **= 1.2
                            entity.take_damage(dmg, 50)
                        else:
                            entity.take_damage(dmg, 30)
                        effects_array.append(Damage_text(dmg, entity.pos, 
                                                   critical=True))
            
            screen_shake(30)
            # Assuming you have a swing sound
            shoot_sound.play()
    
    def copy(self):
        return SpinningBlade()


class WeaponShop:
    def __init__(self, pos):
        self.weapons_d = [Stargazer(), Shotgun(), SpinningBlade()]
        self.weapon_dict = {weapon.id: weapon for weapon in self.weapons_d}
        self.weapons_d = list(self.weapon_dict.values())
        self.weapons_centered = get_centered(self.weapons_d[0].image_raw)
        
        for weapon in self.weapons_d:
            weapon.image_raw = pygame.transform.scale(weapon.image_raw, [width/5] * 2)

        self.image_arr = [pygame.transform.scale(weaponshop_image, [weaponshop_image.get_width() * (height * 0.45)/weaponshop_image.get_height(), height * 0.45]), weaponshopselect_image]
        self.image = self.image_arr[0]
        self.centered = get_centered(self.image)
        self.pos = [pos[x] - self.centered[x], pos[y] - self.centered[y] * 2]
        
        # Shop state
        self.ready = False
        self.choice = None
        self.selected_owned = None
        
        # Layout calculations
        self.left_panel_width = width * 0.6
        self.grid_cols = 4
        self.cell_padding = 30
        self.cell_size = (self.left_panel_width - (self.grid_cols + 1) * self.cell_padding) / self.grid_cols

        self.right_panel_x = self.left_panel_width + 50
        
        self.buy_button = pygame.Rect(self.right_panel_x, height * 0.8, 200, 50)
        self.sell_button = pygame.Rect(self.right_panel_x, height * 0.8, 200, 50)

        # Scroll positions for both sections
        self.scroll_inventory = 0
        self.scroll_inventory_target = 0
        self.scroll_shop = 0
        
        
        # Calculate max scroll values
        self.shop_section_height = height * 0.55
        self.owned_section_height = height - self.shop_section_height
        
        # Max scroll calculations will be updated in run() based on content

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
        r = True
        
        # Layout calculations
        cell_padding = self.cell_padding
        grid_cols = self.grid_cols
        shop_section_height = self.shop_section_height
        cell_size = self.cell_size

        # Owned section
        owned_section_height = height - shop_section_height
        owned_cell_size = cell_size * 0.85
        owned_padding = cell_padding * 0.85
        
        # Calculate max scroll values
        max_scroll_shop = max(0, ((len(self.weapons_d) - 1) // grid_cols + 1) * (cell_size + cell_padding) - shop_section_height)
        max_scroll_inventory = (owned_cell_size + owned_padding) * ((len(player.weapons) - 1) // 4)


        while r:
            last_frame = pygame.time.get_ticks()
            dt = 1
            mouse_pos = pygame.mouse.get_pos()

            # update inventory scroll
            self.scroll_inventory += (self.scroll_inventory_target - self.scroll_inventory) / 20 * dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return None
                    
                if event.type == pygame.MOUSEWHEEL:
                    # Determine which section to scroll based on mouse position
                    if mouse_pos[1] < shop_section_height:
                        self.scroll_shop = max(0, min(self.scroll_shop - event.y * 20, max_scroll_shop))
                    else:
                        self.scroll_inventory_target = max(0, min(self.scroll_inventory_target - event.y * 20, max_scroll_inventory))
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Shop section clicks
                    for i in range(len(self.weapons_d)):
                        row = i // grid_cols
                        col = i % grid_cols
                        x = cell_padding + col * (cell_size + cell_padding)
                        y = cell_padding + row * (cell_size + cell_padding) - self.scroll_shop

                        cell_rect = pygame.Rect(x, y, cell_size, cell_size)
                        
                        if cell_rect.collidepoint(mouse_pos) and mouse_pos[1] < shop_section_height:
                            self.choice = i
                            self.selected_owned = None
                    
                    # Owned weapons clicks
                    for i in range(len(player.weapons)):
                        row = i // grid_cols
                        col = i % grid_cols
                        x = owned_padding + col * (owned_cell_size + owned_padding)
                        y = shop_section_height + owned_padding + row * (owned_cell_size + owned_padding) - self.scroll_inventory
                        cell_rect = pygame.Rect(x, y, owned_cell_size, owned_cell_size)
                        
                        if cell_rect.collidepoint(mouse_pos):
                            self.selected_owned = i
                            self.choice = None

                    # Handle buy/sell buttons

                    # BUY
                    if self.choice is not None and self.buy_button.collidepoint(mouse_pos):

                        if game.stardust >= self.weapons_d[self.choice].cost:
                            player.weapons.append(self.weapon_dict[self.choice + 1].copy())
                            player.current_weapon = len(player.weapons) - 1
                            max_scroll_inventory = (owned_cell_size + owned_padding) * ((len(player.weapons) - 1) // 4)

                            self.scroll_inventory_target = (owned_cell_size + owned_padding) * ((len(player.weapons) - 1) // 4)
                            game.stardust -= self.weapons_d[self.choice].cost
                            game.save_progress()

                    # SELL
                    elif self.selected_owned is not None and self.sell_button.collidepoint(mouse_pos):
                        
                        game.stardust += player.weapons[self.selected_owned].cost * 0.3
                        player.weapons.pop(self.selected_owned)
                        player.current_weapon = self.selected_owned-1
                        self.selected_owned = None
                        max_scroll_inventory = (owned_cell_size + owned_padding) * ((len(player.weapons) - 1) // 4)

                        self.scroll_inventory_target = (owned_cell_size + owned_padding) * ((len(player.weapons) - 1) // 4)
                        game.save_progress()

                    

            screen.fill(BLACK)

            # Draw owned weapons section
            for i in range(len(player.weapons)):
                row = i // grid_cols
                col = i % grid_cols
                x = owned_padding + col * (owned_cell_size + owned_padding)
                y = shop_section_height + owned_padding*2 + row * (owned_cell_size + owned_padding) - self.scroll_inventory
                cell_rect = pygame.Rect(x, y, owned_cell_size, owned_cell_size)
                
                pygame.draw.rect(screen, colors['blue'][20], cell_rect)
                
                if i == self.selected_owned:
                    pygame.draw.rect(screen, colors['blue'][10], cell_rect, 3)
                elif cell_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, colors['blue'][15], cell_rect, 3)
                
                weapon = player.weapons[i]
                weapon_scaled = pygame.transform.scale(weapon.image_ori,
                    (int(owned_cell_size * 0.8), int(owned_cell_size * 0.8)))
                screen.blit(weapon_scaled,
                    (x + owned_cell_size * 0.1, y + owned_cell_size * 0.1))
            
            # Draw owned section title
            draw_text("OWNED WEAPONS", owned_padding, 
                        shop_section_height + owned_padding/2, color=colors['blue'][1])
            
            # Draw shop section
            shop_surface = pygame.Surface((self.left_panel_width, shop_section_height))
            shop_surface.fill(BLACK)
            
            # Draw shop grid with scroll
            for i in range(len(self.weapons_d)):
                row = i // grid_cols
                col = i % grid_cols
                x = cell_padding + col * (cell_size + cell_padding)
                y = cell_padding + row * (cell_size + cell_padding) - self.scroll_shop
                
                if -cell_size < y < shop_section_height:
                    cell_rect = pygame.Rect(x, y, cell_size, cell_size)
                    pygame.draw.rect(shop_surface, colors['green'][20], cell_rect)
                    
                    if i == self.choice:
                        pygame.draw.rect(shop_surface, colors['green'][10], cell_rect, 3)
                    elif cell_rect.collidepoint((mouse_pos[0], mouse_pos[1])):
                        pygame.draw.rect(shop_surface, colors['green'][15], cell_rect, 3)
                    
                    weapon = self.weapons_d[i]
                    weapon_scaled = pygame.transform.scale(weapon.image_raw, 
                        (int(cell_size * 0.8), int(cell_size * 0.8)))
                    shop_surface.blit(weapon_scaled, 
                        (x + cell_size * 0.1, y + cell_size * 0.1))
            
            screen.blit(shop_surface, (0, 0))
            
            # Draw separators
            pygame.draw.line(screen, colors['green'][1], 
                            (0, shop_section_height), 
                            (self.left_panel_width, shop_section_height), 2)
            pygame.draw.line(screen, colors['green'][1],
                            (self.left_panel_width, 0),
                            (self.left_panel_width, height), 2)
            
            
            # Draw right panel info
            if self.choice is not None:
                selected_weapon = self.weapons_d[self.choice]
                preview_size = height * 0.3
                weapon_preview = pygame.transform.scale(selected_weapon.image_ori, 
                                                        (preview_size, preview_size))
                screen.blit(weapon_preview, (self.right_panel_x, height * 0.1))
                
                draw_text(f"Name: {selected_weapon.name}", self.right_panel_x, height * 0.5)
                draw_text(f"Damage: {selected_weapon.damage}", self.right_panel_x, height * 0.5 + 40)
                draw_text(f"Reload: {selected_weapon.reset_time}s", self.right_panel_x, height * 0.5 + 80)
                draw_text(f"Magazine: {selected_weapon.capacity}", self.right_panel_x, height * 0.5 + 120)
                
                
                # Buy button with hover effect
                self.buy_button = pygame.Rect(self.right_panel_x, height * 0.8, 200, 50)
                button_color = colors['green'][21] if self.buy_button.collidepoint(mouse_pos) else colors['green'][20]
                pygame.draw.rect(screen, button_color, self.buy_button)
                # Calculate the center of the button
                button_center_x = self.buy_button.x + self.buy_button.width // 2
                button_center_y = self.buy_button.y + self.buy_button.height // 2
                draw_text_centered('BUY', button_center_x, button_center_y)

                draw_text(f"Cost: {selected_weapon.cost} Stardust", self.right_panel_x, self.buy_button.y - self.buy_button.height // 2 - 30)
                
            elif self.selected_owned is not None:
                selected_weapon = player.weapons[self.selected_owned]
                preview_size = height * 0.3
                weapon_preview = pygame.transform.scale(selected_weapon.image_ori, 
                                                        (preview_size, preview_size))
                screen.blit(weapon_preview, (self.right_panel_x, height * 0.1))
                
                draw_text(f"Name: {selected_weapon.name}", self.right_panel_x, height * 0.5)
                draw_text(f"Damage: {selected_weapon.damage}", self.right_panel_x, height * 0.5 + 40)
                draw_text(f"Reload: {selected_weapon.reset_time}s", self.right_panel_x, height * 0.5 + 80)
                draw_text(f"Magazine: {selected_weapon.capacity}", self.right_panel_x, height * 0.5 + 120)

                
                # Sell button with hover effect
                self.sell_button = pygame.Rect(self.right_panel_x, height * 0.8, 200, 50)
                button_color = colors['red'][21] if self.sell_button.collidepoint(mouse_pos) else colors['red'][20]
                pygame.draw.rect(screen, button_color, self.sell_button)
                # Calculate the center of the button
                button_center_x = self.sell_button.x + self.sell_button.width // 2
                button_center_y = self.sell_button.y + self.sell_button.height // 2
                draw_text_centered('SELL', button_center_x, button_center_y)

                draw_text(f"Sell for {selected_weapon.cost * 0.3} Stardust", self.right_panel_x, self.buy_button.y - self.buy_button.height // 2 - 30)
            
            draw_text(f"Stardust: {int(game.stardust)}", self.right_panel_x, height * 0.1)
            
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
    def hex_to_rgb(self, hex_color):
        if isinstance(hex_color, list) and len(hex_color) == 3:
            return hex_color
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    def __init__(self, pos, color_base=[255, 255, 255], count=5, size=1, angle=1, phase=0):
        self.pos = pos
        self.size = size
        self.particles = []
        self.angle = angle
        
        # Convert color to RGB
        color_base_rgb = self.hex_to_rgb(color_base)
        
        for i in range(count):
            subbed = random.randint(0, 70)
            particle_size = random.randint(int(width * 0.008 * self.size),
                                       int(width * 0.03 * self.size * self.size))
            
            self.particles.append([
                [pos[x], pos[y]],  # Position
                [random.randint(int(-width / 200), int(width / 200)),  # Velocity X
                 random.randint(int(-height / 200), int(height / 200))],  # Velocity Y
                particle_size,  # Size
                [max(0, min(255, abs(color_base_rgb[0] - subbed))), 
                 max(0, min(255, abs(color_base_rgb[1] - subbed))), 
                 max(0, min(255, abs(color_base_rgb[2] - subbed))),
                 255]  # Color with alpha
            ])
        
        for i in self.particles[:]:
            # pre-Update position
            i[0][x] += i[1][x] * self.angle * dt * phase
            i[0][y] += i[1][y] * self.angle * dt * phase

    def render(self):
        position = 0
        velocity = 1
        size = 2
        color = 3

        if not self.particles:
            effects_array.remove(self)
            return True
        
        for i in self.particles[:]:
            # Update position
            i[position][x] += i[velocity][x] * self.angle * dt
            i[position][y] += i[velocity][y] * self.angle * dt
            i[size] -= height / 1000 * dt
            
            if i[size] <= 0.1:
                self.particles.remove(i)
            else:
                # Pixelation factor
                pixel_scale = 3
                
                # Create smaller surface first
                small_size = max(1, int(i[size] * 3 / pixel_scale))
                small_surface = pygame.Surface((small_size, small_size), pygame.SRCALPHA)
                
                # Calculate scaled positions and sizes
                small_center = small_size / 2
                small_outer = max(1, int(i[size] * 1.27 / pixel_scale))
                small_main = max(1, int(i[size] * 0.6 / pixel_scale))
                small_core = max(1, int(i[size] * 0.2 / pixel_scale))
                
                # Calculate colors
                main_color = []
                for c in i[color][:3]:
                    whitened = int(c + (255 - c) * 0.45)
                    main_color.append(whitened)
                
                # Draw on small surface
                pygame.draw.circle(small_surface, (*i[color][:3], 5),
                                (small_center, small_center),
                                small_outer)
                
                pygame.draw.circle(small_surface, (*main_color, 20),
                                (small_center, small_center),
                                small_main)
                
                pygame.draw.circle(small_surface, (*WHITE, 255),
                                (small_center, small_center),
                                small_core)
                
                # Scale up to final size
                final_size = int(i[size] * 3)
                glow_surface = pygame.transform.scale(small_surface, (final_size, final_size))
                
                # Blit with blend
                screen_x = i[position][x] + offset[x] - i[size] * 1.5
                screen_y = i[position][y] + offset[y] - i[size] * 1.5
                screen.blit(glow_surface, (screen_x, screen_y), special_flags=pygame.BLEND_RGB_ADD)
        
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

        WANDER_STRENGTH = height / 2000  # Strength of wandering motion
        WANDER_FREQUENCY = 0.1  # How often direction changes
        AIR_RESISTANCE = 0.99  # For smooth deceleration

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
                # Apply gravity acceleration to Y velocity
                i[velocity][y] += GRAVITY_ACCEL * dt
                
                # Apply air resistance
                i[velocity][y] *= AIR_RESISTANCE
                i[velocity][x] *= AIR_RESISTANCE
                
                # Limit to terminal velocity
                if i[velocity][y] > TERMINAL_VELOCITY:
                    i[velocity][y] = TERMINAL_VELOCITY
            
            # Add wandering motion using sine waves
            time_offset = pygame.time.get_ticks() * WANDER_FREQUENCY
            i[velocity][x] += math.sin(time_offset + i[position][y] * 0.1) * WANDER_STRENGTH * dt
            i[velocity][y] += math.cos(time_offset + i[position][x] * 0.1) * WANDER_STRENGTH * dt
            
            # Apply air resistance for smooth motion
            i[velocity][x] *= AIR_RESISTANCE
            i[velocity][y] *= AIR_RESISTANCE
            
            # Add slight random drift
            i[velocity][x] += (random.random() - 0.5) * WANDER_STRENGTH * dt
            i[velocity][y] += (random.random() - 0.5) * WANDER_STRENGTH * dt
            
            if not 0 < i[position][x] + offset[x] < width or not 0 < i[position][y] + offset[y] < height:
                effects_array.remove(self)
                return True
            elif i[size] <= 0.1:
                self.particles.remove(i)
            else:
                # Pixelation factor (higher = more pixelated)
                pixel_scale = 3  # You can adjust this value
                
                # Create smaller surface first
                small_size = max(1, int(i[size] * 3 / pixel_scale))
                small_surface = pygame.Surface((small_size, small_size), pygame.SRCALPHA)
                
                # Calculate scaled positions and sizes for the small surface
                small_center = small_size / 2
                small_outer = max(1, int(i[size] * 1.27 / pixel_scale))
                small_main = max(1, int(i[size] * 0.6 / pixel_scale))
                small_core = max(1, int(i[size] * 0.2 / pixel_scale))
                
                # Calculate colors
                main_color = []
                for c in i[color][:3]:
                    whitened = int(c + (255 - c) * 0.45)
                    main_color.append(whitened)
                
                # Draw on small surface
                pygame.draw.circle(small_surface, (*i[color][:3], 5),
                                (small_center, small_center),
                                small_outer)
                
                pygame.draw.circle(small_surface, (*main_color, 20),
                                (small_center, small_center),
                                small_main)
                
                pygame.draw.circle(small_surface, (*WHITE, 255),
                                (small_center, small_center),
                                small_core)
                
                # Scale up to final size
                final_size = int(i[size] * 3)
                glow_surface = pygame.transform.scale(small_surface, (final_size, final_size))
                
                # Blit the combined surface with blend
                screen_x = i[position][x] + offset[x] - i[size] * 1.5
                screen_y = i[position][y] + offset[y] - i[size] * 1.5
                screen.blit(glow_surface, (screen_x, screen_y), special_flags=pygame.BLEND_RGB_ADD)
        
        return False


class Fireflies:
    def hex_to_rgb(self, hex_color):
        if isinstance(hex_color, list) and len(hex_color) == 3:
            return hex_color
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    
    

    def __init__(self, pos, count, size=10, color='#FFE87C', spread=2300, speed=1):  # Added spread parameter
        self.pos = pos
        self.particles = []
        self.scale_x, self.scale_y = 36, 3.2
        self.speed = speed
        
        # Convert color to RGB
        color_rgb = self.hex_to_rgb(color)
        
        # Each firefly pulse rate
        self.pulse_frequency = random.uniform(0.01, 0.1)

        def get_cosmic_coords(spread, height_limit):
            # Increase scale factors for bigger patterns
            scale_x = self.scale_x  # Horizontal scale multiplier 
            scale_y = self.scale_y  # Vertical scale multiplier
            
            t = random.uniform(0, 4 * math.pi)
            phi = (1 + math.sqrt(5)) / 2
            
            x = (spread * scale_x) * math.cos(t/phi) * math.exp(-0.2*t)
            y = height_limit/2 + ((height_limit * scale_y) /4 * math.sin(t*2) * math.exp(-0.1*t))
            
            return [int(x), int(y)]
        
        # Add path progress for each particle
        for i in range(count):
            spawn_pos = get_cosmic_coords(width/2, floor - 100)  # Initial position
            particle_size = random.randint(int(width / 1500 * size), 
                                        int(width / 1500 * 1.5 * size))
            particle_spread = random.uniform(0.8, 1.2)    # Individual scale variation
            self.particles.append([
                spawn_pos,  # Position
                [0, 0],    # Velocity
                particle_size,
                [color_rgb[0], color_rgb[1], color_rgb[2], 255],
                random.uniform(0, math.pi * 2),  # Phase
                random.uniform(0, 8 * math.pi),  # Path progress
                random.uniform(0.001*self.speed, 0.003*self.speed),     # Individual speed
                particle_spread
            ])

    def render(self):
        position = 0
        velocity = 1
        size = 2
        color = 3
        phase = 4
        progress = 5
        speed = 6
        spread = 7  # Add spread factor for width variation

        for i in self.particles[:]:
            i[progress] += i[speed] * dt
            t = i[progress]
            
            # Base path with more even distribution
            base_x = width/2 + (width/3) * math.sin(t/3)
            base_y = floor/2 + (height/6) * math.cos(t*2)
            
            # Add spiral component
            spiral_x = math.cos(t) * t * 5
            spiral_y = math.sin(t) * t * 3
            
            # Combine with individual spread
            i[position][0] = base_x + spiral_x + math.sin(t) * i[spread] * 50  * self.scale_x
            i[position][1] = base_y + spiral_y + math.cos(t) * i[spread] * 30 * self.scale_y

            # Reset progress when reaching end of path
            if t > 8 * math.pi:
                i[progress] = 0

            # Add small wander
            wander_x = math.sin(i[phase]) * (height / 600)
            wander_y = math.cos(i[phase] * 0.5) * (height / 600)
           
            i[phase] += self.pulse_frequency * dt
            
            # Calculate pulse brightness
            pulse = (math.sin(i[phase]) + 1) * 0.5
            
            # Pixelation factor
            pixel_scale = 2


            screen_x = i[position][x] + wander_x + offset[x] - i[size] * 1.5
            screen_y = i[position][y] + wander_y + offset[y] - i[size] * 1.5

            if 0 < screen_x < width and 0 < screen_y < height:
            
                # Create smaller surface first
                small_size = 18
                small_surface = pygame.Surface((small_size, small_size), pygame.SRCALPHA)
                
                # Calculate scaled positions and sizes
                small_center = small_size / 2
                small_outer = max(1, int(i[size] * (0.7 + pulse * 0.3) / pixel_scale))
                small_core = max(1, int(i[size] * (0.2 + pulse * 0.3) / pixel_scale))
                
                # Calculate colors with pulse
                main_color = []
                for c in i[color][:3]:
                    whitened = int(c + (255 - c) * (0.45 + pulse * 0.3))
                    main_color.append(whitened)
                
                # Draw on small surface
                outer_alpha = int(5 + pulse * 10)
                pygame.draw.circle(small_surface, (*i[color][:3], outer_alpha),
                                (small_center, small_center),
                                small_outer)
                
                core_alpha = int(200 + pulse * 55)
                pygame.draw.circle(small_surface, WHITE,
                                (small_center, small_center),
                                small_core)
                
                
                
                # Scale up to final size
                final_size = int(i[size] * 3)
                glow_surface = pygame.transform.scale(small_surface, (final_size, final_size))
                
                # Blit with blend, adding wander offset to position
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
    conda = 0 < obj.pos[x] + offset[x] < width
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


# Usage in main game:
def play_intro_sequence():
    splash = SplashScreen()
    lore = LoreSequence()
    menu = MainMenu()

    running_intro = True
    running_menu = True
    
    play_music_long_fade(music_shroom, loops=0)

    start_trigger = False
    
    
    # Show splash screen first
    while running_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running_intro = False    
        screen.fill(BLACK)
        if splash.render():
            break
        pygame.display.flip()
        clock.tick(60)
    
    # Then show lore sequence
    while running_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running_intro = False                
        screen.fill(BLACK)
        if lore.render(screen):
            running_intro = False
        pygame.display.flip()
        clock.tick(60)
    
    # then show main menu
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
        if menu.render():
            menu.fading_out = True

            if not start_trigger:
                game_start_sound.play()
                pygame.mixer.music.unload()
                start_trigger = not start_trigger
        if menu.end_check == True:
            running_menu = False

        pygame.display.flip()
        clock.tick(60)

offset_target = [0, 0]
offset = [0, height * 10]
moving_L = False
moving_R = False

# Initialize game objects
player = Player()
game = Game()
killstreak = KillStreak()

# Create fireflies
fireflies_day = Fireflies(
    pos=[width/2, height/2],  # Center of screen
    count=80,                 # Number of fireflies
    size=6,                 # Size of fireflies
    color=colors['blue'][21],         # Warm yellow color
    spread=4000
)

fireflies_night = Fireflies(
    pos=[width/2, height/2],  # Center of screen
    count=80,                 # Number of fireflies
    size=6,                 # Size of fireflies
    color=colors['red'][21],         # Warm yellow color
    spread=4000,
    speed=5
)


dt = 1 # pre initialise dt before any class to prevent dt not defined
bg_pos = 0
bg_pos_targ = 0
player_pos_raw = [0, 0]
player_pos = [0, 0]
cursor_angle = 0
cursor_rotation = 0
cursor_player_displacement = 0
weapon_pos = [0, 0]
weapon_player_displacement = [0, 0]
weapon_angle = 0
weapon_rotation = 0

weapon_shop = WeaponShop([-width*1.5, floor])

buildings_array = [
    weapon_shop,

            ]

# for particles, more heavy objects
render_array = []

mushroom_array = []
mushroom_array_2 = []
meteor_array = []  # Add this new array

# for rendering entities mobs
entities_array = []
effects_array = [killstreak]


player_weapon_id = game.gamedata['weapons']
for id in player_weapon_id:
    player.weapons.append(weapon_shop.weapon_dict[id].copy())

environment = Environment()
weapon = player.weapons[player.current_weapon]
environment.fade_in()
cam_osc_base = 0
cam_osc = [0, 0]

# play intro here
play_intro_sequence()

# initialise dt here cuz i dont want dt to be messed up by the intro  
dt = 1
last_frame = pygame.time.get_ticks()

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

    # Find closest entity within snap radius
    closest_entity = None
    closest_dist = SNAP_RADIUS

    # snap function freezed
    """for entity_list in entities_array:
        for entity in entity_list:
            screen_pos = [entity.pos[x] + offset[x], entity.pos[y] + offset[y]]
            dist = get_distance(raw_mouse_pos, screen_pos)
            
            if dist < closest_dist:
                closest_dist = dist
                closest_entity = screen_pos

    # Smoothly snap cursor to entity if one is found
    if closest_entity is not None:
        mouse_pos[0] += (closest_entity[0] - mouse_pos[0]) * SNAP_SPEED
        mouse_pos[1] += (closest_entity[1] + 100 - mouse_pos[1]) * SNAP_SPEED"""
    

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

    if pygame.mouse.get_pressed()[0] and player.weapons:
        weapon.attack()

    # Camera and player position updates
    offset_target = [-player.steps + width / 2 - mouse_pos[0] * 0.8 + width * 0.4 + cam_osc[x],
                    -player.attitude + height * 0.8 - mouse_pos[1] * 0.8 + height * 0.25 + cam_osc[y]]
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

    # Render game world
    environment.render()

    # update and render buildings
    if environment.daynight > 0:
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

    if player.weapons:
        weapon = player.weapons[player.current_weapon]
        weapon_pos = [weapon.image.get_width() * -0.1 * math.sin(cursor_angle) + player_pos_raw[x],
                    weapon.image.get_height() * -0.2 * math.cos(cursor_angle) + player_pos_raw[y] + hip]
        weapon_player_displacement = [mouse_pos[x] - weapon_pos[x] - offset[x], 
                                    mouse_pos[y] - weapon_pos[y] - offset[y]]
        weapon_angle = math.atan2(weapon_player_displacement[x], weapon_player_displacement[y])
        weapon_rotation = (180 / math.pi) * weapon_angle - 90


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
    if player.weapons:
        weapon.render_hud()
    game.render_ui()
    environment.render_effects()

    # Update display
    pygame.display.update()
    clock.tick(-1)
    

if __name__ == "__main__":
    pygame.init()