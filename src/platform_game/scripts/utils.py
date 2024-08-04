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
    for img_name in sorted(
        os.listdir(dir_path)
    ):  # Sorted to ensure consistent order across OSes
        img_path = os.path.join(path, img_name)
        images.append(
            load_image(img_path)
        )  # Load and append the image as a Surface object
    return images
