import pygame
pygame.font.init()


class Menu:

    def __init__(self, states, font, color, x, y):
        self.states = states
        self.start_state = 0
        self.font = font
        self.color = color
        self.x = x
        self.y = y

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.start_state != 0:
                    self.start_state -= 1
            if event.key == pygame.K_DOWN:
                if self.start_state != len(self.state)-1:
                    self.start_state += 1
            if event.key == pygame.K_RETURN:
                self.states[self.start_state]

    def draw(self, window):
        for state in self.states:
            text = self.font.render(state[0], 1, self.color)
            window.blit(text, (self.x + 10, self.y + 10))
            pygame.draw.rect(window, self.color, (self.x, self.y,
                                                  text.get_width() + 20, text.get_height() + 20))
            #self.y += text.get_height()

    def activate(self, window):
        self.handle_events()
        self.draw(window)
