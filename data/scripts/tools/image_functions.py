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

import pygame

def add_border(image, border_size=2, border_color=(255, 255, 255), alpha=255):
    border_color = (*border_color, alpha)

    mask = pygame.mask.from_surface(image)

    border_surf = pygame.Surface(
        (image.get_width() + border_size * 2, image.get_height() + border_size * 2),
        pygame.SRCALPHA
    )

    for dx in range(-border_size, border_size + 1):
        for dy in range(-border_size, border_size + 1):
            if dx != 0 or dy != 0:
                mask.to_surface(
                    border_surf,
                    setcolor=border_color,
                    unsetcolor=(0, 0, 0, 0),
                    dest=(dx + border_size, dy + border_size)
                )

    border_surf.blit(image, (border_size, border_size))

    return border_surf