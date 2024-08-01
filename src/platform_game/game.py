import pygame
import sys


class Game:
    def __init__(self):
        # pygame window set-up
        pygame.init()
        pygame.display.set_caption('Platform Game')
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            pygame.display.update()
            # 60 fps
            self.clock.tick(60)

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

Game().run()