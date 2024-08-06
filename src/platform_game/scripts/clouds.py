import random


class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0, 0)):
        # Multiple by depth to create a parallax effect
        rend_pos_x = self.pos[0] - offset[0] * self.depth
        rend_pos_y = self.pos[1] - offset[1] * self.depth
        surface.blit(
            self.img,
            (
                rend_pos_x % (surface.get_width() + self.img.get_width())
                - self.img.get_width(),
                rend_pos_y % (surface.get_height() + self.img.get_height())
                - self.img.get_height(),
            ),
        )


class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for i in range(count):
            self.clouds.append(
                Cloud(
                    (random.random() * 99999, random.random() * 99999),
                    random.choice(cloud_images),
                    random.random() * 0.05 + 0.05,
                    random.random() * 0.6 + 0.2,
                )
            )

        self.clouds.sort(key=lambda x: x.depth)
        
    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
