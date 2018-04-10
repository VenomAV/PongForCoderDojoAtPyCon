#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random

SCREEN_SIZE = (640, 480)
TOP_BAR_HEIGHT = 40
BORDER_SIZE = 5
        
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/ball_base.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
        self.position = [ float(self.rect.center[0]), float(self.rect.center[1]) ]
        self.speed = [0.25, 0.3]
        
    def lowest_y_value(self):
        return TOP_BAR_HEIGHT + BORDER_SIZE + self.rect.height / 2

    def highest_y_value(self):
        return SCREEN_SIZE[1] - BORDER_SIZE - self.rect.height / 2
    
    def is_too_low(self):
        return self.position[1] < self.lowest_y_value()

    def is_too_high(self):
        return self.position[1] > self.highest_y_value()

    def is_too_left(self):
        return self.position[0] < 0

    def is_too_right(self):
        return self.position[0] > SCREEN_SIZE[0]

    def bounce_vertical(self):
        self.speed[1] *= -1

    def bounce_horizontal(self):
        self.speed[0] *= -1

    def update_bouncing(self, ms):

        self.position = (self.position[0] + self.speed[0] * ms, self.position[1] + self.speed[1] * ms)
        self.rect.center = self.position
        
        if self.is_too_low() or self.is_too_high():
            self.bounce_vertical()

        if self.is_too_left() or self.is_too_right():
            self.bounce_horizontal()
    
    def update(self, ms):
        self.update_bouncing(ms)
 
class Paddle(pygame.sprite.Sprite):
    Y_SPEED = 0.75

    def __init__(self, position, keys):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/paddle_vert.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.move_y = 0
        self.setup_keys(keys)

    def setup_keys(self, keys):
        self.key_move_down = keys[0]
        self.key_move_up = keys[1]

    def handle_key_down(self, key):
        if key == self.key_move_down:
            self.move_y = self.Y_SPEED
        elif key == self.key_move_up:
            self.move_y = -self.Y_SPEED
    
    def handle_key_up(self, key):
        if key == self.key_move_down and self.move_y == self.Y_SPEED:
            self.move_y = 0
        elif key == self.key_move_up and self.move_y == -self.Y_SPEED:
            self.move_y = 0

    def change_position(self, ms):
        self.rect.move_ip(0,self.move_y * ms)

    def lowest_y_value(self):
        return TOP_BAR_HEIGHT + BORDER_SIZE + self.rect.height / 2

    def highest_y_value(self):
        return SCREEN_SIZE[1] - BORDER_SIZE - self.rect.height / 2
    
    def is_too_low(self):
        return self.rect.center[1] < self.lowest_y_value()

    def is_too_high(self):
        return self.rect.center[1] > self.highest_y_value()

    def update(self, ms):
        self.change_position(ms)
        if self.is_too_low():
            self.rect.center = ( self.rect.center[0], self.lowest_y_value() )
        elif self.is_too_high():
            self.rect.center = ( self.rect.center[0], self.highest_y_value() )

class Game:

    RUNNING = 0
    GAME_OVER = 1

    def __init__(self, SCREEN_SIZE, caption):
        self.screen = self.init_game_window(SCREEN_SIZE, caption)
        self.backdrop = pygame.image.load('img/pong_a_2.bmp').convert()
        self.state = self.RUNNING
        self.create_game_sprites()
        self.clock = pygame.time.Clock()

    def is_game_over(self):
        return self.state == self.GAME_OVER
        
    def init_game_window(self, screen_size, caption):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(caption)
        return screen

    def render(self):
        self.screen.blit(self.backdrop,(0,0))
        self.sprites.draw(self.screen)
        self.ball_group.draw(self.screen)
        pygame.display.update()
        return self.clock.tick(60)
        
    def terminate(self):
        pygame.quit()

    def handle_events(self):
        for ourevent in pygame.event.get():
            if ourevent.type == pygame.QUIT:
                self.state = self.GAME_OVER

            if ourevent.type == pygame.KEYUP:
                if ourevent.key == pygame.K_ESCAPE:
                    self.state = self.GAME_OVER
                else:
                    for sprite in self.sprites:
                        sprite.handle_key_up(ourevent.key)

            if ourevent.type == pygame.KEYDOWN:
                for sprite in self.sprites:
                        sprite.handle_key_down(ourevent.key)

    def create_game_sprites(self):
        self.sprites = pygame.sprite.Group()
        self.sprites.add( Paddle( (20, SCREEN_SIZE[1] / 2), (pygame.K_z, pygame.K_a, pygame.K_s)))
        self.sprites.add( Paddle( (SCREEN_SIZE[0]-20, SCREEN_SIZE[1] / 2), (pygame.K_l, pygame.K_p, pygame.K_o)))
        self.ball_group = pygame.sprite.GroupSingle( Ball() )

    def update(self, ms):
        self.sprites.update(ms)
        self.ball_group.update(ms)

def main(args):
    game = Game(SCREEN_SIZE, "python pong")
    
    while not game.is_game_over():
        ms = game.render()
        game.handle_events()
        game.update(ms)
    
    game.terminate()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
