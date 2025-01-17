import pygame

color_key = (0, 0, 0)

def load_image(path, alpha = 255):
    path = "data/images/" + path
    image = pygame.image.load(path)
    image.set_alpha(alpha)
    image.set_colorkey(color_key)
    return image

def scale_image_size(image, width, height):
    image = pygame.transform.scale(image, [width, height])
    return image

def scale_image_ratio(image, ratio):
    width, height = image.get_width(), image.get_height()
    image = pygame.transform.scale(image, (width * ratio, height * ratio))
    return image

def swap_color(img, old_color, new_color):
    img.set_colorkey(old_color)
    surface = img.copy()
    surface.fill(new_color)
    surface.blit(img, (0, 0))
    surface.set_colorkey(color_key)
    return surface

def clip_surface(surface, x, y, x_size, y_size):
    handle_surface = surface.copy()
    clip_rect = pygame.Rect(x, y, x_size, y_size)
    handle_surface.set_clip(clip_rect)
    image = surface.subsurface(handle_surface.get_clip())
    return image.copy()