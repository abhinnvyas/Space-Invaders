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
        self.cooldown_time = 0
        self.cooldown_counter = 0
        self.spawn_time = 0
        self.health_bar_color = (0, 0, 0)
        self.max_health = health
        self.laser_damage = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        self.health_bar(window)
        for laser in self.lasers:
            laser.draw(window)
            laser.move()
            if laser.is_offscreen(window.get_height()):
                self.lasers.remove(laser)
                del laser

    def cooldown(self):
        if pygame.time.get_ticks() - self.spawn_time >= self.cooldown_time:
            self.cooldown_counter = 0

    def shoot(self, vel):
        self.cooldown()
        if self.cooldown_counter == 0:
            laser = Laser(self.x + self.laser_img.get_width()//2 - 2,
                          self.y - 10, self.laser_img, vel, self.laser_damage)
            self.lasers.append(laser)
            self.spawn_time = pygame.time.get_ticks()
            self.cooldown_counter = 1

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def collide(self, obj1, obj2):
        x_offset = obj2.x - obj1.x
        y_offset = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (x_offset, y_offset)) != None

    def collisions(self, enemy):
        for laser in self.lasers:
            if self.collide(laser, enemy):
                enemy.health -= laser.damage
                self.lasers.remove(laser)
                return True

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.x,
                                                   self.y+self.get_height()+10, self.get_width(), 10))
        pygame.draw.rect(window, self.health_bar_color, (self.x+2, self.y +
                                                         self.get_height()+12, (self.get_width()-4)*(self.health/self.max_health), 5))


class Player(Ship):

    IMG = pygame.transform.scale(pygame.image.load(
        os.path.join('assets', 'player_space_ship.png')), (55, 55))
    LASER = pygame.transform.scale(pygame.image.load(
        os.path.join('assets', 'pixel_laser_red.png')), (30, 50))

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.img = self.IMG
        self.laser_img = self.LASER
        self.laser_damage = 20
        self.mask = pygame.mask.from_surface(self.img)
        self.cooldown_time = 300
        self.vel = 5
        self.health_bar_color = (0, 255, 0)


class Enemy(Ship):
    SHIP = {
        "level1": (pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space_ship_lvl1.png')), (55, 55)), 180), pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png')), (30, 50)), 20, 10),
        "level2": (pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space_ship_lvl2.png')), (55, 55)), 180), pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png')), (30, 50)), 40, 30),
        "level3": (pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space_ship_lvl3.png')), (55, 55)), 180), pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_laser_green.png')), (30, 50)), 60, 40)
    }

    def __init__(self, x, y, level, health=100):
        super().__init__(x, y, health=health)
        self.health = self.SHIP[level][2]
        self.max_health = self.health
        self.img = self.SHIP[level][0]
        self.laser_img = self.SHIP[level][1]
        self.laser_damage = 20
        self.cooldown_time = 2000
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 1
        self.health_bar_color = (255, 0, 0)
        self.collision_damage = self.SHIP[level][3]

    def move(self):
        self.y += self.vel

    def activate(self, bullet_vel):
        super().shoot(vel=bullet_vel)
        self.move()
