import pygame
from ship import Enemy, Player
import os
import random

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

FPS = 60

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")),(WIDTH, HEIGHT))

def redraw_window(player, enemies):
    WIN.blit(BG, (0, 0))
    
    for enemy in enemies:
        enemy.draw(WIN)
        enemy.shoot(vel=4)
        enemy.move()

    player.draw(WIN)
    pygame.display.update()

def game_loop():
    clock = pygame.time.Clock()

    player = Player(300,500)

    wave_lenth = 5
    enemies = []

    run = True
    while run:
        clock.tick(FPS)

        if len(enemies) < wave_lenth:
            for _ in range(wave_lenth):
                enemy = Enemy(random.randrange(50, WIDTH-100),random.randrange(-1500,-100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] and player.x - player.vel > 0 :
            player.x -= player.vel
        if key_pressed[pygame.K_RIGHT] and player.x + player.vel + player.get_width() < WIDTH :
            player.x += player.vel
        if key_pressed[pygame.K_UP] and player.y - player.vel > 0 :
            player.y -= player.vel
        if key_pressed[pygame.K_DOWN] and player.y + player.vel + player.get_height() < HEIGHT :
            player.y += player.vel
        if key_pressed[pygame.K_SPACE]:
            player.shoot(vel=-5)

        redraw_window(player, enemies)

game_loop()