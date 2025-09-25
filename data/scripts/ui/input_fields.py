import pygame

from data.scripts.tools.font import Font

text_color=(255, 255, 255)
dropdown_text_color = text_color
radio_text_color = text_color
slider_text = Font('small_font.png', text_color, 3)
dropdown_text = Font('small_font.png', dropdown_text_color, 3)
radio_text = Font('small_font.png', radio_text_color, 3)

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val, color=(200,200,200), knob_color=(255, 0, 0)):
        self.text_height = slider_text.image_height
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.color = color
        self.knob_color = knob_color
        self.knob_radius = height // 2 + 10
        self.dragging = False

    def draw(self, surface, scroll = (0, 0)):
        slider_text.display_fonts(surface, str(int(self.value)), [self.rect.x - scroll[0] + self.rect.width + 20,
                                    self.rect.y - scroll[1] - (self.text_height - self.rect.height) // 2], 5)
        pygame.draw.rect(surface, self.color, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width,
                                               self.rect.height))

        knob_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        knob_y = self.rect.centery

        pygame.draw.circle(surface, self.knob_color, (knob_x - scroll[0], knob_y - scroll[1]), self.knob_radius)

    def handle_event(self, mouse_pos, event, scroll = (0, 0)):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = mouse_pos
            knob_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
            knob_y = self.rect.centery
            if (mouse_x - knob_x + scroll[0]) ** 2 + (mouse_y - knob_y + scroll[1]) ** 2 <= self.knob_radius**2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = mouse_pos
            mouse_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))
            self.value = self.min_val + (mouse_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
            return self.value

        return None


class RadioButton:
    def __init__(self, x, y, radius, label, selected=False,
                 circle_color=(255, 0, 0), fill_color=(200, 0, 0), text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.label = label
        self.circle_color = circle_color
        self.fill_color = fill_color
        self.text_color = text_color
        self.selected = selected
        self.text_height = radio_text.image_height
        self.width = radio_text.get_width(self.label, 5)

    def draw(self, surface, scroll=(0,0)):

        pygame.draw.circle(surface, self.circle_color,
                           (self.x - scroll[0], self.y - scroll[1]), self.radius, 2)

        if self.selected:
            pygame.draw.circle(surface, self.fill_color,
                               (self.x - scroll[0], self.y - scroll[1]), self.radius - 4)

        radio_text.display_fonts(surface, self.label, [self.x + self.radius + 10 - scroll[0],
                      self.y - self.text_height // 2 - scroll[1]], 5)

    def handle_event(self, mouse_pos, event, scroll=(0,0)):
        mouse_x, mouse_y = mouse_pos
        adj_x, adj_y = self.x - scroll[0], self.y - scroll[1]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx, dy = mouse_x - adj_x, mouse_y - adj_y
            if dx*dx + dy*dy <= self.radius*self.radius:
                return True
        return False


class RadioButtonGroup:
    def __init__(self, options, x, y, spacing = 10, radius = 15, selected_option = 0,
                 circle_color=(200, 200,200), fill_color=(200, 0, 0), text_color=(255, 255, 255)):
        self.buttons = []
        self.height = 0
        self.widht = 0
        for i, label in enumerate(options):
            self.buttons.append(RadioButton(x, y + i*spacing + self.height, radius, label,
                                            selected=(i==selected_option),
                                            circle_color=circle_color,
                                            fill_color=fill_color,
                                            text_color=text_color))
            self.height += self.buttons[i].text_height + spacing
            self.width = max(self.widht, self.buttons[i].width)

    def draw(self, surface, scroll=(0,0)):
        for btn in self.buttons:
            btn.draw(surface, scroll)

    def handle_event(self, mouse_pos, event, scroll=(0,0)):
        for i, btn in enumerate(self.buttons):
            if btn.handle_event(mouse_pos, event, scroll):
                for b in self.buttons:
                    b.selected = False
                btn.selected = True
                return i
        return None

    def get_selected(self):
        for i, btn in enumerate(self.buttons):
            if btn.selected:
                return btn.label
        return None, None

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
        main_rect = self.rect.move(-scroll[0], -scroll[1])
        pygame.draw.rect(surface, self.bg_color, main_rect)
        pygame.draw.rect(surface, self.border_color, main_rect, 2)

        # Draw selected text
        dropdown_text.display_fonts(
            surface,
            str(self.options[self.selected_index]),
            [main_rect.x + 5, main_rect.y + (main_rect.height - self.text_height)//2]
        )

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
        mouse_x, mouse_y = mouse_pos
        adjusted_rect = self.rect.move(-scroll[0], -scroll[1])

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if adjusted_rect.collidepoint(mouse_x, mouse_y):
                self.open = not self.open
                return None

            if self.open:
                for i, rect in enumerate(self.option_rects):
                    adj_rect = rect.move(-scroll[0], -scroll[1])
                    if adj_rect.collidepoint(mouse_x, mouse_y):
                        self.selected_index = i
                        self.open = False
                        return i
                self.open = False
        return None
