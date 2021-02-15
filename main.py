import pygame
import random
import os

pygame.font.init()

WIDTH, HEIGHT = 600, 650 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

LEVEL_LIVES_FONT = pygame.font.SysFont("comicsans", 40)

FPS = 60

YELLOW = (255,255,0)

YELLOW_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))
RED_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))

YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))

BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

class Ship(object):
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move(self, vel):
        self.y += vel

def redraw_window(player, enemies, lives, level):
    WIN.blit(BG, (0,0))

    for enemy in enemies:
        enemy.draw(WIN)

    lives_draw_text = LEVEL_LIVES_FONT.render(f"Lives: {lives}", 1, YELLOW)
    level_draw_text = LEVEL_LIVES_FONT.render(f"Level: {level}", 1, YELLOW)

    WIN.blit(lives_draw_text, (10,10))
    WIN.blit(level_draw_text, (WIDTH- level_draw_text.get_width() -10,10))

    player.draw(WIN)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    lives = 5
    level = 0

    player = Player(250,300)
    player_vel = 5

    enemies = []
    wave_length = 5
    enemy_vel = 1

    run = True
    while run:
        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for _ in range(wave_length):
                enemies.append(Enemy(random.randrange(50, WIDTH-100),random.randrange(-1500,-100),random.choice(["red","green","blue"])))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] and player.x - player_vel > 0 : #Left
            player.x -= player_vel
        if key_pressed[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH : #Right
            player.x += player_vel
        if key_pressed[pygame.K_UP] and player.y - player_vel > 0 : #Up
            player.y -= player_vel
        if key_pressed[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT : #Down
            player.y += player_vel

        for enemy in enemies:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_width() > HEIGHT:
                enemies.remove(enemy)

        redraw_window(player, enemies, lives, level)

    pygame.quit()

main()