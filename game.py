import pygame
from ship import Enemy, Player
from menu import Menu
import os
import random

pygame.font.init()

NORMAL_FONT = pygame.font.SysFont('comicsans', 40, True)
WIN_OVER_FONT = pygame.font.SysFont('comicsans', 100)
f = pygame.font.SysFont("segoeuisymbol", 30, True)

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

LEVELS = {
    "level1": 3,
    "level2": 4,
    "level3": 5
}

FPS = 60

BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

COLLISION = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "collision.png")), (55, 55))


def draw_text(text):
    text_label = WIN_OVER_FONT.render(text, 1, (255, 255, 0))
    WIN.blit(text_label, (WIDTH//2 - text_label.get_width() //
                          2, HEIGHT//2 - text_label.get_height()//2))
    pygame.display.update()


def redraw_window(player, enemies, lives, wave):

    WIN.blit(BG, (0, 0))

    for enemy in enemies:
        enemy.draw(WIN)
        enemy.activate(bullet_vel=4)
        if enemy.collisions(player):
            WIN.blit(COLLISION, (player.x, player.y))
        if player.collisions(enemy):
            WIN.blit(COLLISION, (enemy.x, enemy.y))
        if player.collide(player, enemy):
            player.health -= 10
            WIN.blit(COLLISION, (enemy.x, enemy.y))
            enemies.remove(enemy)
            WIN.blit(COLLISION, (player.x, player.y))

    lives_draw_text = f.render(
        f"{lives}❤", 1, (255, 0, 0))
    wave_draw_text = NORMAL_FONT.render(f"Level:{wave}", 1, (255, 255, 0))

    WIN.blit(lives_draw_text, (WIDTH - lives_draw_text.get_width() -
                               10, 10 + wave_draw_text.get_height()))
    WIN.blit(wave_draw_text, (WIDTH - wave_draw_text.get_width() - 10, 10))

    player.draw(WIN)

    pygame.display.update()


def game_loop():
    clock = pygame.time.Clock()

    player = Player(300, 500)

    enemies = []
    wave_length = 5

    lives = 3
    wave = 0
    total_wave = 3

    lost = False
    lost_count = 0

    won = False
    won_count = 0

    run = True
    while run:
        clock.tick(FPS)

        if wave > total_wave:
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
            if wave <= total_wave:
                wave += 1
            try:
                for _ in range(wave_length):
                    enemy = Enemy(random.randrange(
                        50, WIDTH-100), random.randrange(-1500, -100), level=f"level{wave}")
                    enemies.append(enemy)
            except KeyError:
                continue

        for enemy in enemies:
            if enemy.y + enemy.vel + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)
                del enemy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] and player.x - player.vel > 0:
            player.x -= player.vel
        if key_pressed[pygame.K_RIGHT] and player.x + player.vel + player.get_width() < WIDTH:
            player.x += player.vel
        if key_pressed[pygame.K_UP] and player.y - player.vel > 0:
            player.y -= player.vel
        if key_pressed[pygame.K_DOWN] and player.y + player.vel + player.get_height() < HEIGHT:
            player.y += player.vel
        if key_pressed[pygame.K_SPACE]:
            player.shoot(vel=-3)

        redraw_window(player, enemies, lives, wave)


def main_menu():
    state = {
        "START GAME": game_loop,
        "QUIT": pygame.quit
    }

    font = pygame.font.SysFont("comicsans", 40)
    menu = Menu(state, font, (255, 255, 0),
                10, 10)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            menu.handle_events(event)

        WIN.blit(BG, (0, 0))
        menu.draw(WIN)

        # pygame.display.update()


main_menu()
