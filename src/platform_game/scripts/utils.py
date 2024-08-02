import pygame

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