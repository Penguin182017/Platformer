import pygame
import os

pygame.init()
pygame.mixer.init()

# Player effect state
player_effect = "normal"
player_effect_frame = 0
player_effect_timer = pygame.time.get_ticks()

# ============================================================
# GAME SETTINGS
# ============================================================

WIDTH = 1000
HEIGHT = 600
WORLD_WIDTH = 3000

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

CLOCK = pygame.time.Clock()
FPS = 60

BASE = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# SOUNDS
# ============================================================

SOUNDS = os.path.join(
    BASE,
    "Sounds(ZW)"
)

pygame.mixer.music.load(
    os.path.join(
        SOUNDS,
        "background.ogg"
    )
)

pygame.mixer.music.set_volume(0.75)
pygame.mixer.music.play(-1)


coin_sound = pygame.mixer.Sound(
    os.path.join(
        SOUNDS,
        "Coin.ogg"
    )
)

explosion_sound = pygame.mixer.Sound(
    os.path.join(
        SOUNDS,
        "Explosion.ogg"
    )
)

hit_sound = pygame.mixer.Sound(
    os.path.join(
        SOUNDS,
        "Hit.ogg"
    )
)

powerup_sound = pygame.mixer.Sound(
    os.path.join(
        SOUNDS,
        "Powerup.ogg"
    )
)

select_sound = pygame.mixer.Sound(
    os.path.join(
        SOUNDS,
        "Select.ogg"
    )
)

shoot_sound = pygame.mixer.Sound(
    os.path.join(
        SOUNDS,
        "Shoot.ogg"
    )
)


# ============================================================
# CAMERA
# ============================================================

camera_x = 0


# ============================================================
# CHARACTERS
# ============================================================

characters = {
    1: "MaskDude",
    2: "NinjaFrog",
    3: "PinkMan",
    4: "VirtualGuy"
}

character_number = 1
character_name = characters[character_number]


# ============================================================
# GROUND
# ============================================================

ground_y = 500


# ============================================================
# PLATFORMS
# ============================================================

platforms = [
    pygame.Rect(300, 420, 192, 16),
    pygame.Rect(650, 350, 192, 16),
    pygame.Rect(1000, 420, 256, 16),
    pygame.Rect(1350, 330, 192, 16),
    pygame.Rect(1700, 400, 256, 16),
    pygame.Rect(2100, 300, 192, 16),
    pygame.Rect(2500, 400, 256, 16)
]


# ============================================================
# PLATFORM SUPPORT HELPER
# ============================================================

def get_support_surface(rect):

    # Ground
    if abs(rect.bottom - ground_y) <= 3:
        return ground_y, None

    # Platforms
    for platform in platforms:

        if (
            abs(rect.bottom - platform.top) <= 3
            and rect.right > platform.left
            and rect.left < platform.right
        ):

            return platform.top, platform

    return None, None


# ============================================================
# LEVEL BACKGROUNDS
# ============================================================

level_background_names = [
    "Blue",
    "Green",
    "Brown",
    "Purple",
    "Pink",
    "Gray",
    "Yellow",
    "Blue",
    "Purple",
    "Green"
]

level_backgrounds = {}

for background_name in set(level_background_names):

    level_backgrounds[background_name] = pygame.image.load(
        os.path.join(
            BASE,
            "Background",
            background_name + ".png"
        )
    ).convert()

current_background = level_backgrounds["Blue"]


# ============================================================
# TERRAIN
# ============================================================

terrain = pygame.image.load(
    os.path.join(
        BASE,
        "Terrain",
        "Terrain.png"
    )
).convert_alpha()

TILE_SIZE = 16
TILE_DISPLAY = 64


def get_tile(number):

    number -= 1

    columns = terrain.get_width() // TILE_SIZE

    row = number // columns
    column = number % columns

    tile = pygame.Surface(
        (TILE_SIZE, TILE_SIZE),
        pygame.SRCALPHA
    )

    tile.blit(
        terrain,
        (0, 0),
        pygame.Rect(
            column * TILE_SIZE,
            row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
    )

    return pygame.transform.scale(
        tile,
        (
            TILE_DISPLAY,
            TILE_DISPLAY
        )
    )


# Different terrain styles for each level.
# These are all taken from the SAME Terrain.png asset sheet.
LEVEL_TILE_SETS = [
    (7, 8, 9),        # Level 1  - green grass
    (89, 90, 91),     # Level 2  - brown/wood
    (95, 96, 97),     # Level 3  - orange
    (101, 102, 103),  # Level 4  - gray stone
    (106, 107, 108),  # Level 5  - red brick
    (139, 140, 141),  # Level 6  - pink
    (189, 190, 191),  # Level 7  - orange trim
    (194, 195, 196),  # Level 8  - yellow
    (35, 36, 37),     # Level 9  - stone/brown
    (57, 58, 59)      # Level 10 - dark red/stone
]

current_tile_set = LEVEL_TILE_SETS[0]

grass_left = get_tile(
    current_tile_set[0]
)

grass_middle = get_tile(
    current_tile_set[1]
)

grass_right = get_tile(
    current_tile_set[2]
)


# ============================================================
# SPRITE SHEET LOADER
# ============================================================

def load_sprite_sheet(
    folder,
    filename,
    frame_size,
    display_size
):

    sheet = pygame.image.load(
        os.path.join(
            BASE,
            folder,
            filename
        )
    ).convert_alpha()

    frames = []

    frame_count = (
        sheet.get_width() //
        frame_size
    )

    for i in range(frame_count):

        frame = pygame.Surface(
            (
                frame_size,
                frame_size
            ),
            pygame.SRCALPHA
        )

        frame.blit(
            sheet,
            (0, 0),
            pygame.Rect(
                i * frame_size,
                0,
                frame_size,
                frame_size
            )
        )

        frame = pygame.transform.scale(
            frame,
            (
                display_size,
                display_size
            )
        )

        frames.append(frame)

    return frames


# ============================================================
# PLAYER ANIMATIONS
# ============================================================

PLAYER_SIZE = 64


def load_player_animation(filename):

    return load_sprite_sheet(
        os.path.join(
            "MainCharacters",
            character_name
        ),
        filename,
        32,
        PLAYER_SIZE
    )


def load_all_animations():

    global idle_frames
    global run_frames
    global jump_frames
    global double_jump_frames
    global fall_frames

    idle_frames = load_player_animation(
        "idle.png"
    )

    run_frames = load_player_animation(
        "run.png"
    )

    jump_frames = load_player_animation(
        "jump.png"
    )

    double_jump_frames = load_player_animation(
        "double_jump.png"
    )

    fall_frames = load_player_animation(
        "fall.png"
    )


load_all_animations()


# ============================================================
# APPEARING / DISAPPEARING EFFECTS
# ============================================================

def find_effect_file(folder, starts_with):

    for filename in os.listdir(folder):

        if filename.lower().startswith(
            starts_with.lower()
        ):

            return os.path.join(
                folder,
                filename
            )

    return None


def load_effect(filepath):

    sheet = pygame.image.load(
        filepath
    ).convert_alpha()

    frames = []

    frame_count = (
        sheet.get_width() // 96
    )

    for i in range(frame_count):

        frame = pygame.Surface(
            (96, 96),
            pygame.SRCALPHA
        )

        frame.blit(
            sheet,
            (0, 0),
            pygame.Rect(
                i * 96,
                0,
                96,
                96
            )
        )

        frames.append(frame)

    return frames


effect_folder = os.path.join(
    BASE,
    "MainCharacters"
)


appearing_file = find_effect_file(
    effect_folder,
    "Appearing"
)


disappearing_file = find_effect_file(
    effect_folder,
    "Desappearing"
)


if appearing_file is None:

    raise FileNotFoundError(
        "Appearing animation was not found in MainCharacters."
    )


if disappearing_file is None:

    raise FileNotFoundError(
        "Desappearing animation was not found in MainCharacters."
    )


appearing_frames = load_effect(
    appearing_file
)

disappearing_frames = load_effect(
    disappearing_file
)


# ============================================================
# ENEMIES
# ============================================================

enemy_characters = {
    1: "NinjaFrog",
    2: "PinkMan",
    3: "VirtualGuy",
    4: "MaskDude"
}

enemy_name = enemy_characters[
    character_number
]


def load_enemy():
    global enemy_frames
    global enemy_idle_frames
    global enemy_attack_frames

    enemy_folder = os.path.join(
        "MainCharacters",
        enemy_name
    )

    enemy_frames = load_sprite_sheet(
        enemy_folder,
        "run.png",
        32,
        64
    )

    idle_path = os.path.join(
        BASE,
        enemy_folder,
        "idle.png"
    )

    if os.path.exists(idle_path):
        enemy_idle_frames = load_sprite_sheet(
            enemy_folder,
            "idle.png",
            32,
            64
        )
    else:
        enemy_idle_frames = enemy_frames[:1]

    # Your assets do not need an attack.png.
    # If one exists, use it; otherwise use idle during the attack.
    attack_path = os.path.join(
        BASE,
        enemy_folder,
        "attack.png"
    )

    if os.path.exists(attack_path):
        enemy_attack_frames = load_sprite_sheet(
            enemy_folder,
            "attack.png",
            32,
            64
        )
    else:
        enemy_attack_frames = enemy_idle_frames[:1]


load_enemy()


ENEMY_SPEED = 3
ENEMY_DETECTION_RANGE = 500
ENEMY_ATTACK_COOLDOWN = 1000
ENEMY_DAMAGE = 10
ENEMY_KNOCKBACK_X = 12
ENEMY_KNOCKBACK_Y = -5
ENEMY_KNOCKBACK_TIME = 180

PLAYER_KNOCKBACK_X = 12
PLAYER_KNOCKBACK_Y = -6
PLAYER_KNOCKBACK_TIME = 250
player_knockback_until = 0

ENEMY_ATTACK_ANIMATION_TIME = 400

ENEMY_JUMP_COOLDOWN = 300
ENEMY_MAX_JUMPS = 2

ENEMY_PATROL_DISTANCE = 180
ENEMY_PATROL_SPEED = 2

MAX_ENEMY_HEALTH = 100

# Four enemies for the current world.
# They are independent: each has its own health, patrol,
# chase, jumping, knockback, attack and respawn timer.
ENEMY_START_POSITIONS = [
    (700, 436),
    (1250, 436),
    (1850, 436),
    (2450, 436)
]


class Enemy:
    def __init__(self, x, y):
        self.spawn_x = x
        self.spawn_y = y

        self.rect = pygame.Rect(
            x,
            y,
            64,
            64
        )

        self.health = MAX_ENEMY_HEALTH

        self.ai_state = "patrol"
        self.patrol_direction = 1

        self.patrol_left = (
            x - ENEMY_PATROL_DISTANCE
        )
        self.patrol_right = (
            x + ENEMY_PATROL_DISTANCE
        )

        self.velocity_y = 0
        self.jumps_left = ENEMY_MAX_JUMPS
        self.jumps_used = 0
        self.last_jump = -ENEMY_JUMP_COOLDOWN

        self.last_attack = -ENEMY_ATTACK_COOLDOWN
        self.attack_start = 0
        self.is_attacking = False
        self.attack_has_hit = False

        self.knockback_until = 0
        self.knockback_velocity_x = 0
        self.knockback_velocity_y = 0

        self.can_see_player = False

        self.effect = "appearing"
        self.effect_frame = 0
        self.effect_timer = pygame.time.get_ticks()

        self.respawn_at = 0

        self.hit_particles = []

    def reset(self):
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y

        self.health = MAX_ENEMY_HEALTH

        self.ai_state = "patrol"
        self.patrol_direction = 1

        self.velocity_y = 0
        self.jumps_left = ENEMY_MAX_JUMPS
        self.jumps_used = 0
        self.last_jump = -ENEMY_JUMP_COOLDOWN

        self.last_attack = (
            -ENEMY_ATTACK_COOLDOWN
        )
        self.attack_start = 0
        self.is_attacking = False
        self.attack_has_hit = False

        self.knockback_until = 0
        self.knockback_velocity_x = 0
        self.knockback_velocity_y = 0

        self.can_see_player = False

        self.effect = "appearing"
        self.effect_frame = 0
        self.effect_timer = pygame.time.get_ticks()

        self.respawn_at = 0

        self.hit_particles.clear()



# ============================================================
# MID BOSS / FINAL BOSS
# ============================================================

class Boss(Enemy):

    def __init__(self, x, y, boss_type="mid"):
        super().__init__(x, y)

        self.is_boss = True
        self.boss_type = boss_type

        if boss_type == "final":
            self.max_health = 500
            self.rect.width = 128
            self.rect.height = 128
        else:
            self.max_health = 250
            self.rect.width = 96
            self.rect.height = 96

        self.health = self.max_health
        self.spawn_x = x
        self.spawn_y = y
        self.patrol_left = x - 220
        self.patrol_right = x + 220

    def reset(self):
        super().reset()

        if self.boss_type == "final":
            self.max_health = 500
            self.rect.width = 128
            self.rect.height = 128
        else:
            self.max_health = 250
            self.rect.width = 96
            self.rect.height = 96

        self.health = self.max_health
        self.is_boss = True
        self.effect = "normal"
        self.respawn_at = 0

        self.patrol_left = self.spawn_x - 220
        self.patrol_right = self.spawn_x + 220


def create_bosses_for_level(level_number):

    if level_number == 5:
        return [
            Boss(
                max(900, WORLD_WIDTH - 750),
                ground_y - 96,
                "mid"
            )
        ]

    if level_number == 10:
        return [
            Boss(
                max(1000, WORLD_WIDTH - 550),
                ground_y - 128,
                "final"
            )
        ]

    return []


enemies = [
    Enemy(x, y)
    for x, y in ENEMY_START_POSITIONS
]

for _enemy in enemies:
    _enemy.is_boss = False
    _enemy.boss_type = ""

# Compatibility name for any remaining code that expects `enemy`.
enemy = enemies[0].rect

# Compatibility values; the real values are stored per enemy.
enemy_health = MAX_ENEMY_HEALTH
enemy_effect = "normal"
enemy_ai_state = "patrol"

# ============================================================
# PLAYER HEALTH
# ============================================================

MAX_HEALTH = 100
health = MAX_HEALTH

# ============================================================
# SHIELD POWER-UP
# ============================================================

SHIELD_DURATION = 6000
shield_active = False
shield_until = 0

# Speed boost power-up
SPEED_BOOST_DURATION = 6000
NORMAL_player_speed = 5
player_speed = NORMAL_player_speed
SPEED_BOOST_MULTIPLIER = 3.0
speed_boost_active = False
speed_boost_until = 0

DAMAGE = 10

# ============================================================
# DAMAGE BOOST POWER-UP
# ============================================================

DAMAGE_BOOST_DURATION = 6000
NORMAL_ATTACK_DAMAGE = 25
DAMAGE_BOOST_MULTIPLIER = 2
damage_boost_active = False

# Fun movement/combo systems
DASH_DISTANCE = 180
DASH_COOLDOWN = 900
DASH_DURATION = 140
dash_until = 0
dash_cooldown_until = 0
dash_direction = 1

COIN_COMBO_TIME = 1400
coin_combo = 0
coin_combo_until = 0
damage_boost_until = 0

INVINCIBLE_TIME = 1000
last_damage_time = 0


# ============================================================
# ENEMY HEALTH
# ============================================================

MAX_ENEMY_HEALTH = 100


# ============================================================
# ATTACK
# ============================================================

ATTACK_DAMAGE = 25
ATTACK_TIME = 200
ATTACK_COOLDOWN = 400

attacking = False
attack_start_time = 0
last_attack_time = 0


# ============================================================
# SCORE
# ============================================================

score = 0


# ============================================================
# COINS
# ============================================================

COIN_SIZE = 28

coin_positions = [
    (500, 460),
    (850, 310),
    (1150, 380),
    (1500, 290),
    (1900, 360),
    (2250, 260),
    (2650, 360),
    (2900, 460)
]


def load_coin_frames():

    possible_files = [
        os.path.join(BASE, "Items", "Coin", "Coin.png"),
        os.path.join(BASE, "Items", "Coins", "Coin.png"),
        os.path.join(BASE, "Items", "Coin.png")
    ]

    for filepath in possible_files:

        if os.path.exists(filepath):

            sheet = pygame.image.load(
                filepath
            ).convert_alpha()

            frames = []

            frame_count = max(
                1,
                sheet.get_width() // 32
            )

            for i in range(frame_count):

                frame = pygame.Surface(
                    (32, 32),
                    pygame.SRCALPHA
                )

                frame.blit(
                    sheet,
                    (0, 0),
                    pygame.Rect(
                        i * 32,
                        0,
                        32,
                        32
                    )
                )

                frames.append(
                    pygame.transform.scale(
                        frame,
                        (COIN_SIZE, COIN_SIZE)
                    )
                )

            return frames

    return None


coin_frames = load_coin_frames()


def create_coins():

    result = []

    for x, y in coin_positions:

        result.append({
            "rect": pygame.Rect(
                x,
                y,
                COIN_SIZE,
                COIN_SIZE
            ),
            "collected": False
        })

    return result


coins = create_coins()


# ============================================================
# SHIELD POWER-UP POSITIONS
# ============================================================

shield_positions = [
    (900, 460),
    (1600, 360),
    (2350, 260)
]

SHIELD_SIZE = 30


def create_shields():

    result = []

    for x, y in shield_positions:

        result.append({
            "rect": pygame.Rect(
                x,
                y,
                SHIELD_SIZE,
                SHIELD_SIZE
            ),
            "collected": False
        })

    return result


shields = create_shields()


# ============================================================
# SPEED BOOST PICK-UPS
# ============================================================

speed_positions = [
    (1100, 460),
    (2050, 360),
    (2750, 460)
]

SPEED_SIZE = 28


def create_speed_boosts():

    result = []

    for x, y in speed_positions:

        result.append({
            "rect": pygame.Rect(
                x,
                y,
                SPEED_SIZE,
                SPEED_SIZE
            ),
            "collected": False
        })

    return result


speed_boosts = create_speed_boosts()


# ============================================================
# DAMAGE BOOST PICK-UPS
# ============================================================

damage_positions = [
    (1300, 460),
    (2200, 360),
    (2850, 460)
]

DAMAGE_BOOST_SIZE = 28


def create_damage_boosts():

    result = []

    for x, y in damage_positions:

        result.append({
            "rect": pygame.Rect(
                x,
                y,
                DAMAGE_BOOST_SIZE,
                DAMAGE_BOOST_SIZE
            ),
            "collected": False
        })

    return result


damage_boosts = create_damage_boosts()


# ============================================================
# LEVEL-SPECIFIC POWER-UP POSITIONS
# ============================================================

LEVEL_POWERUP_POSITIONS = [
    # Level 1
    {
        "speed": [(1100, 460), (2050, 360), (2750, 460)],
        "shield": [(900, 460), (1600, 360), (2350, 260)],
        "damage": [(1300, 460), (2200, 360), (2850, 460)]
    },
    # Level 2
    {
        "speed": [(520, 310), (1510, 320), (2550, 250)],
        "shield": [(880, 360), (1840, 240), (3000, 420)],
        "damage": [(1180, 250), (2220, 360), (3100, 420)]
    },
    # Level 3
    {
        "speed": [(570, 430), (1510, 240), (2500, 220)],
        "shield": [(850, 260), (1810, 390), (2900, 420)],
        "damage": [(1160, 350), (2110, 290), (3150, 420)]
    },
    # Level 4
    {
        "speed": [(560, 420), (1470, 220), (2450, 390)],
        "shield": [(900, 220), (1810, 320), (2850, 420)],
        "damage": [(1170, 340), (2100, 230), (3050, 420)]
    },
    # Level 5 - Mid Boss
    {
        "speed": [(500, 320), (1340, 260), (2240, 190)],
        "shield": [(780, 180), (1660, 380), (2520, 350)],
        "damage": [(1080, 340), (1930, 260), (2800, 420)]
    },
    # Level 6
    {
        "speed": [(500, 400), (1040, 190), (2200, 250)],
        "shield": [(790, 290), (1600, 220), (2500, 170)],
        "damage": [(1340, 330), (1940, 360), (2850, 420)]
    },
    # Level 7
    {
        "speed": [(530, 240), (1370, 180), (2240, 360)],
        "shield": [(820, 380), (1630, 320), (2500, 240)],
        "damage": [(1080, 270), (1980, 210), (2850, 420)]
    },
    # Level 8
    {
        "speed": [(520, 350), (1340, 260), (2200, 200)],
        "shield": [(780, 260), (1620, 160), (2470, 350)],
        "damage": [(1090, 380), (1900, 320), (2850, 420)]
    },
    # Level 9
    {
        "speed": [(470, 260), (1260, 210), (2080, 140), (2600, 200)],
        "shield": [(730, 160), (1530, 370), (2350, 300)],
        "damage": [(1010, 320), (1800, 240), (2500, 180)]
    },
    # Level 10 - Final Boss
    {
        "speed": [(450, 190), (1200, 110), (1990, 330)],
        "shield": [(700, 360), (1470, 300), (2250, 210)],
        "damage": [(950, 220), (1720, 170), (2500, 100)]
    }
]


def create_level_powerups(level_number):

    data = LEVEL_POWERUP_POSITIONS[
        level_number - 1
    ]

    speed = [
        {
            "rect": pygame.Rect(
                x,
                y,
                SPEED_SIZE,
                SPEED_SIZE
            ),
            "collected": False
        }
        for x, y in data["speed"]
    ]

    shield = [
        {
            "rect": pygame.Rect(
                x,
                y,
                SHIELD_SIZE,
                SHIELD_SIZE
            ),
            "collected": False
        }
        for x, y in data["shield"]
    ]

    damage = [
        {
            "rect": pygame.Rect(
                x,
                y,
                DAMAGE_BOOST_SIZE,
                DAMAGE_BOOST_SIZE
            ),
            "collected": False
        }
        for x, y in data["damage"]
    ]

    return speed, shield, damage


def draw_damage_boost(surface, rect, camera):

    x = rect.centerx - camera
    y = rect.centery

    # Cross/sword-like damage symbol
    pygame.draw.rect(
        surface,
        (255, 80, 80),
        (x - 4, y - 12, 8, 24)
    )

    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (x - 10, y - 3, 20, 6)
    )

    pygame.draw.circle(
        surface,
        (255, 220, 60),
        (x, y),
        15,
        2
    )


