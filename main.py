import pygame
import os

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))


def redraw_window():
    WIN.blit(BACKGROUND_IMG, (0,0))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window()
                
    pygame.quit()

if __name__ == "__main":
    main()