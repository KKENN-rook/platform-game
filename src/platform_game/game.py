import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image


class Game:
    def __init__(self):
        # pygame window set-up
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))  # Window
        self.clock = pygame.time.Clock()
        self.running = True

        self.display = pygame.Surface((320, 240))  # Display to be upscaled

        self.movement = [False, False]  # [Left, Right]
        self.assets = {"player": load_image("entities/player.png")}
        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))

    def run(self):
        while self.running:
            self.display.fill((14, 219, 248))  # Sky-color background

            self.player.update((self.movement[1] - self.movement[0], 0))  # (x, y)
            self.player.render(self.display)

            # # Blit draws source at destination (source, dest)
            # self.screen.blit(self.img, self.img_pos)

            for event in pygame.event.get():
                # Exit window
                if event.type == pygame.QUIT:
                    self.quit()
                # Key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                # Key release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # Render the upscaled display onto the game window 
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0) 
            )

            pygame.display.update()
            self.clock.tick(60)  # 60 FPS

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()


# game = Game()
# print(game.img.get_size())
Game().run()
