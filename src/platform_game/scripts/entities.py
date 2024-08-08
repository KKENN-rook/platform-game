import pygame


class PhysicsEntity:
    def __init__(self, game, ent_type, pos, size):
        """
        Initialize a physics-based entity.
        Args:
            game (Game): Reference to the game object.
            ent_type (str): Type of the entity.
            pos (tuple): Initial position of the entity (x, y).
            size (tuple): Size of the entity (w x h in pixels)
        """
        self.game = game
        self.type = ent_type
        self.pos = list(pos)  # Shallow copy list to ensure each entity has its own pos
        self.size = size
        self.velocity = [0, 0]  # Initial velocity (x, y)
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        # Animation attributes
        self.action = None
        self.animation = None
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")

    def rect(self):
        """
        Create a Pygame Rect object for the entity.
        Returns:
            pygame.Rect: A rectangle representing the entity's position and size.
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def reset_collisions(self):
        """
        Reset the collision states for the entity.
        """
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

    def calc_displacement(self, movement):
        """
        Calculate the displacement (per frame) of the entity based on movement and velocity.
        Args:
            movement (tuple): The movement input (x, y).
        Returns:
            tuple: The calculated displacement (dx, dy).
        """
        return (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

    def update_pos_x(self, tilemap, dx):
        """
        Update the entity's X position and handle collisions.
        Args:
            tilemap (Tilemap): The tilemap for collision detection.
            dx (float): The displacement in the X direction.
        """
        self.pos[0] += dx
        # Check for collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_create_rects(self.pos):
            if entity_rect.colliderect(rect):
                if dx > 0:  # Moving Right
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if dx < 0:  # Moving Left
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                # Resolve char position
                self.pos[0] = entity_rect.x

    def update_pos_y(self, tilemap, dy):
        """
        Update the entity's Y position and handle collisions.
        Args:
            tilemap (Tilemap): The tilemap for collision detection.
            dy (float): The displacement in the Y direction.
        """
        self.pos[1] += dy
        # Check for collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_create_rects(self.pos):
            if entity_rect.colliderect(rect):
                if dy > 0:  # Falling
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if dy < 0:  # Jumping
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                # Resolve char position
                self.pos[1] = entity_rect.y

    def update_direction(self, movement_x):
        """
        Update the direction the entity is facing based on horizontal movement.
        Args:
            movement_x (float): The horizontal movement input.
        """
        if movement_x > 0:
            self.flip = False
        if movement_x < 0:
            self.flip = True

    def update_vy(self):
        """
        Update the y-axis velocity.
        """
        # Apply gravity, ensuring terminal velocity (5) is not exceeded
        self.velocity[1] = min(self.velocity[1] + 0.1, 5)

        # Reset velocity if a surface is met
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def update(self, tilemap, movement=(0, 0)):
        """
        Update the entity's position based on movement and velocity.
        Args:
            tilemap (Tilemap): The tilemap for collision detection.
            movement (tuple): The movement input (x, y).
        """
        self.reset_collisions()
        d_xy = self.calc_displacement(movement)
        self.update_pos_x(tilemap, d_xy[0])
        self.update_pos_y(tilemap, d_xy[1])
        self.update_direction(movement[0])
        self.update_vy()
        self.animation.update()

    def render(self, surface, offset=(0, 0)):
        """
        Draw the entity on the given surface at its current position.
        Args:
            surface (pygame.Surface): The surface to draw the entity on.
            offset (tuple): Coordinates to offset for the camera position.
        """
        # Calculate the render position
        render_pos_x = self.pos[0] - offset[0] + self.anim_offset[0]
        render_pos_y = self.pos[1] - offset[1] + self.anim_offset[1]
        render_pos = (render_pos_x, render_pos_y)

        # Get the current frame of the animation
        current_frame = self.animation.img()

        # Flip the image if necessary
        flipped_frame = pygame.transform.flip(current_frame, self.flip, False)

        # Blit the image onto the surface
        surface.blit(flipped_frame, render_pos)

    def set_action(self, action):
        """
        Set the current action of the entity and update the animation.
        Args:
            action (str): The new action to set.
        """
        if action != self.action:
            self.action = action
            # Make a copy of the animation to start from the beginning
            self.animation = self.game.assets[self.type + "/" + self.action].copy()


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        """
        Initialize the player entity.
        Args:
            game (Game): Reference to the game object.
            pos (tuple): Initial position of the player (x, y).
            size (tuple): Size of the player (w x h in pixels).
        """
        super().__init__(game, "player", pos, size)
        self.air_time = 0

    def update_airtime(self):
        """
        Update the airtime of the player based on collision with the ground.
        Resets airtime if the player is on the ground, otherwise increments it.
        """
        if self.collisions["down"]:
            self.air_time = 0
        else:
            self.air_time += 1

    def update_action(self, movement=(0, 0)):
        """
        Update the player's action based on movement and airtime.
        Sets the appropriate animation state based on current conditions.
        Args:
            movement (tuple): The movement input (x, y).
        """
        if self.air_time > 4:
            self.set_action("jump")
        elif movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

    def update(self, tilemap, movement=(0, 0)):
        """
        Update the player's state, including position, collisions, airtime, and actions.
        Args:
            tilemap (Tilemap): The tilemap for collision detection.
            movement (tuple): The movement input (x, y).
        """
        super().update(tilemap, movement=movement)
        self.update_airtime()
        self.update_action(movement)
