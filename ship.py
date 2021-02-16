import pygame
from laser import Laser
import os

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_time = 500
        self.cooldown_counter = 0
        self.spawn_time = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        
        for laser in self.lasers:
            laser.draw(window)
            laser.move()

    def cooldown(self):
        if pygame.time.get_ticks() - self.spawn_time >= self.cooldown_time :
            self.cooldown_counter = 0

    def shoot(self, vel):
        self.cooldown()
        if self.cooldown_counter == 0:
            laser = Laser(self.x + self.laser_img.get_width()//2 -2, self.y - 10, self.laser_img, vel)
            self.lasers.append(laser)
            self.spawn_time = pygame.time.get_ticks()
            self.cooldown_counter = 1

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

class Player(Ship):

    IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'player_space_ship.png')),(55,55))
    LASER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_laser_red.png')), (30,50))

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.img = self.IMG
        self.laser_img = self.LASER
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 5
