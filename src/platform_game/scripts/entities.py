import pygame


class PhysicsEntity:
    def __init__(self, game, ent_type, pos, size):
        self.game = game
        self.type = ent_type
        self.pos = list(pos)  # Shallow copy list to ensure each ent has its own pos
        self.size = size
        self.velocity = [0, 0]

    def rect(self):
        """Create a rect around the Entity"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        self.pos[0] += frame_movement[0]  # Update X pos
        entity_rect = self.rect()
        for rect in tilemap.physics_create_rects(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]  # Update Y pos
        entity_rect = self.rect()
        for rect in tilemap.physics_create_rects(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y
        


        # Gravity, min func to implement terminal velocity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

    def render(self, surface):
        surface.blit(self.game.assets["player"], self.pos)
