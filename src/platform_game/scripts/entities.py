import pygame


class PhysicsEntity:
    def __init__(self, game, ent_type, pos, size):
        self.game = game
        self.type = ent_type
        self.pos = list(pos)  # Shallow copy list to ensure each ent has its own pos
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement=(0, 0)):
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        self.pos[0] += frame_movement[0]  # Update X pos
        self.pos[1] += frame_movement[1]  # Update Y pos

    def render(self, surface):
        surface.blit(self.game.assets["player"], self.pos)
