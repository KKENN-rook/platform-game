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

        self.img = pygame.image.load('src/platform_game/data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0, 0, 0))  # black(0,0,0) becomes transparent
        self.img_pos = [160, 260]
        self.movement = [False, False]  # [Up, Down]


    def run(self):
        while self.running:
            self.screen.fill((14, 219, 248))  # Sky-color background
            # Moves image based on key presses
            self.img_pos[1] += self.movement[1] - self.movement[0]
            # Blit draws source at destination (source, dest)
            self.screen.blit(self.img, self.img_pos)
            
            for event in pygame.event.get():
                # Exit window
                if event.type == pygame.QUIT:
                    self.quit()
                # Key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                # Key release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            # 60 fps
            self.clock.tick(60)

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

Game().run()