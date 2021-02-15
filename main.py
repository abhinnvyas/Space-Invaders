import pygame
import os

pygame.font.init()

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

LIVES_LEVEL_FONT = pygame.font.SysFont('comicsans', 40)

YELLOW = (255,255,0)
WHITE = (0,0,0)

FPS = 60

SPACESHIP_WIDTH = 60
SPACESHIP_HEIGHT = 60

BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

MAIN_SHIP = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png')), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
MAIN_SHIP_VEL = 5


def redraw_window(main_ship, lives, level):
    WIN.blit(BACKGROUND_IMG, (0,0))

    lives_display_text = LIVES_LEVEL_FONT.render(f"Lives:  {lives}", 1, YELLOW)
    level_display_text = LIVES_LEVEL_FONT.render(f"Level: {level}", 1, YELLOW)

    WIN.blit(lives_display_text, (10,10))
    WIN.blit(level_display_text, (WIDTH - level_display_text.get_width() - 10,10))

    WIN.blit(MAIN_SHIP, (main_ship.x,main_ship.y))
    
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    main_ship = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    lives = 5
    level = 1

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] and main_ship.x - MAIN_SHIP_VEL > 0:
            main_ship.x -= MAIN_SHIP_VEL
        if key_pressed[pygame.K_RIGHT] and main_ship.x + MAIN_SHIP_VEL + main_ship.width < WIDTH:
            main_ship.x += MAIN_SHIP_VEL
        if key_pressed[pygame.K_UP] and main_ship.y - MAIN_SHIP_VEL > 0:
            main_ship.y -= MAIN_SHIP_VEL
        if key_pressed[pygame.K_DOWN] and main_ship.y + MAIN_SHIP_VEL +  main_ship.width < HEIGHT:
            main_ship.y += MAIN_SHIP_VEL

        redraw_window(main_ship, lives, level)
                
    pygame.quit()

main()