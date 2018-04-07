#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

SCREEN_SIZE = (640, 480)

class Game:

    RUNNING = 0
    GAME_OVER = 1

    def __init__(self, SCREEN_SIZE, caption):
        self.screen = self.init_game_window(SCREEN_SIZE, caption)
        self.backdrop = pygame.image.load('img/pong_a_2.bmp').convert()
        self.state = self.RUNNING

    def is_game_over(self):
        return self.state == self.GAME_OVER
        
    def init_game_window(self, screen_size, caption):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(caption)
        return screen

    def render(self):
        self.screen.blit(self.backdrop,(0,0))
        pygame.display.update()
        
    def terminate(self):
        pygame.quit()

    def handle_events(self):
        for ourevent in pygame.event.get():
            if ourevent.type == pygame.QUIT:
                self.state = self.GAME_OVER

def main(args):
    game = Game(SCREEN_SIZE, "python pong")
    
    while not game.is_game_over():
        game.render()
        game.handle_events()
    
    game.terminate()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
