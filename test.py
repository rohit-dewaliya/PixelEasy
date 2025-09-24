import pygame

from data.scripts.tools.font import Font

dropdown_text = Font('small_font.png', (255, 255, 255), 3)


class Dropdown:
    def __init__(self, x, y, width, height, options, selected_index=0,
                 bg_color=(50, 50, 50), text_color=(255, 255, 255),
                 hover_color=(70, 70, 70), border_color=(200, 200, 200)):
        self.rect = pygame.Rect(x - width // 2, y, width, height)
        self.options = options
        self.selected_index = selected_index
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.text_height = dropdown_text.image_height

        self.open = False
        self.option_rects = [pygame.Rect(x - width // 2, y + (i + 1) * height, width, height)
                             for i in range(len(options))]

    def draw(self, surface, scroll=[0, 0]):
        # Draw main rectangle
        main_rect = self.rect.move(-scroll[0], -scroll[1])
        pygame.draw.rect(surface, self.bg_color, main_rect)
        pygame.draw.rect(surface, self.border_color, main_rect, 2)

        # Draw selected text
        dropdown_text.display_fonts(
            surface,
            str(self.options[self.selected_index]),
            [main_rect.x + 5, main_rect.y + (main_rect.height - self.text_height)//2]
        )

        # Draw options if open
        if self.open:
            for i, option in enumerate(self.options):
                rect = self.option_rects[i].move(-scroll[0], -scroll[1])
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(surface, self.hover_color, rect)
                else:
                    pygame.draw.rect(surface, self.bg_color, rect)
                pygame.draw.rect(surface, self.border_color, rect, 2)

                dropdown_text.display_fonts(
                    surface,
                    option,
                    [rect.x + 5, rect.y + (rect.height - self.text_height)//2]
                )

    def handle_event(self, mouse_pos, event, scroll=[0, 0]):
        mx, my = mouse_pos
        adj_main = self.rect.move(-scroll[0], -scroll[1])

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Toggle dropdown
            if adj_main.collidepoint(mx, my):
                self.open = not self.open
                return None

            # Check options if open
            if self.open:
                for i, rect in enumerate(self.option_rects):
                    adj_rect = rect.move(-scroll[0], -scroll[1])
                    if adj_rect.collidepoint(mx, my):
                        self.selected_index = i
                        self.open = False
                        return i
                self.open = False
        return None


pygame.init()
screen = pygame.display.set_mode((600,400))
scroll_y = 0
dropdown = Dropdown(100, 600, 100, 50, ["apple", "ball", "car", "dog"])
running = True
while running:
    screen.fill((30,30,30))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll_y += 20
            if event.button == 5:
                scroll_y -= 20

        dropdown.handle_event(mouse_pos, event, [0, scroll_y])

    dropdown.draw(screen, [0, scroll_y])

    pygame.display.flip()