def draw_speed_boost(surface, rect, camera):

    x = rect.centerx - camera
    y = rect.centery

    points = [
        (x + 3, y - 14),
        (x - 4, y - 2),
        (x + 1, y - 2),
        (x - 4, y + 14),
        (x + 6, y),
        (x + 1, y)
    ]

    pygame.draw.polygon(
        surface,
        (255, 230, 40),
        points
    )

    pygame.draw.polygon(
        surface,
        (255, 255, 255),
        points,
        2
    )


def draw_shield(surface, rect, camera):

    x = rect.centerx - camera
    y = rect.centery

    points = [
        (x, y - 14),
        (x + 12, y - 8),
        (x + 10, y + 7),
        (x, y + 15),
        (x - 10, y + 7),
        (x - 12, y - 8)
    ]

    pygame.draw.polygon(
        surface,
        (80, 180, 255),
        points
    )

    pygame.draw.polygon(
        surface,
        (255, 255, 255),
        points,
        2
    )


coins = create_coins()


# Fallback coin drawing if no coin image exists.
def draw_coin(surface, rect, camera):

    x = rect.centerx - camera
    y = rect.centery

    pygame.draw.circle(
        surface,
        (255, 215, 0),
        (x, y),
        COIN_SIZE // 2
    )

    pygame.draw.circle(
        surface,
        (180, 130, 0),
        (x, y),
        COIN_SIZE // 2,
        2
    )

    pygame.draw.rect(
        surface,
        (180, 130, 0),
        (
            x - 2,
            y - 7,
            4,
            14
        )
    )


# ============================================================
# FRUITS
# ============================================================

FRUIT_SIZE = 48

fruit_heal = {
    "Apple.png": 5,
    "Bananas.png": 10,
    "Cherries.png": 15,
    "Kiwi.png": 20,
    "Melon.png": 25,
    "Orange.png": 30,
    "Pineapple.png": 40,
    "Strawberry.png": 50
}


fruit_data = {
    "Apple.png": 10,
    "Bananas.png": 15,
    "Cherries.png": 20,
    "Kiwi.png": 25,
    "Melon.png": 30,
    "Orange.png": 35,
    "Pineapple.png": 40,
    "Strawberry.png": 50
}


fruit_animations = {}


for filename in fruit_data:

    fruit_sheet = pygame.image.load(
        os.path.join(
            BASE,
            "Items",
            "Fruits",
            filename
        )
    ).convert_alpha()

    frames = []

    frame_count = (
        fruit_sheet.get_width() // 32
    )

    for i in range(frame_count):

        fruit_frame = pygame.Surface(
            (32, 32),
            pygame.SRCALPHA
        )

        fruit_frame.blit(
            fruit_sheet,
            (0, 0),
            pygame.Rect(
                i * 32,
                0,
                32,
                32
            )
        )

        fruit_frame = pygame.transform.scale(
            fruit_frame,
            (
                FRUIT_SIZE,
                FRUIT_SIZE
            )
        )

        frames.append(
            fruit_frame
        )

    fruit_animations[
        filename
    ] = frames


# ============================================================
# FRUIT POSITIONS
# ============================================================

fruit_positions = [
    (350, "Apple.png"),
    (700, "Bananas.png"),
    (1050, "Cherries.png"),
    (1400, "Kiwi.png"),
    (1750, "Melon.png"),
    (2100, "Orange.png"),
    (2450, "Pineapple.png"),
    (2800, "Strawberry.png")
]


