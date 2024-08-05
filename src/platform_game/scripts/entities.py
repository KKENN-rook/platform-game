import pygame


class PhysicsEntity:
    def __init__(self, game, ent_type, pos, size):
        """
        Initialize a physics-based entity.

        Args:
            game (Game): Reference to the game object.
            ent_type (str): Type of the entity.
            pos (tuple): Initial position of the entity (x, y).
            size (tuple): Size of the entity (width, height) (Pixels of asset).
            collisions (dict): Collision detection bools
        """
        self.game = game
        self.type = ent_type
        self.pos = list(
            pos
        )  # Shallow copy list to ensure each entity has its own position
        self.size = size
        self.velocity = [0, 0]  # Initial velocity (x, y)
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

    def rect(self):
        """
        Create a Pygame Rect object for the entity.

        Returns:
            pygame.Rect: A rectangle representing the entity's position and size.
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        """
        Update the entity's position based on movement and velocity.

        Args:
            tilemap (Tilemap): The tilemap for collision detection.
            movement (tuple): The movement input (x, y).
        """
        # Reset collisions between updates
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

        # Calculate frame movement based on input movement and current velocity
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        # Update the X position
        self.pos[0] += frame_movement[0]
        # Check for collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_create_rects(self.pos):
            if entity_rect.colliderect(rect):
                # Moving Right
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                # Moving Left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                # Update position
                self.pos[0] = entity_rect.x

        # Update the Y position
        self.pos[1] += frame_movement[1]
        # Check for collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_create_rects(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:  # Falling
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:  # Jumping
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                # Update position
                self.pos[1] = entity_rect.y

        # Apply gravity, ensuring terminal velocity (5) is not exceeded
        self.velocity[1] = min(self.velocity[1] + 0.1, 5)

        # Reset velocity if a surface is met
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, surface, offset=(0, 0)):
        """
        Render the entity on the given surface at its current position

        Args:
            surface (pygame.Surface): The surface to draw the entity on.
            offset (tuple): Coordinates to offset for mock camera.
        """
        surface.blit(
            self.game.assets[self.type],
            (self.pos[0] - offset[0], self.pos[1] - offset[1]),
        )
