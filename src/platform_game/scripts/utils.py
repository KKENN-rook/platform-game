import pygame
import os

# Base path to the images directory
BASE_IMG_PATH = "src/platform_game/data/images/"


def load_image(path: str) -> pygame.Surface:
    """
    Loads an image from the specified path and converts it into a Pygame Surface object.
    Args:
        path (str): Relative path to the image file within the base image directory.
    Returns:
        pygame.Surface: The loaded and converted image as a Pygame Surface object.
    Raises:
        FileNotFoundError: If the image file does not exist at the specified path.
    """
    # Construct full path to the image
    full_path = os.path.join(BASE_IMG_PATH, path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Image file '{full_path}' not found.")

    img = pygame.image.load(full_path).convert()  # Convert the image to blit faster
    img.set_colorkey((0, 0, 0))  # Set the colorkey to make black (0, 0, 0) transparent
    return img


def load_images(path: str) -> list:
    """
    Loads all images in a specified directory and converts them into Pygame Surface objects.
    Args:
        path(str): Relative path to the directory containing image files.
    Returns:
        list: A list of Pygame Surface objects for all images in the specified directory.
    Raises:
        FileNotFoundError: If the specified directory does not exist.
    """
    # Construct full path to the directory
    dir_path = os.path.join(BASE_IMG_PATH, path)
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory '{dir_path}' not found.")

    images = []
    for img_name in sorted(os.listdir(dir_path)):  # Sorted to ensure consistent order across OSes
        img_path = os.path.join(path, img_name)
        images.append(load_image(img_path))  # Load and append the image as a Surface object
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        """
        Initialize an animation.
        Args:
            images (list): A list of Pygame Surface objects representing the frames of the animation.
            img_dur (int): The duration each frame is displayed, in terms of update calls (default is 5).
            loop (bool): Whether the animation should loop (default is True).
        """
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        """
        Create a copy of the animation.
        Returns:
            Animation: A new instance of the Animation class with the same properties.
        """
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        """
        Update the animation to progress to the next frame.
        If the animation loops, it will cycle through the frames indefinitely.
        If the animation does not loop, it will stop at the last frame.
        """
        self.frame += 1
        total_frames = self.img_dur * len(self.images)
        if self.loop:
            self.frame %= total_frames 
        else:
            if self.frame >= total_frames - 1: # -1 to account for frames starting at 0 
                self.frame = total_frames - 1 
                self.done = True

    def img(self):
        """
        Get the current frame image.
        Returns:
            pygame.Surface: The current frame image.
        """
        curr_img_idx = int(self.frame / self.img_dur)
        return self.images[curr_img_idx]