# Fruit positions for each level.
# The second value is the platform/ground Y position.
# Fruits on higher platforms force the player to jump.
LEVEL_FRUIT_POSITIONS = [
    [
        (350, ground_y - FRUIT_SIZE, "Apple.png"),
        (700, 350 - FRUIT_SIZE, "Bananas.png"),
        (1050, ground_y - FRUIT_SIZE, "Cherries.png"),
        (1400, 330 - FRUIT_SIZE, "Kiwi.png"),
        (1750, ground_y - FRUIT_SIZE, "Melon.png"),
        (2100, 300 - FRUIT_SIZE, "Orange.png"),
        (2450, ground_y - FRUIT_SIZE, "Pineapple.png"),
        (2800, ground_y - FRUIT_SIZE, "Strawberry.png")
    ],
    [
        (300, ground_y - FRUIT_SIZE, "Apple.png"),
        (540, 310 - FRUIT_SIZE, "Bananas.png"),
        (880, 400 - FRUIT_SIZE, "Cherries.png"),
        (1180, 280 - FRUIT_SIZE, "Kiwi.png"),
        (1510, 370 - FRUIT_SIZE, "Melon.png"),
        (1840, 300 - FRUIT_SIZE, "Orange.png"),
        (2220, 390 - FRUIT_SIZE, "Pineapple.png"),
        (2550, 300 - FRUIT_SIZE, "Strawberry.png")
    ],
    [
        (260, 350 - FRUIT_SIZE, "Apple.png"),
        (570, ground_y - FRUIT_SIZE, "Bananas.png"),
        (850, 300 - FRUIT_SIZE, "Cherries.png"),
        (1160, 390 - FRUIT_SIZE, "Kiwi.png"),
        (1510, 270 - FRUIT_SIZE, "Melon.png"),
        (1810, ground_y - FRUIT_SIZE, "Orange.png"),
        (2110, 330 - FRUIT_SIZE, "Pineapple.png"),
        (2500, 250 - FRUIT_SIZE, "Strawberry.png")
    ],
    [
        (300, 300 - FRUIT_SIZE, "Apple.png"),
        (560, 420 - FRUIT_SIZE, "Bananas.png"),
        (900, 280 - FRUIT_SIZE, "Cherries.png"),
        (1170, 380 - FRUIT_SIZE, "Kiwi.png"),
        (1470, 250 - FRUIT_SIZE, "Melon.png"),
        (1810, 350 - FRUIT_SIZE, "Orange.png"),
        (2100, 260 - FRUIT_SIZE, "Pineapple.png"),
        (2450, 390 - FRUIT_SIZE, "Strawberry.png")
    ],
    [
        (260, ground_y - FRUIT_SIZE, "Apple.png"),
        (500, 320 - FRUIT_SIZE, "Bananas.png"),
        (780, 240 - FRUIT_SIZE, "Cherries.png"),
        (1080, 380 - FRUIT_SIZE, "Kiwi.png"),
        (1340, 290 - FRUIT_SIZE, "Melon.png"),
        (1660, 410 - FRUIT_SIZE, "Orange.png"),
        (1930, 300 - FRUIT_SIZE, "Pineapple.png"),
        (2240, 220 - FRUIT_SIZE, "Strawberry.png"),
        (2520, 380 - FRUIT_SIZE, "Apple.png")
    ],
    [
        (220, 300 - FRUIT_SIZE, "Apple.png"),
        (500, 420 - FRUIT_SIZE, "Bananas.png"),
        (790, 330 - FRUIT_SIZE, "Cherries.png"),
        (1040, 230 - FRUIT_SIZE, "Kiwi.png"),
        (1340, 370 - FRUIT_SIZE, "Melon.png"),
        (1600, 260 - FRUIT_SIZE, "Orange.png"),
        (1940, 400 - FRUIT_SIZE, "Pineapple.png"),
        (2200, 290 - FRUIT_SIZE, "Strawberry.png"),
        (2500, 210 - FRUIT_SIZE, "Apple.png")
    ],
    [
        (300, 390 - FRUIT_SIZE, "Apple.png"),
        (530, 270 - FRUIT_SIZE, "Bananas.png"),
        (820, ground_y - FRUIT_SIZE, "Cherries.png"),
        (1080, 300 - FRUIT_SIZE, "Kiwi.png"),
        (1370, 220 - FRUIT_SIZE, "Melon.png"),
        (1630, 360 - FRUIT_SIZE, "Orange.png"),
        (1980, 250 - FRUIT_SIZE, "Pineapple.png"),
        (2240, 400 - FRUIT_SIZE, "Strawberry.png"),
        (2500, 280 - FRUIT_SIZE, "Apple.png")
    ],
    [
        (250, 250 - FRUIT_SIZE, "Apple.png"),
        (520, 380 - FRUIT_SIZE, "Bananas.png"),
        (780, 290 - FRUIT_SIZE, "Cherries.png"),
        (1090, ground_y - FRUIT_SIZE, "Kiwi.png"),
        (1340, 300 - FRUIT_SIZE, "Melon.png"),
        (1620, 200 - FRUIT_SIZE, "Orange.png"),
        (1900, 350 - FRUIT_SIZE, "Pineapple.png"),
        (2200, 240 - FRUIT_SIZE, "Strawberry.png"),
        (2470, 390 - FRUIT_SIZE, "Apple.png")
    ],
    [
        (220, ground_y - FRUIT_SIZE, "Apple.png"),
        (470, 290 - FRUIT_SIZE, "Bananas.png"),
        (730, 190 - FRUIT_SIZE, "Cherries.png"),
        (1010, 350 - FRUIT_SIZE, "Kiwi.png"),
        (1260, 240 - FRUIT_SIZE, "Melon.png"),
        (1530, 400 - FRUIT_SIZE, "Orange.png"),
        (1800, 270 - FRUIT_SIZE, "Pineapple.png"),
        (2080, 170 - FRUIT_SIZE, "Strawberry.png"),
        (2350, 330 - FRUIT_SIZE, "Apple.png"),
        (2600, 230 - FRUIT_SIZE, "Bananas.png")
    ],
    [
        (220, 350 - FRUIT_SIZE, "Apple.png"),
        (450, 220 - FRUIT_SIZE, "Bananas.png"),
        (700, 390 - FRUIT_SIZE, "Cherries.png"),
        (950, 270 - FRUIT_SIZE, "Kiwi.png"),
        (1200, 160 - FRUIT_SIZE, "Melon.png"),
        (1470, 340 - FRUIT_SIZE, "Orange.png"),
        (1720, 210 - FRUIT_SIZE, "Pineapple.png"),
        (1990, 380 - FRUIT_SIZE, "Strawberry.png"),
        (2250, 250 - FRUIT_SIZE, "Apple.png"),
        (2500, 140 - FRUIT_SIZE, "Bananas.png"),
        (2740, 320 - FRUIT_SIZE, "Cherries.png")
    ]
]



# ============================================================
# CREATE FRUITS
# ============================================================

def create_fruits(positions=None):

    if positions is None:
        positions = [
            (
                x,
                ground_y - FRUIT_SIZE,
                filename
            )
            for x, filename in fruit_positions
        ]

    result = []

    for x, y, filename in positions:

        result.append({

            "rect": pygame.Rect(
                x,
                y,
                FRUIT_SIZE,
                FRUIT_SIZE
            ),

            "frames": fruit_animations[
                filename
            ],

            "points": fruit_data[
                filename
            ],

            "heal": fruit_heal[
                filename
            ]

        })

    return result



fruits = create_fruits()



# ============================================================
# CHECKPOINT SYSTEM
# ============================================================

CHECKPOINT_SIZE = 64

# These are respawn checkpoints, not the final finish flag.
CHECKPOINT_POSITIONS = [
    (900, ground_y),
    (1700, ground_y),
    (2450, ground_y)
]

checkpoints = [
    {
        "rect": pygame.Rect(
            x,
            y - CHECKPOINT_SIZE,
            CHECKPOINT_SIZE,
            CHECKPOINT_SIZE
        ),
        "activated": False
    }
    for x, y in CHECKPOINT_POSITIONS
]

active_checkpoint = -1

# Default starting spawn.
respawn_x = 150
respawn_y = 400


# ============================================================
# REAL CHECKPOINT ASSETS
# ============================================================

CHECKPOINT_IDLE_PATH = os.path.join(
    BASE,
    "Items",
    "Checkpoints",
    "Checkpoint",
    "Checkpoint (Flag Idle)(64x64).png"
)

CHECKPOINT_OUT_PATH = os.path.join(
    BASE,
    "Items",
    "Checkpoints",
    "Checkpoint",
    "Checkpoint (Flag Out) (64x64).png"
)

CHECKPOINT_NO_FLAG_PATH = os.path.join(
    BASE,
    "Items",
    "Checkpoints",
    "Checkpoint",
    "Checkpoint (No Flag).png"
)


def load_checkpoint_frame(filepath, frame_index=0):

    sheet = pygame.image.load(
        filepath
    ).convert_alpha()

    frame_count = max(
        1,
        sheet.get_width() // CHECKPOINT_SIZE
    )

    frame_index = min(
        frame_index,
        frame_count - 1
    )

    frame = pygame.Surface(
        (CHECKPOINT_SIZE, CHECKPOINT_SIZE),
        pygame.SRCALPHA
    )

    frame.blit(
        sheet,
        (0, 0),
        pygame.Rect(
            frame_index * CHECKPOINT_SIZE,
            0,
            CHECKPOINT_SIZE,
            CHECKPOINT_SIZE
        )
    )

    return frame


checkpoint_idle_image = load_checkpoint_frame(
    CHECKPOINT_IDLE_PATH,
    0
)

checkpoint_out_image = load_checkpoint_frame(
    CHECKPOINT_OUT_PATH,
    0
)

checkpoint_no_flag_image = pygame.image.load(
    CHECKPOINT_NO_FLAG_PATH
).convert_alpha()

checkpoint_no_flag_image = pygame.transform.scale(
    checkpoint_no_flag_image,
    (CHECKPOINT_SIZE, CHECKPOINT_SIZE)
)


def draw_checkpoint(surface, checkpoint, camera):

    rect = checkpoint["rect"]

    if checkpoint["activated"]:
        image = checkpoint_out_image
    else:
        image = checkpoint_no_flag_image

    surface.blit(
        image,
        (
            rect.x - camera,
            rect.y
        )
    )


# ============================================================
# FINISH / WIN SYSTEM
# ============================================================

FINISH_X = WORLD_WIDTH - 120
FINISH_SIZE = 64

FINISH_RECT = pygame.Rect(
    FINISH_X,
    ground_y - 10,
    FINISH_SIZE,
    10
)

game_won = False

death_respawn_at = 0

# HOW TO PLAY

# ============================================================
# LEVEL LOADING
# ============================================================

def load_selected_level(level_number):
    """
    Fully reset and load the requested level.

    Every level gets:
    - fresh fruits
    - a fresh checkpoint state
    - a different platform layout
    - reset enemies
    - a fresh player/score state
    """

    global current_level
    global health
    global velocity_x
    global velocity_y
    global jumps_left
    global attacking
    global game_won
    global game_paused
    global finish_message
    global finish_message_until
    global respawn_x
    global respawn_y
    global death_respawn_at
    global level_unlock_processed
    global fruits
    global platforms
    global checkpoints
    global active_checkpoint
    global speed_boosts
    global shields
    global damage_boosts
    global player_speed
    global speed_boost_active
    global speed_boost_until
    global shield_active
    global shield_until
    global damage_boost_active
    global damage_boost_until
    global ATTACK_DAMAGE
    global dash_until
    global dash_cooldown_until
    global dash_direction
    global coin_combo
    global coin_combo_until
    global enemies
    global WORLD_WIDTH
    global FINISH_X
    global FINISH_RECT
    global current_background
    global current_tile_set
    global grass_left
    global grass_middle
    global grass_right

    current_level = max(
        1,
        min(
            TOTAL_LEVELS,
            int(level_number)
        )
    )

    # Each level has its own world width.
    level_widths = [
        3000,
        3400,
        3700,
        3200,
        4000,
        4300,
        3600,
        4500,
        4800,
        5200
    ]

    WORLD_WIDTH = level_widths[
        current_level - 1
    ]

    # Each level has a different background from the supplied assets.
    current_background = level_backgrounds[
        level_background_names[
            current_level - 1
        ]
    ]

    # Each level uses a different terrain style from Terrain.png.
    current_tile_set = LEVEL_TILE_SETS[
        current_level - 1
    ]

    grass_left = get_tile(
        current_tile_set[0]
    )

    grass_middle = get_tile(
        current_tile_set[1]
    )

    grass_right = get_tile(
        current_tile_set[2]
    )

    # Move the finish flag to the end of THIS level.
    FINISH_X = WORLD_WIDTH - 120

    FINISH_RECT = pygame.Rect(
        FINISH_X,
        ground_y - 10,
        FINISH_SIZE,
        10
    )

    # ------------------------------------------------------------
    dash_until = 0
    dash_cooldown_until = 0
    dash_direction = 1
    coin_combo = 0
    coin_combo_until = 0

    # RESET POWER-UPS FOR THIS LEVEL
    # ------------------------------------------------------------

    (
        speed_boosts,
        shields,
        damage_boosts
    ) = create_level_powerups(
        current_level
    )

    player_speed = NORMAL_player_speed
    speed_boost_active = False
    speed_boost_until = 0

    shield_active = False
    shield_until = 0

    damage_boost_active = False
    damage_boost_until = 0

    ATTACK_DAMAGE = NORMAL_ATTACK_DAMAGE

    # Different platform layouts for each level.
    layouts = [
        [
            (300, 420, 192, 16),
            (650, 350, 192, 16),
            (1000, 420, 256, 16),
            (1350, 330, 192, 16),
            (1700, 400, 256, 16),
            (2100, 300, 192, 16),
            (2500, 400, 256, 16)
        ],
        [
            (260, 390, 160, 16),
            (540, 310, 220, 16),
            (880, 400, 180, 16),
            (1180, 280, 220, 16),
            (1510, 370, 180, 16),
            (1840, 300, 240, 16),
            (2220, 390, 180, 16),
            (2550, 300, 220, 16)
        ],
        [
            (240, 350, 220, 16),
            (570, 430, 160, 16),
            (850, 300, 180, 16),
            (1160, 390, 240, 16),
            (1510, 270, 180, 16),
            (1810, 420, 180, 16),
            (2110, 330, 240, 16),
            (2500, 250, 180, 16)
        ],
        [
            (300, 300, 170, 16),
            (560, 420, 200, 16),
            (900, 280, 170, 16),
            (1170, 380, 190, 16),
            (1470, 250, 220, 16),
            (1810, 350, 170, 16),
            (2100, 260, 210, 16),
            (2450, 390, 230, 16)
        ],
        [
            (260, 430, 150, 16),
            (500, 320, 170, 16),
            (780, 240, 190, 16),
            (1080, 380, 150, 16),
            (1340, 290, 210, 16),
            (1660, 410, 170, 16),
            (1930, 300, 190, 16),
            (2240, 220, 170, 16),
            (2520, 380, 230, 16)
        ],
        [
            (220, 300, 180, 16),
            (500, 420, 180, 16),
            (790, 330, 150, 16),
            (1040, 230, 190, 16),
            (1340, 370, 160, 16),
            (1600, 260, 220, 16),
            (1940, 400, 150, 16),
            (2200, 290, 200, 16),
            (2500, 210, 200, 16)
        ],
        [
            (300, 390, 150, 16),
            (530, 270, 180, 16),
            (820, 410, 160, 16),
            (1080, 300, 180, 16),
            (1370, 220, 160, 16),
            (1630, 360, 220, 16),
            (1980, 250, 170, 16),
            (2240, 400, 160, 16),
            (2500, 280, 210, 16)
        ],
        [
            (250, 250, 180, 16),
            (520, 380, 150, 16),
            (780, 290, 190, 16),
            (1090, 410, 150, 16),
            (1340, 300, 180, 16),
            (1620, 200, 180, 16),
            (1900, 350, 200, 16),
            (2200, 240, 160, 16),
            (2470, 390, 220, 16)
        ],
        [
            (220, 410, 150, 16),
            (470, 290, 160, 16),
            (730, 190, 180, 16),
            (1010, 350, 150, 16),
            (1260, 240, 180, 16),
            (1530, 400, 160, 16),
            (1800, 270, 180, 16),
            (2080, 170, 180, 16),
            (2350, 330, 170, 16),
            (2600, 230, 180, 16)
        ],
        [
            (220, 350, 140, 16),
            (450, 220, 150, 16),
            (700, 390, 140, 16),
            (950, 270, 150, 16),
            (1200, 160, 160, 16),
            (1470, 340, 150, 16),
            (1720, 210, 160, 16),
            (1990, 380, 150, 16),
            (2250, 250, 160, 16),
            (2500, 140, 170, 16),
            (2740, 320, 150, 16)
        ]
    ]

    selected_layout = layouts[
        current_level - 1
    ]

    platforms = [
        pygame.Rect(
            x,
            y,
            width,
            height
        )
        for x, y, width, height
        in selected_layout
    ]

    # Fresh fruits for THIS level.
    # Many are elevated so the player must actually jump to collect them.
    fruits = create_fruits(
        LEVEL_FRUIT_POSITIONS[
            current_level - 1
        ]
    )

    # ------------------------------------------------------------
    # BOSS FOR THIS LEVEL
    # Level 5 = Mid Boss
    # Level 10 = Final Boss
    # ------------------------------------------------------------

    enemies[:] = [
        e for e in enemies
        if not getattr(e, "is_boss", False)
    ]

    for boss_obj in create_bosses_for_level(current_level):
        enemies.append(boss_obj)

    # ------------------------------------------------------------
    # LEVEL DIFFICULTY
    # ------------------------------------------------------------

    difficulty_multiplier = 1.0 + (
        (current_level - 1) * 0.07
    )

    for enemy_obj in enemies:
        if not getattr(
            enemy_obj,
            "is_boss",
            False
        ):

            if hasattr(enemy_obj, "speed"):
                enemy_obj.speed = (
                    getattr(
                        enemy_obj,
                        "base_speed",
                        enemy_obj.speed
                    )
                    * difficulty_multiplier
                )

            if hasattr(enemy_obj, "velocity_x"):
                enemy_obj.velocity_x *= (
                    difficulty_multiplier
                )


    # Reset checkpoints.
    checkpoints = [
        {
            "rect": pygame.Rect(
                x,
                y - CHECKPOINT_SIZE,
                CHECKPOINT_SIZE,
                CHECKPOINT_SIZE
            ),
            "activated": False
        }
        for x, y in CHECKPOINT_POSITIONS
    ]

    active_checkpoint = -1

    respawn_x = 150
    respawn_y = 400

    health = MAX_HEALTH
    velocity_x = 0
    velocity_y = 0
    jumps_left = 2
    attacking = False

    game_won = False
    game_paused = False
    finish_message = ""
    finish_message_until = 0
    death_respawn_at = 0
    level_unlock_processed = False

    player.x = respawn_x
    player.y = respawn_y

    player_x = float(player.x)
    player_y = float(player.y)

    # Reset enemies.
    for enemy_obj in enemies:
        try:
            enemy_obj.reset()
        except Exception:
            pass



