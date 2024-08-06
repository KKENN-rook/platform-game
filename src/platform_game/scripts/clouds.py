import random


class Cloud:
    def __init__(self, pos, img, speed, depth):
        """
        Initialize a cloud object.
        Args:
            pos (tuple): The initial position (x, y) of the cloud.
            img (pygame.Surface): The image representing the cloud.
            speed (float): The speed at which the cloud moves horizontally.
            depth (float): The depth of the cloud, used for parallax effect.
        """
        self.pos = list(pos)  # Convert tuple to list for mutable operations
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        """
        Update the cloud's position based on its speed.
        """
        self.pos[0] += self.speed  # Move cloud horizontally

    def render(self, surf, offset=(0, 0)):
        """
        Render the cloud on the given surface with a parallax effect.
        Args:
            surf (pygame.Surface): The surface to draw the cloud on.
            offset (tuple): The camera offset
        """
        # Adjust cloud position based on depth to create parallax effect
        # Closer objects (larger depth) move faster
        rend_pos_x = self.pos[0] - offset[0] * self.depth
        rend_pos_y = self.pos[1] - offset[1] * self.depth
        # Wrap cloud position around to create an infinite scrolling effect
        # add/sub img w/h to avoid img teleporting from end to start upon wrap
        wrapped_x = (
            rend_pos_x % (surf.get_width() + self.img.get_width())
            - self.img.get_width()
        )
        wrapped_y = (
            rend_pos_y % (surf.get_height() + self.img.get_height())
            - self.img.get_height()
        )
        # Draw the cloud on the surface
        surf.blit(self.img, (wrapped_x, wrapped_y))


class Clouds:
    MIN_SPEED = 0.05
    MAX_SPEED = 0.1
    MIN_DEPTH = 0.2
    MAX_DEPTH = 0.8

    def __init__(self, cloud_images, count=16):
        """
        Initialize a collection of clouds.
        Args:
            cloud_images (list): A list of cloud images to choose from.
            count (int): The number of clouds to generate.
        """
        self.clouds = []

        for _ in range(count):
            # Generate a cloud with random position, image, speed, and depth
            cloud = Cloud(
                pos=(random.random() * 99999, random.random() * 99999),
                img=random.choice(cloud_images),
                speed=random.uniform(Clouds.MIN_SPEED, Clouds.MAX_SPEED),
                depth=random.uniform(Clouds.MIN_DEPTH, Clouds.MAX_DEPTH),
            )
            self.clouds.append(cloud)

        # Sort clouds by depth to ensure correct rendering order (furthest to closest)
        self.clouds.sort(key=lambda cloud: cloud.depth)

    def update(self):
        """
        Update position of all clouds in the collection.
        """
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset=(0, 0)):
        """
        Render all clouds on the given surface with a parallax effect.
        Args:
            surface (pygame.Surface): The surface to draw the clouds on.
            offset (tuple): The camera offset
        """
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)
