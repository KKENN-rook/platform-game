import pygame
import os 

# Base path to the images directory
BASE_IMG_PATH = 'src/platform_game/data/images/'


def load_image(path: str) -> object:
    """ 
    Converts image into pygame Surface object

    Args:
        path (str): Path to image

    Returns:
        object: Surface object 
    """
    img = pygame.image.load(BASE_IMG_PATH + path).convert() # convert for faster draws
    img.set_colorkey((0, 0, 0))  # Makes black bgs transparent when blitting
    return img

def load_images(path):
    """
    Converts all images in a directory specified by path into a surface object
    """
    images = []
    # Sorted due to non-windows os (ex. linux)
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): 
        images.append(load_image(path + '/' + img_name))
    return images 