import pygame
from ship import Enemy, Player
import os
import random

pygame.font.init()

NORMAL_FONT = pygame.font.SysFont('comicsans', 40)
WIN_OVER_FONT = pygame.font.SysFont('comicsans',100)

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

FPS = 60

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")),(WIDTH, HEIGHT))

def draw_text(text):
    text_label = WIN_OVER_FONT.render(text,1,(255,255,0))
    WIN.blit(text_label, (WIDTH//2 - text_label.get_width()//2, HEIGHT//2 - text_label.get_height()//2))
    pygame.display.update()

def redraw_window(player, enemies, lives, wave):
    WIN.blit(BG, (0, 0))
    
    for enemy in enemies:
        enemy.draw(WIN)
        enemy.shoot(vel=4)
        enemy.move()
        enemy.collisions(player)
        player.collisions(enemy)
        if player.collide(player,enemy):
            player.health -= 10
            enemies.remove(enemy)

    lives_draw_text = NORMAL_FONT.render(f"Lives: {lives}", 1, (255,255,0))
    wave_draw_text = NORMAL_FONT.render(f"Level: {wave}", 1, (255,255,0))

    WIN.blit(lives_draw_text, (10,10))
    WIN.blit(wave_draw_text, (WIDTH- wave_draw_text.get_width() -10,10))

    player.draw(WIN)
    
    pygame.display.update()

def game_loop():
    clock = pygame.time.Clock()

    player = Player(300,500)

    wave_length = 0
    enemies = []

    lives = 5
    wave = 0
    total_wave = 3

    lost = False
    lost_count = 0

    won = False
    won_count = 0

    run = True
    while run:
        clock.tick(FPS)

        if wave == total_wave:
            draw_text("You Won!")
            won = True
            won_count += 1

        if won:
            if won_count > FPS * 3:
                break
            else:
                continue

        if lives == 0:
            draw_text("Game Over!")
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                break
            else:
                continue

        if player.health <= 0:
            lives -= 1
            player.health = player.max_health
        for enemy in enemies:
            if enemy.health <= 0:
                enemies.remove(enemy)
                del enemy

        if len(enemies) == 0:
            if wave < total_wave:
                wave += 1
                wave_length += 5
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100),random.randrange(-1500,-100), level=f"level{wave}", health=20)
                enemies.append(enemy)

        for enemy in enemies:
            if enemy.y + enemy.vel + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)
                del enemy

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
            player.shoot(vel=-3)

        redraw_window(player, enemies, lives, wave)

game_loop()