menu_open = True
menu_selection = 0
MENU_ITEMS = ["PLAY", "LEVEL SELECT", "HOW TO PLAY", "SETTINGS", "QUIT"]

# ============================================================
# SETTINGS
# ============================================================

settings_open = False
settings_selection = 0

# Level Select
level_select_open = False
selected_level = 0
TOTAL_LEVELS = 10
current_level = 1
unlocked_levels = 1
completed_levels = set()
level_unlock_processed = False

music_volume = 0.60
sfx_volume = 0.80
music_muted = False

SETTINGS_ITEMS = [
    "MUSIC VOLUME",
    "SOUND EFFECTS",
    "MUTE MUSIC",
    "BACK"
]

show_help = False
help_from_game = False

# Game-over screen
finish_message = ""
finish_message_until = 0

# Pause menu
game_paused = False

# Positions captured at the exact moment of victory.
frozen_player_x = 0
frozen_player_y = 0
frozen_velocity_x = 0
frozen_velocity_y = 0
frozen_enemy_positions = []

# YOUR REAL FINISH ASSETS
FINISH_IDLE_PATH = os.path.join(
    BASE,
    "Items",
    "Checkpoints",
    "End",
    "End (Idle).png"
)

FINISH_PRESSED_PATH = os.path.join(
    BASE,
    "Items",
    "Checkpoints",
    "End",
    "End (Pressed) (64x64).png"
)

finish_idle_image = pygame.image.load(
    FINISH_IDLE_PATH
).convert_alpha()

finish_idle_image = pygame.transform.scale(
    finish_idle_image,
    (FINISH_SIZE, FINISH_SIZE)
)

finish_pressed_image = None

if os.path.exists(FINISH_PRESSED_PATH):

    pressed_sheet = pygame.image.load(
        FINISH_PRESSED_PATH
    ).convert_alpha()

    # End (Pressed) is a sprite sheet: 8 frames of 64x64.
    # Take ONLY ONE frame so the flag is not drawn 8 times.
    finish_pressed_image = pygame.Surface(
        (FINISH_SIZE, FINISH_SIZE),
        pygame.SRCALPHA
    )

    finish_pressed_image.blit(
        pressed_sheet,
        (0, 0),
        pygame.Rect(
            0,
            0,
            FINISH_SIZE,
            FINISH_SIZE
        )
    )


def all_fruits_collected():
    return len(fruits) == 0



fruits = create_fruits()


# ============================================================
# FRUIT EFFECTS
# ============================================================

fruit_effects = []

heal_popups = []


# ============================================================
# PLAYER POSITION
# ============================================================

player = pygame.Rect(
    150,
    400,
    50,
    64
)

player_x = float(player.x)
player_y = float(player.y)

velocity_x = 0
velocity_y = 0

GRAVITY = 0.7
JUMP_POWER = -13

jumps_left = 2

facing_right = True


# ============================================================
# JUMP
# ============================================================

def jump():

    global velocity_y
    global jumps_left

    if jumps_left > 0:

        velocity_y = JUMP_POWER

        jumps_left -= 1


# ============================================================
# PLAYER APPEARING
# ============================================================

def start_player_appearing():

    global player_effect
    global player_effect_frame
    global player_effect_timer

    player_effect = "appearing"

    player_effect_frame = 0

    player_effect_timer = pygame.time.get_ticks()


# ============================================================
# FONT
# ============================================================

score_font = pygame.font.Font(
    None,
    40
)


# ============================================================
# GAME LOOP
# ============================================================

running = True



# ============================================================
# GAMEPLAY FREEZE AFTER WIN
# ============================================================

def gameplay_locked():
    return game_won

