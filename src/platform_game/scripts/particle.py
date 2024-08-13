class Particle:
    def __init__(self, game, p_type, pos, velocity=[0, 0], frame=0):
        """
        Initialize a particle object.

        Args:
            game (Game): Reference to the main game object.
            p_type (str): Type of particle (used to fetch the correct animation).
            pos (tuple): Initial position of the particle (x, y).
            velocity (list, optional): Velocity of the particle (x, y). Defaults to [0, 0].
            frame (int, optional): Initial frame of the animation. Defaults to 0.
        """
        self.game = game
        self.type = p_type
        self.pos = list(pos)  # Convert position tuple to a list to allow modification.
        self.velocity = list(velocity)  # Convert velocity to a list to ensure it's mutable.
        self.animation = self.game.assets["particle/" + p_type].copy()  # Copy so it is unique to this particle
        self.animation.frame = frame  # Set the animation to start at the specified frame.

    def update(self):
        """
        Update the particle's state.
        Returns:
            bool: True if the particle's animation is complete and it should be removed, False otherwise.
        """
        kill = False
        if self.animation.done:
            kill = True  # Mark the particle for removal if the animation is complete.

        # Update the particle's position based on its velocity.
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Update the animation frame.
        self.animation.update()

        return kill

    def render(self, surf, offset=(0, 0)):
        """
        Render the particle on the given surface.
        Args:
            surf (pygame.Surface): The surface to draw the particle on.
            offset (tuple, optional): Offset for camera position. Defaults to (0, 0).
        """
        img = self.animation.img()  # Get the current frame of the animation.
        # Draw the particle on the surface, centered at its position minus the camera offset.
        surf.blit(
            img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2)
        )