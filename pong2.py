#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

SCREEN_SIZE = (640, 480)

class Game:
    def __init__(self, SCREEN_SIZE, caption):
        self.screen = self.init_game_window(SCREEN_SIZE, caption)
        self.backdrop = pygame.image.load('img/pong_a_2.bmp').convert()
        
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

def main(args):
    game = Game(SCREEN_SIZE, "python pong")
    
    terminate = False
    while not terminate:
        for ourevent in pygame.event.get():
            if ourevent.type == pygame.QUIT:
                terminate = True
        game.render()
    
    game.terminate()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