while running:

    CLOCK.tick(FPS)

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:


            # =================================================
            # MAIN MENU CONTROLS
            # =================================================
            # =================================================
            # SETTINGS CONTROLS
            # =================================================

            if settings_open:

                if event.key in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    settings_selection = (
                        settings_selection - 1
                    ) % len(SETTINGS_ITEMS)

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s
                ):

                    settings_selection = (
                        settings_selection + 1
                    ) % len(SETTINGS_ITEMS)

                elif event.key in (
                    pygame.K_LEFT,
                    pygame.K_a,
                    pygame.K_RIGHT,
                    pygame.K_d
                ):

                    change = (
                        0.05
                        if event.key in (
                            pygame.K_RIGHT,
                            pygame.K_d
                        )
                        else -0.05
                    )

                    selected = SETTINGS_ITEMS[
                        settings_selection
                    ]

                    if selected == "MUSIC VOLUME":

                        music_volume = max(
                            0.0,
                            min(
                                1.0,
                                music_volume + change
                            )
                        )

                        if not music_muted:
                            pygame.mixer.music.set_volume(
                                music_volume
                            )

                    elif selected == "SOUND EFFECTS":

                        sfx_volume = max(
                            0.0,
                            min(
                                1.0,
                                sfx_volume + change
                            )
                        )

                        # Update known sound effects.
                        for sound_name in (
                            "shoot_sound",
                            "jump_sound",
                            "hurt_sound",
                            "coin_sound",
                            "powerup_sound"
                        ):

                            sound_obj = globals().get(
                                sound_name
                            )

                            if sound_obj is not None:
                                sound_obj.set_volume(
                                    sfx_volume
                                )

                elif event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):

                    selected = SETTINGS_ITEMS[
                        settings_selection
                    ]

                    if selected == "MUTE MUSIC":

                        music_muted = not music_muted

                        pygame.mixer.music.set_volume(
                            0.0
                            if music_muted
                            else music_volume
                        )

                    elif selected == "BACK":

                        settings_open = False
                        menu_open = True
                        game_paused = False

                elif event.key == pygame.K_ESCAPE:

                    settings_open = False
                    menu_open = True
                    game_paused = False

                continue



            if menu_open:

                if event.key in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    menu_selection = (
                        menu_selection - 1
                    ) % len(MENU_ITEMS)

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s
                ):

                    menu_selection = (
                        menu_selection + 1
                    ) % len(MENU_ITEMS)

                elif event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):

                    if MENU_ITEMS[menu_selection] == "PLAY":

                        menu_open = False
                        settings_open = False
                        show_help = False
                        help_from_game = False
                        game_paused = False

                    elif MENU_ITEMS[menu_selection] == "LEVEL SELECT":

                        menu_open = False
                        level_select_open = True
                        selected_level = 0
                        game_won = False
                        game_paused = False

                    elif MENU_ITEMS[menu_selection] == "HOW TO PLAY":

                        menu_open = False
                        show_help = True
                        help_from_game = False
                        game_paused = True

                    elif MENU_ITEMS[menu_selection] == "SETTINGS":

                        menu_open = False
                        settings_open = True
                        settings_selection = 0
                        game_paused = True

                    elif MENU_ITEMS[menu_selection] == "QUIT":

                        running = False

                continue


            # LEVEL SELECT CONTROLS

            if level_select_open:

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    selected_level = (
                        selected_level - 1
                    ) % TOTAL_LEVELS

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    selected_level = (
                        selected_level + 1
                    ) % TOTAL_LEVELS

                elif event.key in (pygame.K_UP, pygame.K_w):
                    selected_level = max(
                        0,
                        selected_level - 3
                    )

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected_level = min(
                        TOTAL_LEVELS - 1,
                        selected_level + 3
                    )

                elif event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):

                    if selected_level < unlocked_levels:

                        current_level = selected_level + 1

                        level_select_open = False
                        menu_open = False
                        game_paused = False
                        show_help = False
                        help_from_game = False

                        load_selected_level(
                            current_level
                        )

                elif event.key == pygame.K_ESCAPE:

                    level_select_open = False
                    menu_open = True
                    game_paused = False

                continue


            # NEXT LEVEL AFTER WIN

            if game_won:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                    pygame.K_n
                ):

                    if current_level < TOTAL_LEVELS:

                        load_selected_level(
                            current_level + 1
                        )

                        game_won = False
                        game_paused = False

                    else:

                        game_won = False
                        game_paused = False
                        level_select_open = True
                        selected_level = TOTAL_LEVELS - 1

                elif event.key == pygame.K_l:

                    game_won = False
                    game_paused = False
                    level_select_open = True
                    selected_level = current_level - 1

                continue


            # H = How To Play


            if event.key == pygame.K_h:


                if show_help:


                    show_help = False


                    help_from_game = False


                    game_paused = False
                    menu_open = False


                else:


                    show_help = True


                    help_from_game = True


            


            # ENTER / SPACE starts the game from the opening help screen


            elif (


                show_help


                and not help_from_game


                and event.key in (pygame.K_RETURN, pygame.K_SPACE)


            ):


                show_help = False


                game_paused = False



            # ESC closes mid-game help


            elif (


                event.key == pygame.K_ESCAPE


                and show_help


                and help_from_game


            ):


                show_help = False


                help_from_game = False


                game_paused = False

            if (
                event.key == pygame.K_p
                and health > 0
                and not game_won
                and player_effect == "normal"
            ):
                game_paused = not game_paused


            # =================================================
            # DASH
            # =================================================

            if event.key in (
                pygame.K_LSHIFT,
                pygame.K_RSHIFT
            ):

                current_time = pygame.time.get_ticks()

                if (
                    health > 0
                    and player_effect == "normal"
                    and not game_won
                    and current_time >= dash_cooldown_until
                ):

                    dash_direction = (
                        1
                        if facing_right
                        else -1
                    )

                    dash_until = (
                        current_time
                        + DASH_DURATION
                    )

                    dash_cooldown_until = (
                        current_time
                        + DASH_COOLDOWN
                    )


            # =================================================
            # JUMP
            # =================================================

            if event.key in (
                pygame.K_SPACE,
                pygame.K_UP,
                pygame.K_w
            ):

                if (
                    health > 0
                    and player_effect == "normal"
                    and not game_won
                ):

                    jump()


            # =================================================
            # ATTACK
            # =================================================

            if event.key == pygame.K_f:

                current_time = pygame.time.get_ticks()

                if (
                    current_time -
                    last_attack_time
                    >= ATTACK_COOLDOWN
                    and health > 0
                    and player_effect == "normal"
                    and not game_won
                ):

                    attacking = True

                    attack_start_time = current_time

                    last_attack_time = current_time

                    shoot_sound.play()


            # =================================================
            # CHARACTER 1
            # =================================================

            if event.key == pygame.K_1:

                character_number = 1

                character_name = characters[
                    character_number
                ]

                load_all_animations()

                enemy_name = enemy_characters[
                    character_number
                ]

                load_enemy()

                select_sound.play()


            # =================================================
            # CHARACTER 2
            # =================================================

            if event.key == pygame.K_2:

                character_number = 2

                character_name = characters[
                    character_number
                ]

                load_all_animations()

                enemy_name = enemy_characters[
                    character_number
                ]

                load_enemy()

                select_sound.play()


            # =================================================
            # CHARACTER 3
            # =================================================

            if event.key == pygame.K_3:

                character_number = 3

                character_name = characters[
                    character_number
                ]

                load_all_animations()

                enemy_name = enemy_characters[
                    character_number
                ]

                load_enemy()

                select_sound.play()


            # =================================================
            # CHARACTER 4
            # =================================================

            if event.key == pygame.K_4:

                character_number = 4

                character_name = characters[
                    character_number
                ]

                load_all_animations()

                enemy_name = enemy_characters[
                    character_number
                ]

                load_enemy()

                select_sound.play()


            # =================================================
            # RESTART / RESPAWN
            # =================================================

            if (
                event.key == pygame.K_r
                and health <= 0
            ):

                health = MAX_HEALTH

                game_won = False
                finish_message = ""
                finish_message_until = 0
                death_respawn_at = 0
                game_paused = False

                frozen_player_x = 0
                frozen_player_y = 0
                frozen_velocity_x = 0
                frozen_velocity_y = 0
                frozen_enemy_positions = []

                velocity_x = 0
                velocity_y = 0
                jumps_left = 2

                attacking = False

                # If a checkpoint was reached, use it.
                # Otherwise go back to the original spawn.
                if active_checkpoint >= 0:

                    player_x = respawn_x
                    player_y = respawn_y

                else:

                    player_x = 150
                    player_y = 400

                player.x = int(player_x)
                player.y = int(player_y)

                # Enemies respawn normally.
                for enemy_obj in enemies:
                    enemy_obj.reset()

                camera_x = max(
                    0,
                    min(
                        WORLD_WIDTH - WIDTH,
                        player.x - WIDTH // 2
                    )
                )

                # Fruits and power-ups stay collected after a checkpoint.
                # A full run can still be restarted by closing and
                # reopening the game.
                fruit_effects = []
                heal_popups = []

                shield_active = False
                shield_until = 0

                speed_boost_active = False
                speed_boost_until = 0
                player_speed = NORMAL_player_speed

                damage_boost_active = False
                damage_boost_until = 0
                ATTACK_DAMAGE = NORMAL_ATTACK_DAMAGE

                start_player_appearing()



    if not game_paused:

            # ========================================================
            # PLAYER MOVEMENT
            # ========================================================

            if (
                health > 0
                and player_effect == "normal"
            ):

                keys = pygame.key.get_pressed()

                current_time = pygame.time.get_ticks()

                # =================================================
                # DASH MOVEMENT
                # =================================================

                if current_time < dash_until:

                    velocity_x = (
                        dash_direction
                        * (
                            DASH_DISTANCE
                            / max(
                                1,
                                DASH_DURATION
                            )
                        )
                    )

                else:

                    velocity_x = 0


                if current_time >= player_knockback_until:

                        if (
                        keys[pygame.K_LEFT]
                        or keys[pygame.K_a]
                    ):

                            velocity_x = -player_speed

                            facing_right = False


                        if (
                        keys[pygame.K_RIGHT]
                        or keys[pygame.K_d]
                    ):

                            velocity_x = player_speed

                            facing_right = True


                player_x += velocity_x

                player.x = int(player_x)

            else:

                velocity_x = 0


            # ========================================================
            # WORLD BOUNDARIES
            # ========================================================

            if player.left < 0:

                player.left = 0
                player_x = player.x


            if player.right > WORLD_WIDTH:

                player.right = WORLD_WIDTH
                player_x = player.x


            # ========================================================
            # SAVE OLD POSITION
            # ========================================================

            old_player_bottom = player.bottom


            # ========================================================
            # GRAVITY
            # ========================================================

            if health > 0 and not game_won:

                velocity_y += GRAVITY

                if velocity_y > 15:

                    velocity_y = 15

                player_y += velocity_y

                player.y = int(player_y)


            # ========================================================
            # GROUND COLLISION
            # ========================================================

            on_ground = False


            if (
                velocity_y >= 0
                and player.bottom >= ground_y
            ):

                player.bottom = ground_y

                player_y = float(player.y)

                velocity_y = 0

                jumps_left = 2

                on_ground = True


            # ========================================================
            # PLATFORM COLLISION
            # ========================================================

            if velocity_y >= 0:

                for platform in platforms:

                    if (
                        old_player_bottom <= platform.top
                        and
                        player.bottom >= platform.top
                        and
                        player.right > platform.left
                        and
                        player.left < platform.right
                    ):

                        player.bottom = platform.top

                        player_y = float(player.y)

                        velocity_y = 0

                        jumps_left = 2

                        on_ground = True

                        break


            # ========================================================
            # ALL ENEMIES: AI, ATTACKS, PHYSICS, KNOCKBACK, RESPAWN
            # ========================================================

            current_time = pygame.time.get_ticks()

            for enemy_obj in enemies:

                # ----------------------------------------------------
                # RESPAWN
                # ----------------------------------------------------

                if enemy_obj.effect == "dead":

                    # Normal enemies respawn after a few seconds.
                    # Bosses are different: once defeated, they stay dead
                    # until the player starts/reloads the level.
                    if getattr(
                        enemy_obj,
                        "is_boss",
                        False
                    ):

                        continue

                    if (
                        enemy_obj.respawn_at > 0
                        and current_time >= enemy_obj.respawn_at
                    ):

                        enemy_obj.reset()

                    continue


                # ----------------------------------------------------
                # APPEARING
                # ----------------------------------------------------

                if enemy_obj.effect == "appearing":

                    elapsed = (
                        current_time -
                        enemy_obj.effect_timer
                    )

                    enemy_obj.effect_frame = (
                        elapsed // 100
                    )

                    if (
                        enemy_obj.effect_frame >=
                        len(appearing_frames)
                    ):

                        enemy_obj.effect = "normal"
                        enemy_obj.effect_frame = 0


                # ----------------------------------------------------
                # AI + COMBAT
                # ----------------------------------------------------

                if (
                    enemy_obj.effect == "normal"
                    and health > 0
                ):

                    distance = abs(
                        enemy_obj.rect.centerx -
                        player.centerx
                    )

                    enemy_obj.can_see_player = (
                        distance <= ENEMY_DETECTION_RANGE
                    )


                    # ----------------------------------------------
                    # PLAYER DETECTED
                    # ----------------------------------------------

                    if enemy_obj.can_see_player:

                        if (
                            current_time >=
                            enemy_obj.knockback_until
                        ):

                            enemy_obj.ai_state = "chase"


                    # ----------------------------------------------
                    # CHASE
                    # ----------------------------------------------

                    if enemy_obj.ai_state == "chase":

                        if enemy_obj.can_see_player:

                            if (
                                current_time >=
                                enemy_obj.knockback_until
                            ):

                                if not enemy_obj.rect.colliderect(
                                    player
                                ):

                                    if (
                                        enemy_obj.rect.centerx <
                                        player.centerx
                                    ):

                                        enemy_obj.rect.x += (
                                            ENEMY_SPEED
                                        )

                                        enemy_obj.patrol_direction = 1

                                    elif (
                                        enemy_obj.rect.centerx >
                                        player.centerx
                                    ):

                                        enemy_obj.rect.x -= (
                                            ENEMY_SPEED
                                        )

                                        enemy_obj.patrol_direction = -1

                                else:

                                    if (
                                        not enemy_obj.is_attacking
                                        and
                                        current_time -
                                        enemy_obj.last_attack >=
                                        ENEMY_ATTACK_COOLDOWN
                                    ):

                                        enemy_obj.is_attacking = True
                                        enemy_obj.attack_start = (
                                            current_time
                                        )
                                        enemy_obj.attack_has_hit = False
                                        enemy_obj.last_attack = (
                                            current_time
                                        )

                        else:

                            # Lost player = STOP exactly here.
                            enemy_obj.ai_state = "idle"


                    # ----------------------------------------------
                    # IDLE AFTER LOSING PLAYER
                    # ----------------------------------------------

                    if enemy_obj.ai_state == "idle":

                        # Absolutely no horizontal movement.
                        pass


                    # ----------------------------------------------
                    # NORMAL PATROL
                    # ----------------------------------------------

                    if (
                        enemy_obj.ai_state == "patrol"
                        and
                        not enemy_obj.can_see_player
                    ):

                        if enemy_obj.patrol_direction > 0:

                            enemy_obj.rect.x += (
                                ENEMY_PATROL_SPEED
                            )

                            if (
                                enemy_obj.rect.x >=
                                enemy_obj.patrol_right
                            ):

                                enemy_obj.rect.x = (
                                    enemy_obj.patrol_right
                                )

                                enemy_obj.patrol_direction = -1

                        else:

                            enemy_obj.rect.x -= (
                                ENEMY_PATROL_SPEED
                            )

                            if (
                                enemy_obj.rect.x <=
                                enemy_obj.patrol_left
                            ):

                                enemy_obj.rect.x = (
                                    enemy_obj.patrol_left
                                )

                                enemy_obj.patrol_direction = 1


                    # ----------------------------------------------
                    # ENEMY ATTACK
                    # ----------------------------------------------

                    if enemy_obj.is_attacking:

                        attack_elapsed = (
                            current_time -
                            enemy_obj.attack_start
                        )

                        if (
                            attack_elapsed >= 150
                            and
                            not enemy_obj.attack_has_hit
                        ):

                            enemy_obj.attack_has_hit = True

                            if (
                                enemy_obj.rect.colliderect(player)
                                and
                                player_effect == "normal"
                                and
                                current_time >=
                                last_damage_time +
                                INVINCIBLE_TIME
                            ):

                                if not shield_active:

                                    health -= ENEMY_DAMAGE

                                if (
                                    player.centerx <
                                    enemy_obj.rect.centerx
                                ):

                                    velocity_x = (
                                        -PLAYER_KNOCKBACK_X
                                    )

                                else:

                                    velocity_x = (
                                        PLAYER_KNOCKBACK_X
                                    )

                                velocity_y = PLAYER_KNOCKBACK_Y

                                player_knockback_until = (
                                    current_time +
                                    PLAYER_KNOCKBACK_TIME
                                )

                                last_damage_time = current_time

                                hit_sound.play()

                        if (
                            attack_elapsed >=
                            ENEMY_ATTACK_ANIMATION_TIME
                        ):

                            enemy_obj.is_attacking = False
                            enemy_obj.attack_has_hit = False


                # ----------------------------------------------------
                # ENEMY KNOCKBACK
                # ----------------------------------------------------

                if (
                    enemy_obj.effect == "normal"
                    and
                    current_time <
                    enemy_obj.knockback_until
                ):

                    enemy_obj.rect.x += (
                        enemy_obj.knockback_velocity_x
                    )


                # ----------------------------------------------------
                # ENEMY GRAVITY / PLATFORMS
                # ----------------------------------------------------

                if enemy_obj.effect == "normal":

                    enemy_obj.velocity_y += GRAVITY

                    if enemy_obj.velocity_y > 15:

                        enemy_obj.velocity_y = 15

                    old_enemy_bottom = (
                        enemy_obj.rect.bottom
                    )

                    enemy_obj.rect.y += int(
                        enemy_obj.velocity_y
                    )

                    enemy_landed = False

                    if (
                        enemy_obj.velocity_y >= 0
                        and
                        enemy_obj.rect.bottom >= ground_y
                    ):

                        enemy_obj.rect.bottom = ground_y
                        enemy_obj.velocity_y = 0
                        enemy_landed = True


                    if enemy_obj.velocity_y >= 0:

                        for platform in platforms:

                            if (
                                old_enemy_bottom <=
                                platform.top
                                and
                                enemy_obj.rect.bottom >=
                                platform.top
                                and
                                enemy_obj.rect.right >
                                platform.left
                                and
                                enemy_obj.rect.left <
                                platform.right
                            ):

                                enemy_obj.rect.bottom = (
                                    platform.top
                                )

                                enemy_obj.velocity_y = 0
                                enemy_landed = True

                                break


                    if enemy_landed:

                        enemy_obj.jumps_left = (
                            ENEMY_MAX_JUMPS
                        )

                        enemy_obj.jumps_used = 0


                    # ----------------------------------------------
                    # DOUBLE JUMP WHILE CHASING
                    # ----------------------------------------------

                    if enemy_obj.can_see_player:

                        player_is_higher = (
                            player.y + 20 <
                            enemy_obj.rect.y
                        )

                        player_is_near = (
                            abs(
                                player.centerx -
                                enemy_obj.rect.centerx
                            ) <= 250
                        )

                        if (
                            player_is_higher
                            and player_is_near
                            and enemy_obj.jumps_left > 0
                            and
                            current_time -
                            enemy_obj.last_jump >=
                            ENEMY_JUMP_COOLDOWN
                        ):

                            if (
                                enemy_obj.jumps_used == 0
                                and
                                enemy_obj.velocity_y == 0
                            ):

                                enemy_obj.velocity_y = JUMP_POWER
                                enemy_obj.jumps_left -= 1
                                enemy_obj.jumps_used = 1
                                enemy_obj.last_jump = current_time

                            elif (
                                enemy_obj.jumps_used == 1
                                and
                                enemy_obj.velocity_y != 0
                            ):

                                enemy_obj.velocity_y = JUMP_POWER
                                enemy_obj.jumps_left -= 1
                                enemy_obj.jumps_used = 2
                                enemy_obj.last_jump = current_time


                # ----------------------------------------------------
                # PLAYER ATTACK -> ENEMY HIT
                # ----------------------------------------------------

                if (
                    attacking
                    and
                    enemy_obj.effect == "normal"
                ):

                    if facing_right:

                        attack_rect = pygame.Rect(
                            player.right,
                            player.y + 10,
                            70,
                            45
                        )

                    else:

                        attack_rect = pygame.Rect(
                            player.left - 70,
                            player.y + 10,
                            70,
                            45
                        )


                    if attack_rect.colliderect(
                        enemy_obj.rect
                    ):

                        enemy_obj.health -= ATTACK_DAMAGE

                        attacking = False

                        if (
                            enemy_obj.rect.centerx <
                            player.centerx
                        ):

                            enemy_obj.knockback_velocity_x = (
                                -ENEMY_KNOCKBACK_X
                            )

                        else:

                            enemy_obj.knockback_velocity_x = (
                                ENEMY_KNOCKBACK_X
                            )

                        enemy_obj.knockback_velocity_y = (
                            ENEMY_KNOCKBACK_Y
                        )

                        enemy_obj.velocity_y = (
                            enemy_obj.knockback_velocity_y
                        )

                        enemy_obj.knockback_until = (
                            current_time +
                            ENEMY_KNOCKBACK_TIME
                        )

                        # Small particles, not a white box.
                        enemy_obj.hit_particles.clear()

                        for _ in range(8):

                            enemy_obj.hit_particles.append({
                                "x": enemy_obj.rect.centerx,
                                "y": enemy_obj.rect.centery,
                                "vx": (
                                    pygame.time.get_ticks() % 5
                                ) - 2,
                                "vy": -(
                                    pygame.time.get_ticks() % 4
                                    + 2
                                ),
                                "size": 3,
                                "color": (255, 220, 60)
                            })

                        hit_sound.play()


                # ----------------------------------------------------
                # ENEMY DEATH -> RESPAWN LATER
                # ----------------------------------------------------

                if (
                    enemy_obj.health <= 0
                    and
                    enemy_obj.effect == "normal"
                ):

                    enemy_obj.effect = "disappearing"
                    enemy_obj.effect_frame = 0
                    enemy_obj.effect_timer = current_time

                    if getattr(
                        enemy_obj,
                        "is_boss",
                        False
                    ):

                        enemy_obj.respawn_at = -1

                    else:

                        enemy_obj.respawn_at = (
                            current_time + 3000
                        )

                    enemy_obj.is_attacking = False

                    explosion_sound.play()


                # ----------------------------------------------------
                # DISAPPEARING ANIMATION
                # ----------------------------------------------------

                if enemy_obj.effect == "disappearing":

                    elapsed = (
                        current_time -
                        enemy_obj.effect_timer
                    )

                    enemy_obj.effect_frame = (
                        elapsed // 100
                    )

                    if (
                        enemy_obj.effect_frame >=
                        len(disappearing_frames)
                    ):

                        enemy_obj.effect = "dead"

                        enemy_obj.rect.x = -10000
                        enemy_obj.rect.y = -10000

                        enemy_obj.health = 0


                # ----------------------------------------------------
                # HIT PARTICLES
                # ----------------------------------------------------

                for particle in enemy_obj.hit_particles[:]:

                    particle["x"] += particle["vx"]
                    particle["y"] += particle["vy"]

                    particle["vy"] += 0.25

                    particle["size"] -= 0.08

                    if particle["size"] <= 0:

                        enemy_obj.hit_particles.remove(
                            particle
                        )

            # ========================================================
            # ATTACK TIMER
            # ========================================================

            current_time = pygame.time.get_ticks()


            if attacking:

                if (
                    current_time -
                    attack_start_time
                    >= ATTACK_TIME
                ):

                    attacking = False


            # ========================================================
            # PLAYER DEATH
            # ========================================================

            if (
                health <= 0
                and player_effect == "normal"
            ):

                health = 0

                attacking = False

                player_effect = "disappearing"

                player_effect_frame = 0

                player_effect_timer = pygame.time.get_ticks()

                explosion_sound.play()


            # ========================================================
            # PLAYER EFFECT UPDATE
            # ========================================================

            if player_effect == "appearing":

                elapsed = (
                    pygame.time.get_ticks()
                    - player_effect_timer
                )

                player_effect_frame = elapsed // 100

                if (
                    player_effect_frame
                    >= len(appearing_frames)
                ):

                    player_effect = "normal"

                    player_effect_frame = 0


            elif player_effect == "disappearing":

                elapsed = (
                    pygame.time.get_ticks()
                    - player_effect_timer
                )

                player_effect_frame = elapsed // 100

                if (
                    player_effect_frame
                    >= len(disappearing_frames)
                ):

                    player_effect_frame = (
                        len(disappearing_frames) - 1
                    )


            # ========================================================
            # FRUIT COLLECTION + DIFFERENT HEALING
            # ========================================================

            if (
                health > 0
                and player_effect == "normal"
            ):

                for fruit in fruits[:]:

                    if player.colliderect(
                        fruit["rect"]
                    ):

                        # =================================================
                        # SCORE
                        # =================================================

                        score += fruit["points"]


                        # =================================================
                        # HEAL PLAYER
                        # =================================================

                        heal_amount = fruit["heal"]

                        health += heal_amount


                        # =================================================
                        # NEVER GO ABOVE 100
                        # =================================================

                        if health > MAX_HEALTH:

                            health = MAX_HEALTH


                        # =================================================
                        # PLAY COIN SOUND
                        # =================================================

                        coin_sound.play()


                        # =================================================
                        # HEAL POPUP
                        # =================================================

                        heal_popups.append({

                            "x": player.centerx,

                            "y": player.y,

                            "text": f"+{heal_amount} HP!",

                            "timer": pygame.time.get_ticks()

                        })


                        # =================================================
                        # FRUIT DISAPPEARING EFFECT
                        # =================================================

                        fruit_effects.append({

                            "x": fruit["rect"].x,

                            "y": fruit["rect"].y,

                            "frame": 0,

                            "timer": pygame.time.get_ticks()

                        })


                        # =================================================
                        # REMOVE FRUIT
                        # =================================================

                        fruits.remove(fruit)


            # ========================================================
            # DAMAGE BOOST COLLECTION
            # ========================================================

            current_time = pygame.time.get_ticks()

            if (
                health > 0
                and player_effect == "normal"
            ):

                for boost in damage_boosts:

                    if (
                        not boost["collected"]
                        and player.colliderect(
                            boost["rect"]
                        )
                    ):

                        boost["collected"] = True

                        damage_boost_active = True

                        damage_boost_until = (
                            current_time +
                            DAMAGE_BOOST_DURATION
                        )

                        ATTACK_DAMAGE = (
                            NORMAL_ATTACK_DAMAGE *
                            DAMAGE_BOOST_MULTIPLIER
                        )

                        powerup_sound.play()


            # ========================================================
            # SPEED BOOST COLLECTION
            # ========================================================

            current_time = pygame.time.get_ticks()

            if (
                health > 0
                and player_effect == "normal"
            ):

                for boost in speed_boosts:

                    if (
                        not boost["collected"]
                        and player.colliderect(
                            boost["rect"]
                        )
                    ):

                        boost["collected"] = True

                        speed_boost_active = True

                        speed_boost_until = (
                            current_time +
                            SPEED_BOOST_DURATION
                        )

                        player_speed = (
                            NORMAL_player_speed *
                            SPEED_BOOST_MULTIPLIER
                        )

                        powerup_sound.play()


            # ========================================================
            # SHIELD POWER-UP COLLECTION
            # ========================================================

            current_time = pygame.time.get_ticks()

            if (
                health > 0
                and player_effect == "normal"
            ):

                for shield in shields:

                    if (
                        not shield["collected"]
                        and player.colliderect(
                            shield["rect"]
                        )
                    ):

                        shield["collected"] = True

                        shield_active = True

                        shield_until = (
                            current_time +
                            SHIELD_DURATION
                        )

                        powerup_sound.play()


            # ========================================================
            # COIN COLLECTION
            # ========================================================

            if (
                health > 0
                and player_effect == "normal"
            ):

                for coin in coins:

                    if (
                        not coin["collected"]
                        and player.colliderect(
                            coin["rect"]
                        )
                    ):

                        coin["collected"] = True

                        current_time = pygame.time.get_ticks()

                        if current_time <= coin_combo_until:
                            coin_combo += 1
                        else:
                            coin_combo = 1

                        coin_combo_until = (
                            current_time
                            + COIN_COMBO_TIME
                        )

                        combo_bonus = (
                            min(
                                coin_combo,
                                10
                            )
                            * 5
                        )

                        score += (
                            10
                            + combo_bonus
                        )

                        coin_sound.play()


            # ========================================================
            # HEAL POPUP UPDATE
            # ========================================================

            for popup in heal_popups[:]:

                elapsed = (
                    pygame.time.get_ticks()
                    - popup["timer"]
                )

                popup["y"] -= 1

                if elapsed >= 1000:

                    heal_popups.remove(popup)


            # ========================================================
            # FRUIT EFFECT UPDATE
            # ========================================================

            for effect in fruit_effects[:]:

                elapsed = (
                    pygame.time.get_ticks()
                    - effect["timer"]
                )

                effect["frame"] = elapsed // 100

                if (
                    effect["frame"]
                    >= len(disappearing_frames)
                ):

                    fruit_effects.remove(effect)


            # ========================================================
            # DAMAGE BOOST TIMER
            # ========================================================

            if (
                damage_boost_active
                and
                pygame.time.get_ticks() >= damage_boost_until
            ):

                damage_boost_active = False
                ATTACK_DAMAGE = NORMAL_ATTACK_DAMAGE


            # ========================================================
            # SPEED BOOST TIMER
            # ========================================================

            if (
                speed_boost_active
                and
                pygame.time.get_ticks() >= speed_boost_until
            ):

                speed_boost_active = False
                player_speed = NORMAL_player_speed


            # ========================================================
            # SHIELD TIMER
            # ========================================================

            if (
                shield_active
                and
                pygame.time.get_ticks() >= shield_until
            ):

                shield_active = False


            # ========================================================
            # CHECKPOINT COLLECTION
            # ========================================================

            if (
                health > 0
                and player_effect == "normal"
                and not game_won
            ):

                for checkpoint_index, checkpoint in enumerate(
                    checkpoints
                ):

                    if player.colliderect(
                        checkpoint["rect"]
                    ):

                        if not checkpoint["activated"]:

                            checkpoint["activated"] = True

                            active_checkpoint = (
                                checkpoint_index
                            )

                            respawn_x = (
                                checkpoint["rect"].centerx
                                - player.width // 2
                            )

                            respawn_y = (
                                checkpoint["rect"].bottom
                                - player.height
                            )

                            finish_message = "CHECKPOINT!"

                            finish_message_until = (
                                pygame.time.get_ticks()
                                + 1500
                            )

            # ========================================================
            # FINISH / WIN CHECK
            # ========================================================

            if (
                not game_won
                and player.colliderect(FINISH_RECT)
            ):

                if all_fruits_collected():

                    game_won = True
                    game_paused = True
                    finish_message = "YOU WIN!"
                    finish_message_until = (
                        pygame.time.get_ticks() + 999999999
                    )

                    # Victory freezes gameplay through game_won.
                    # It does NOT activate the normal pause screen.
                    game_paused = False
                    health = MAX_HEALTH
                    attacking = False

                else:

                    remaining = len(fruits)

                    if remaining == 1:
                        finish_message = "Collect the last fruit!"
                    else:
                        finish_message = (
                            f"Collect all fruits! "
                            f"{remaining} left."
                        )

                    finish_message_until = (
                        pygame.time.get_ticks() + 2000
                    )


            # ========================================================
            # FREEZE EVERYTHING AFTER VICTORY
            # ========================================================

            if game_won:

                player.x = frozen_player_x
                player.y = frozen_player_y

                player_x = frozen_player_x
                player_y = frozen_player_y

                velocity_x = 0
                velocity_y = 0

                health = MAX_HEALTH
                attacking = False

                for index, enemy_obj in enumerate(enemies):

                    if index < len(frozen_enemy_positions):

                        enemy_obj.rect.x = (
                            frozen_enemy_positions[index][0]
                        )

                        enemy_obj.rect.y = (
                            frozen_enemy_positions[index][1]
                        )

                    enemy_obj.velocity_y = 0
                    enemy_obj.knockback_velocity_x = 0
                    enemy_obj.knockback_velocity_y = 0
                    enemy_obj.is_attacking = False


    if menu_open:

        velocity_x = 0
        velocity_y = 0


    # ========================================================
    # LARGE BOSS HEALTH BAR
    # ========================================================

    if (
        not menu_open
        and not level_select_open
        and not show_help
        and not game_won
    ):

        active_boss = next(
            (
                e for e in enemies
                if getattr(e, "is_boss", False)
                and e.effect != "dead"
                and getattr(e, "health", 0) > 0
            ),
            None
        )

        if active_boss is not None:

            boss_bar_width = min(
                650,
                WIDTH - 120
            )

            boss_bar_height = 28

            boss_bar_x = (
                WIDTH // 2
                - boss_bar_width // 2
            )

            boss_bar_y = 72

            # Boss name.
            boss_font = pygame.font.Font(
                None,
                32
            )

            boss_title = (
                "FINAL BOSS"
                if active_boss.boss_type == "final"
                else "MID BOSS"
            )

            title_surface = boss_font.render(
                boss_title,
                True,
                (255, 220, 70)
            )

            SCREEN.blit(
                title_surface,
                title_surface.get_rect(
                    center=(
                        WIDTH // 2,
                        boss_bar_y - 22
                    )
                )
            )

            # Outer/background bar.
            pygame.draw.rect(
                SCREEN,
                (25, 25, 25),
                (
                    boss_bar_x - 4,
                    boss_bar_y - 4,
                    boss_bar_width + 8,
                    boss_bar_height + 8
                )
            )

            pygame.draw.rect(
                SCREEN,
                (80, 20, 20),
                (
                    boss_bar_x,
                    boss_bar_y,
                    boss_bar_width,
                    boss_bar_height
                )
            )

            boss_ratio = max(
                0.0,
                min(
                    1.0,
                    active_boss.health
                    / max(
                        1,
                        active_boss.max_health
                    )
                )
            )

            pygame.draw.rect(
                SCREEN,
                (235, 55, 55),
                (
                    boss_bar_x,
                    boss_bar_y,
                    int(
                        boss_bar_width
                        * boss_ratio
                    ),
                    boss_bar_height
                )
            )

            # HP text.
            hp_font = pygame.font.Font(
                None,
                22
            )

            hp_text = hp_font.render(
                (
                    f"{max(0, active_boss.health)}"
                    f" / "
                    f"{active_boss.max_health}"
                ),
                True,
                (255, 255, 255)
            )

            SCREEN.blit(
                hp_text,
                hp_text.get_rect(
                    center=(
                        WIDTH // 2,
                        boss_bar_y
                        + boss_bar_height // 2
                    )
                )
            )


    # ========================================================
    # BOSS HUD
    # ========================================================

    if not menu_open and not level_select_open and not show_help:

        active_boss = next(
            (
                e for e in enemies
                if getattr(e, "is_boss", False)
                and e.effect != "dead"
            ),
            None
        )

        if active_boss is not None:

            boss_font = pygame.font.Font(None, 24)

            boss_text = boss_font.render(
                (
                    "FINAL BOSS!"
                    if active_boss.boss_type == "final"
                    else "MID BOSS!"
                ),
                True,
                (255, 220, 70)
            )

            SCREEN.blit(
                boss_text,
                (20, 52)
            )


    # ========================================================
    # CURRENT LEVEL HUD
    # ========================================================

    if not menu_open and not level_select_open and not show_help:

        level_hud_font = pygame.font.Font(
            None,
            26
        )

        level_hud = level_hud_font.render(
            f"LEVEL {current_level}",
            True,
            (255, 255, 255)
        )

        SCREEN.blit(
            level_hud,
            (20, 20)
        )


    # ========================================================
    # CAMERA
    # ========================================================

    camera_x = (
        player.x -
        WIDTH // 2
    )


    if camera_x < 0:

        camera_x = 0


    if camera_x > WORLD_WIDTH - WIDTH:

        camera_x = (
            WORLD_WIDTH -
            WIDTH
        )


    # ========================================================
    # PLAYER ANIMATION
    # ========================================================

    if player_effect == "normal":

        if not on_ground:

            if jumps_left == 0:

                current_frames = (
                    double_jump_frames
                )

            elif velocity_y < 0:

                current_frames = (
                    jump_frames
                )

            else:

                current_frames = (
                    fall_frames
                )

        elif velocity_x != 0:

            current_frames = run_frames

        else:

            current_frames = idle_frames


        frame_number = (
            pygame.time.get_ticks() // 120
        ) % len(current_frames)

        frame = current_frames[
            frame_number
        ]


        if not facing_right:

            frame = pygame.transform.flip(
                frame,
                True,
                False
            )


    # ========================================================
    # BACKGROUND
    # ========================================================

    # Draw the selected level background as a repeating asset.
    background_tile_size = current_background.get_size()

    bg_x_start = -(
        camera_x
        % background_tile_size[0]
    )

    bg_y_start = 0

    for bg_x in range(
        bg_x_start,
        WIDTH,
        background_tile_size[0]
    ):

        for bg_y in range(
            bg_y_start,
            HEIGHT,
            background_tile_size[1]
        ):

            SCREEN.blit(
                current_background,
                (bg_x, bg_y)
            )


    # ========================================================
    # DRAW FLOOR
    # ========================================================

    for x in range(
        0,
        WORLD_WIDTH,
        TILE_DISPLAY
    ):

        SCREEN.blit(
            grass_middle,
            (
                x - camera_x,
                ground_y
            )
        )


    # ========================================================
    # DRAW PLATFORMS
    # ========================================================

    for platform in platforms:

        block_count = (
            platform.width //
            TILE_DISPLAY
        )


        for i in range(block_count):

            block_x = (
                platform.x
                + i * TILE_DISPLAY
                - camera_x
            )


            if i == 0:

                block = grass_left

            elif i == block_count - 1:

                block = grass_right

            else:

                block = grass_middle


            SCREEN.blit(
                block,
                (
                    block_x,
                    platform.y
                ),
                pygame.Rect(
                    0,
                    0,
                    TILE_DISPLAY,
                    28
                )
            )


    # ========================================================
    # DRAW DAMAGE BOOSTS
    # ========================================================

    for boost in damage_boosts:

        if not boost["collected"]:

            draw_damage_boost(
                SCREEN,
                boost["rect"],
                camera_x
            )


    # ========================================================
    # DRAW CHECKPOINTS
    # ========================================================

    for checkpoint in checkpoints:

        draw_checkpoint(
            SCREEN,
            checkpoint,
            camera_x
        )


    # ========================================================
    # DRAW YOUR REAL FINISH CHECKPOINT
    # ========================================================

    if game_won and finish_pressed_image is not None:
        finish_image = finish_pressed_image
    else:
        finish_image = finish_idle_image

    SCREEN.blit(
        finish_image,
        (
            FINISH_X - camera_x,
            ground_y - FINISH_SIZE
        )
    )


    # ========================================================
    # DRAW SPEED BOOSTS
    # ========================================================

    for boost in speed_boosts:

        if not boost["collected"]:

            draw_speed_boost(
                SCREEN,
                boost["rect"],
                camera_x
            )


    # ========================================================
    # DRAW SHIELD POWER-UPS
    # ========================================================

    for shield in shields:

        if not shield["collected"]:

            draw_shield(
                SCREEN,
                shield["rect"],
                camera_x
            )


    # ========================================================
    # DRAW COINS
    # ========================================================

    coin_frame_number = (
        pygame.time.get_ticks() // 100
    )

    for coin in coins:

        if coin["collected"]:
            continue

        if coin_frames:

            coin_frame = coin_frames[
                coin_frame_number %
                len(coin_frames)
            ]

            SCREEN.blit(
                coin_frame,
                (
                    coin["rect"].x -
                    camera_x,
                    coin["rect"].y
                )
            )

        else:

            draw_coin(
                SCREEN,
                coin["rect"],
                camera_x
            )


    # ========================================================
    # DRAW FRUITS
    # ========================================================

    fruit_frame_number = (
        pygame.time.get_ticks() // 150
    )


    for fruit in fruits:

        frames = fruit["frames"]

        fruit_frame = frames[
            fruit_frame_number %
            len(frames)
        ]


        SCREEN.blit(
            fruit_frame,
            (
                fruit["rect"].x -
                camera_x,

                fruit["rect"].y
            )
        )


    # ========================================================
    # DRAW FRUIT DISAPPEARING EFFECT
    # ========================================================

    for effect in fruit_effects:

        effect_frame = disappearing_frames[
            min(
                effect["frame"],
                len(disappearing_frames) - 1
            )
        ]


        SCREEN.blit(
            effect_frame,
            (
                effect["x"] -
                camera_x - 24,

                effect["y"] - 24
            )
        )


    # ========================================================
    # DRAW ALL ENEMIES
    # ========================================================

    current_time = pygame.time.get_ticks()

    for enemy_obj in enemies:

        if enemy_obj.effect == "normal":

            # Idle after losing sight.
            if enemy_obj.ai_state == "idle":

                frames = enemy_idle_frames

                frame_number = (
                    current_time // 180
                ) % len(frames)

            elif enemy_obj.is_attacking:

                frames = enemy_attack_frames

                frame_number = (
                    current_time // 100
                ) % len(frames)

            else:

                frames = enemy_frames

                frame_number = (
                    current_time // 100
                ) % len(frames)


            enemy_frame = frames[
                frame_number
            ]

            # Bosses must be VISUALLY bigger, not just have a bigger
            # collision box. Normal enemies use their original sprite size.
            if getattr(
                enemy_obj,
                "is_boss",
                False
            ):

                boss_scale = (
                    2.0
                    if enemy_obj.boss_type == "final"
                    else 1.5
                )

                boss_width = int(
                    enemy_frame.get_width()
                    * boss_scale
                )

                boss_height = int(
                    enemy_frame.get_height()
                    * boss_scale
                )

                enemy_frame = pygame.transform.scale(
                    enemy_frame,
                    (
                        boss_width,
                        boss_height
                    )
                )


            # Face player while chasing, otherwise face patrol.
            if enemy_obj.ai_state == "chase":

                if (
                    enemy_obj.rect.centerx >
                    player.centerx
                ):

                    enemy_frame = pygame.transform.flip(
                        enemy_frame,
                        True,
                        False
                    )

            elif (
                enemy_obj.patrol_direction < 0
            ):

                enemy_frame = pygame.transform.flip(
                    enemy_frame,
                    True,
                    False
                )


            if getattr(
                enemy_obj,
                "is_boss",
                False
            ):

                draw_x = (
                    enemy_obj.rect.centerx
                    - camera_x
                    - enemy_frame.get_width() // 2
                )

                draw_y = (
                    enemy_obj.rect.centery
                    - enemy_frame.get_height() // 2
                )

            else:

                draw_x = (
                    enemy_obj.rect.x
                    - camera_x
                )

                draw_y = enemy_obj.rect.y

            SCREEN.blit(
                enemy_frame,
                (
                    draw_x,
                    draw_y
                )
            )

            # Boss name and health bar.
            if (
                getattr(enemy_obj, "is_boss", False)
                and enemy_obj.effect != "dead"
            ):

                boss_name = (
                    "FINAL BOSS"
                    if enemy_obj.boss_type == "final"
                    else "MID BOSS"
                )

                boss_font = pygame.font.Font(None, 26)

                name_surface = boss_font.render(
                    boss_name,
                    True,
                    (255, 255, 255)
                )

                name_rect = name_surface.get_rect(
                    center=(
                        enemy_obj.rect.centerx - camera_x,
                        enemy_obj.rect.top - 32
                    )
                )

                SCREEN.blit(
                    name_surface,
                    name_rect
                )

                bar_width = (
                    170
                    if enemy_obj.boss_type == "final"
                    else 140
                )

                bar_height = 18

                bar_x = (
                    enemy_obj.rect.centerx
                    - camera_x
                    - bar_width // 2
                )

                bar_y = enemy_obj.rect.top - 16

                pygame.draw.rect(
                    SCREEN,
                    (50, 20, 20),
                    (
                        bar_x,
                        bar_y,
                        bar_width,
                        bar_height
                    )
                )

                ratio = max(
                    0,
                    enemy_obj.health
                ) / max(
                    1,
                    enemy_obj.max_health
                )

                pygame.draw.rect(
                    SCREEN,
                    (230, 70, 70),
                    (
                        bar_x,
                        bar_y,
                        int(bar_width * ratio),
                        bar_height
                    )
                )



            # Small particles.
            for particle in enemy_obj.hit_particles:

                pygame.draw.circle(
                    SCREEN,
                    particle["color"],
                    (
                        int(
                            particle["x"] -
                            camera_x
                        ),
                        int(particle["y"])
                    ),
                    max(
                        1,
                        int(particle["size"])
                    )
                )


        elif enemy_obj.effect == "appearing":

            SCREEN.blit(
                appearing_frames[
                    min(
                        enemy_obj.effect_frame,
                        len(appearing_frames) - 1
                    )
                ],
                (
                    enemy_obj.rect.x -
                    camera_x - 16,
                    enemy_obj.rect.y - 16
                )
            )


        elif enemy_obj.effect == "disappearing":

            SCREEN.blit(
                disappearing_frames[
                    min(
                        enemy_obj.effect_frame,
                        len(disappearing_frames) - 1
                    )
                ],
                (
                    enemy_obj.rect.x -
                    camera_x - 16,
                    enemy_obj.rect.y - 16
                )
            )


        # Enemy health bar.
        if (
            enemy_obj.effect == "normal"
        ):

            enemy_bar_x = (
                enemy_obj.rect.x -
                camera_x
            )

            enemy_bar_y = (
                enemy_obj.rect.y - 15
            )

            BAR_WIDTH = 64
            BAR_HEIGHT = 8

            pygame.draw.rect(
                SCREEN,
                (0, 0, 0),
                (
                    enemy_bar_x,
                    enemy_bar_y,
                    BAR_WIDTH,
                    BAR_HEIGHT
                )
            )

            enemy_health_width = (
                BAR_WIDTH *
                max(0, enemy_obj.health) /
                MAX_ENEMY_HEALTH
            )

            pygame.draw.rect(
                SCREEN,
                (220, 0, 0),
                (
                    enemy_bar_x,
                    enemy_bar_y,
                    enemy_health_width,
                    BAR_HEIGHT
                )
            )


    # ========================================================
    # DRAW PLAYER
    # ========================================================

    player_screen_x = (
        player.x -
        camera_x
    )


    if player_effect == "normal":

        SCREEN.blit(
            frame,
            (
                player_screen_x - 7,
                player.y
            )
        )


    elif player_effect == "appearing":

        SCREEN.blit(
            appearing_frames[
                min(
                    player_effect_frame,
                    len(appearing_frames) - 1
                )
            ],
            (
                player_screen_x - 16,
                player.y - 16
            )
        )


    elif player_effect == "disappearing":

        SCREEN.blit(
            disappearing_frames[
                min(
                    player_effect_frame,
                    len(disappearing_frames) - 1
                )
            ],
            (
                player_screen_x - 16,
                player.y - 16
            )
        )


    # ========================================================
    # DRAW ACTIVE SHIELD
    # ========================================================

    if shield_active:

        shield_center = (
            int(player.centerx - camera_x),
            int(player.centery)
        )

        pygame.draw.circle(
            SCREEN,
            (80, 180, 255),
            shield_center,
            42,
            4
        )


    # ========================================================
    # DRAW HEAL POPUPS
    # ========================================================

    heal_font = pygame.font.Font(
        None,
        28
    )


    for popup in heal_popups:

        heal_text = heal_font.render(
            popup["text"],
            True,
            (0, 255, 0)
        )


        SCREEN.blit(
            heal_text,
            (
                popup["x"] -
                camera_x,

                popup["y"]
            )
        )


    # ========================================================
    # PLAYER HEALTH BAR
    # ========================================================

    if health > 0 and not game_won:

        player_bar_width = 70
        player_bar_height = 8

        player_bar_x = (
            player_screen_x - 10
        )

        player_bar_y = (
            player.y - 15
        )


        pygame.draw.rect(
            SCREEN,
            (0, 0, 0),
            (
                player_bar_x,
                player_bar_y,
                player_bar_width,
                player_bar_height
            )
        )


        player_health_width = (
            player_bar_width *
            max(0, health) /
            MAX_HEALTH
        )


        pygame.draw.rect(
            SCREEN,
            (0, 200, 0),
            (
                player_bar_x,
                player_bar_y,
                player_health_width,
                player_bar_height
            )
        )


    # ========================================================
    # DASH AND COMBO HUD
    # ========================================================

    if not menu_open and not level_select_open and not show_help:

        if pygame.time.get_ticks() < dash_cooldown_until:

            dash_font = pygame.font.Font(
                None,
                24
            )

            remaining = max(
                0,
                dash_cooldown_until
                - pygame.time.get_ticks()
            )

            dash_text = dash_font.render(
                f"DASH: {remaining / 1000:.1f}s",
                True,
                (180, 220, 255)
            )

            SCREEN.blit(
                dash_text,
                (20, 155)
            )

        else:

            dash_font = pygame.font.Font(
                None,
                24
            )

            dash_text = dash_font.render(
                "DASH READY [SHIFT]",
                True,
                (100, 220, 255)
            )

            SCREEN.blit(
                dash_text,
                (20, 155)
            )

        if coin_combo > 1 and pygame.time.get_ticks() < coin_combo_until:

            combo_font = pygame.font.Font(
                None,
                30
            )

            combo_text = combo_font.render(
                f"COIN COMBO x{coin_combo}!",
                True,
                (255, 220, 70)
            )

            SCREEN.blit(
                combo_text,
                (WIDTH // 2 - 120, 25)
            )


    # ========================================================
    # SCORE
    # ========================================================

    score_text = score_font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        score_text,
        (20, 20)
    )


    if shield_active:

        shield_text = score_font.render(
            "SHIELD!",
            True,
            (80, 180, 255)
        )

        SCREEN.blit(
            shield_text,
            (20, 65)
        )


    if speed_boost_active:

        speed_text = score_font.render(
            "SPEED!",
            True,
            (255, 230, 40)
        )

        SCREEN.blit(
            speed_text,
            (20, 95)
        )


    if damage_boost_active:

        damage_text = score_font.render(
            "DAMAGE!",
            True,
            (255, 80, 80)
        )

        SCREEN.blit(
            damage_text,
            (20, 125)
        )


    # ========================================================
    # PAUSE MENU
    # ========================================================

    if game_paused:

        pause_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        pause_overlay.fill(
            (0, 0, 0, 170)
        )

        SCREEN.blit(
            pause_overlay,
            (0, 0)
        )

        pause_font = pygame.font.Font(
            None,
            80
        )

        pause_text = pause_font.render(
            "PAUSED",
            True,
            (255, 255, 255)
        )

        pause_rect = pause_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 30)
        )

        SCREEN.blit(
            pause_text,
            pause_rect
        )

        help_text = score_font.render(
            "Press P to continue",
            True,
            (220, 220, 220)
        )

        help_rect = help_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 45)
        )

        SCREEN.blit(
            help_text,
            help_rect
        )


    # ========================================================
    # PROCESS COMPLETED LEVEL
    # ========================================================

    if game_won and not level_unlock_processed:

        completed_levels.add(
            current_level
        )

        if current_level >= unlocked_levels:

            unlocked_levels = min(
                TOTAL_LEVELS,
                current_level + 1
            )

        level_unlock_processed = True


    # ========================================================
    # AUTOMATIC RESPAWN AFTER DEATH
    # ========================================================

    if (
        health <= 0
        and not game_won
        and death_respawn_at == 0
    ):

        death_respawn_at = (
            pygame.time.get_ticks() + 700
        )

        game_paused = False

        velocity_x = 0
        velocity_y = 0
        attacking = False

        for enemy_obj in enemies:
            enemy_obj.velocity_y = 0
            enemy_obj.knockback_velocity_x = 0
            enemy_obj.knockback_velocity_y = 0
            enemy_obj.is_attacking = False


    if (
        health <= 0
        and not game_won
        and death_respawn_at > 0
        and pygame.time.get_ticks() >= death_respawn_at
    ):

        game_paused = False
        show_help = False
        help_from_game = False

        health = MAX_HEALTH

        velocity_x = 0
        velocity_y = 0
        jumps_left = 2
        attacking = False

        player_effect = "appearing"
        player_effect_frame = 0
        player_effect_timer = pygame.time.get_ticks()

        player.x = int(respawn_x)
        player.y = int(respawn_y)

        player_x = respawn_x
        player_y = respawn_y

        last_damage_time = pygame.time.get_ticks()

        death_respawn_at = 0


    # ========================================================



    # ========================================================
    # SETTINGS SCREEN
    # ========================================================

    if settings_open:

        settings_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        settings_overlay.fill(
            (0, 0, 0, 225)
        )

        SCREEN.blit(
            settings_overlay,
            (0, 0)
        )

        settings_title_font = pygame.font.Font(
            None,
            68
        )

        settings_font = pygame.font.Font(
            None,
            38
        )

        title = settings_title_font.render(
            "SETTINGS",
            True,
            (255, 255, 255)
        )

        SCREEN.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 120)
            )
        )

        values = [
            f"{int(music_volume * 100)}%",
            f"{int(sfx_volume * 100)}%",
            (
                "ON"
                if music_muted
                else "OFF"
            ),
            ""
        ]

        for index, item in enumerate(
            SETTINGS_ITEMS
        ):

            selected = (
                index == settings_selection
            )

            prefix = "> " if selected else ""

            if item == "MUTE MUSIC":
                display_text = (
                    prefix
                    + item
                    + ": "
                    + values[index]
                )
            elif item == "BACK":
                display_text = prefix + item
            else:
                display_text = (
                    prefix
                    + item
                    + ": "
                    + values[index]
                )

            text = settings_font.render(
                display_text,
                True,
                (
                    (255, 220, 70)
                    if selected
                    else (235, 235, 235)
                )
            )

            SCREEN.blit(
                text,
                text.get_rect(
                    center=(
                        WIDTH // 2,
                        220 + index * 75
                    )
                )
            )

        hint = pygame.font.Font(
            None,
            25
        ).render(
            "UP/DOWN = Select   LEFT/RIGHT = Change   ESC = Back",
            True,
            (200, 200, 200)
        )

        SCREEN.blit(
            hint,
            hint.get_rect(
                center=(WIDTH // 2, HEIGHT - 40)
            )
        )


    # Never draw the victory screen over menus.
    if menu_open or level_select_open:
        game_won = False


    # ========================================================
    # LEVEL SELECT SCREEN
    # ========================================================

    if level_select_open:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 225)
        )

        SCREEN.blit(
            overlay,
            (0, 0)
        )

        title_font = pygame.font.Font(
            None,
            64
        )

        title = title_font.render(
            "SELECT LEVEL",
            True,
            (255, 255, 255)
        )

        SCREEN.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 70)
            )
        )

        # 10 level boxes: 3 + 3 + 3 + 1
        box_width = 150
        box_height = 70
        gap_x = 20
        gap_y = 25

        grid_width = (
            3 * box_width
            + 2 * gap_x
        )

        grid_left = (
            WIDTH - grid_width
        ) // 2

        for i in range(TOTAL_LEVELS):

            row = i // 3
            col = i % 3

            # Center the final single level.
            if row == 3:
                x = WIDTH // 2
            else:
                x = (
                    grid_left
                    + col * (
                        box_width + gap_x
                    )
                    + box_width // 2
                )

            y = (
                155
                + row * (
                    box_height + gap_y
                )
            )

            box = pygame.Rect(
                x - box_width // 2,
                y - box_height // 2,
                box_width,
                box_height
            )

            unlocked = (
                i < unlocked_levels
            )

            completed = (
                i + 1
                in completed_levels
            )

            selected = (
                i == selected_level
            )

            border_width = 4 if selected else 2

            pygame.draw.rect(
                SCREEN,
                (
                    (255, 220, 70)
                    if selected
                    else (150, 150, 150)
                ),
                box,
                border_width,
                border_radius=10
            )

            if not unlocked:
                label = f"LEVEL {i + 1}"
                suffix = "LOCKED"
            elif completed:
                label = f"LEVEL {i + 1}"
                suffix = "DONE"
            else:
                label = f"LEVEL {i + 1}"
                suffix = ""

            # Pick a font that ALWAYS fits inside the box.
            font_size = 30

            while font_size >= 16:

                level_font = pygame.font.Font(
                    None,
                    font_size
                )

                label_text = label

                if suffix:
                    full_text = (
                        label_text
                        + " "
                        + suffix
                    )
                else:
                    full_text = label_text

                rendered = level_font.render(
                    full_text,
                    True,
                    (255, 255, 255)
                )

                if rendered.get_width() <= box.width - 14:
                    break

                font_size -= 2

            text_color = (
                (255, 220, 70)
                if selected
                else (
                    (235, 235, 235)
                    if unlocked
                    else (120, 120, 120)
                )
            )

            rendered = level_font.render(
                full_text,
                True,
                text_color
            )

            SCREEN.blit(
                rendered,
                rendered.get_rect(
                    center=box.center
                )
            )

        hint_font = pygame.font.Font(
            None,
            24
        )

        hint = hint_font.render(
            "ARROWS / WASD = Select   ENTER = Play   ESC = Back",
            True,
            (200, 200, 200)
        )

        SCREEN.blit(
            hint,
            hint.get_rect(
                center=(WIDTH // 2, HEIGHT - 35)
            )
        )


    # ========================================================
    # MAIN MENU SCREEN
    # ========================================================

    if menu_open:

        # Keep the actual game visible behind the menu.
        # The game itself is frozen while the menu is open.
        menu_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        menu_overlay.fill(
            (5, 15, 22, 150)
        )

        SCREEN.blit(
            menu_overlay,
            (0, 0)
        )

        title_font = pygame.font.Font(
            None,
            62
        )

        item_font = pygame.font.Font(
            None,
            38
        )

        hint_font = pygame.font.Font(
            None,
            22
        )

        title = title_font.render(
            "ALEK'S PLATFORMER",
            True,
            (255, 255, 255)
        )

        SCREEN.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 125)
            )
        )

        menu_start_y = 255
        menu_spacing = 72

        for index, item in enumerate(
            MENU_ITEMS
        ):

            selected = (
                index == menu_selection
            )

            text = item_font.render(
                (
                    "> " + item
                    if selected
                    else item
                ),
                True,
                (
                    (255, 220, 70)
                    if selected
                    else (235, 235, 235)
                )
            )

            SCREEN.blit(
                text,
                text.get_rect(
                    center=(
                        WIDTH // 2,
                        menu_start_y
                        + index * menu_spacing
                    )
                )
            )

        hint = hint_font.render(
            "UP / DOWN = Select     ENTER / SPACE = Choose",
            True,
            (210, 210, 210)
        )

        SCREEN.blit(
            hint,
            hint.get_rect(
                center=(WIDTH // 2, HEIGHT - 28)
            )
        )


    # ========================================================
    # HOW TO PLAY SCREEN
    # ========================================================

    if show_help:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 215))
        SCREEN.blit(overlay, (0, 0))

        title_font = pygame.font.Font(None, 64)
        body_font = pygame.font.Font(None, 30)

        title = title_font.render(
            "HOW TO PLAY",
            True,
            (255, 255, 255)
        )

        SCREEN.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 65)
            )
        )

        # Keep every instruction short enough to fit the help box.
        help_lines = [
            "MOVEMENT",
            "A / LEFT       Move left",
            "D / RIGHT      Move right",
            "SPACE          Jump",
            "SHIFT          Dash",
            "",
            "COMBAT",
            "F              Attack",
            "P              Pause",
            "H / ESC        Close this page",
            "",
            "YOUR GOAL",
            "Collect ALL fruits",
            "then reach the finish flag!",
            "",
            "POWER-UPS",
            "SPEED          Move faster",
            "SHIELD         Block damage",
            "DAMAGE         Stronger attacks",
            "",
            "BONUS",
            "Collect coins for combo points!",
            "MID BOSS       Level 5",
            "FINAL BOSS     Level 10",
            "",
            "WINNING",
            "ENTER / SPACE / N = Next Level",
            "L = Level Select"
        ]

        y = 105

        for line in help_lines:

            if line in (
                "MOVEMENT",
                "COMBAT",
                "YOUR GOAL",
                "POWER-UPS",
                "BONUS",
                "WINNING"
            ):
                text_font = pygame.font.Font(None, 34)
                text_color = (255, 220, 80)

            else:
                text_font = body_font
                text_color = (235, 235, 235)

            text = text_font.render(
                line,
                True,
                text_color
            )

            SCREEN.blit(
                text,
                text.get_rect(
                    center=(WIDTH // 2, y)
                )
            )

            y += 24

        instruction = (
            "Press H or ESC to continue"
            if help_from_game
            else "Press ENTER or SPACE to start"
        )

        bottom = body_font.render(
            instruction,
            True,
            (255, 220, 80)
        )

        SCREEN.blit(
            bottom,
            bottom.get_rect(
                center=(WIDTH // 2, HEIGHT - 35)
            )
        )


    # ========================================================
    # NEXT LEVEL WIN OVERLAY
    # ========================================================

    if game_won:

        win_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )
        win_overlay.fill((0, 0, 0, 190))
        SCREEN.blit(win_overlay, (0, 0))

        win_title_font = pygame.font.Font(None, 72)
        win_font = pygame.font.Font(None, 34)

        text = win_title_font.render(
            "YOU WIN!",
            True,
            (255, 220, 70)
        )
        SCREEN.blit(
            text,
            text.get_rect(
                center=(WIDTH // 2, 220)
            )
        )

        if current_level < TOTAL_LEVELS:
            text = win_font.render(
                f"LEVEL {current_level} COMPLETE!",
                True,
                (255, 255, 255)
            )
            SCREEN.blit(
                text,
                text.get_rect(
                    center=(WIDTH // 2, 300)
                )
            )

            text = win_font.render(
                "ENTER / SPACE / N = NEXT LEVEL",
                True,
                (235, 235, 235)
            )
            SCREEN.blit(
                text,
                text.get_rect(
                    center=(WIDTH // 2, 380)
                )
            )

            text = win_font.render(
                "L = LEVEL SELECT",
                True,
                (200, 200, 200)
            )
            SCREEN.blit(
                text,
                text.get_rect(
                    center=(WIDTH // 2, 430)
                )
            )

        else:
            text = win_font.render(
                "ALL 10 LEVELS COMPLETE!",
                True,
                (255, 255, 255)
            )
            SCREEN.blit(
                text,
                text.get_rect(
                    center=(WIDTH // 2, 310)
                )
            )

    pygame.display.flip()


# ============================================================
# QUIT
# ============================================================

pygame.quit()