import pygame

class Laser:
    def __init__(self, x, y, img, vel,damage=10):
        self.x = x
        self.y = y
        self.damage = damage
        self.img = img
        self.vel = vel
        self.mask = pygame.mask.from_surface(self.img)

    def move(self):
        self.y += self.vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def is_offscreen(self, height):
        return self.y + self.img.get_height() > height or self.y < 0
