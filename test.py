import pygame

class RadioButton:
    def __init__(self, x, y, radius, label, font, selected=False,
                 circle_color=(200, 200, 200), fill_color=(50, 150, 250), text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.label = label
        self.font = font
        self.circle_color = circle_color
        self.fill_color = fill_color
        self.text_color = text_color
        self.selected = selected

    def draw(self, surface, scroll=(0,0)):
        # Outer circle
        pygame.draw.circle(surface, self.circle_color,
                           (self.x - scroll[0], self.y - scroll[1]), self.radius, 2)
        # Inner filled circle if selected
        if self.selected:
            pygame.draw.circle(surface, self.fill_color,
                               (self.x - scroll[0], self.y - scroll[1]), self.radius - 4)

        # Draw label
        text_surface = self.font.render(self.label, True, self.text_color)
        surface.blit(text_surface,
                     (self.x + self.radius + 10 - scroll[0],
                      self.y - text_surface.get_height() // 2 - scroll[1]))

    def handle_event(self, mouse_pos, event, scroll=(0,0)):
        mx, my = mouse_pos
        adj_x, adj_y = self.x - scroll[0], self.y - scroll[1]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx, dy = mx - adj_x, my - adj_y
            if dx*dx + dy*dy <= self.radius*self.radius:
                return True
        return False


class RadioButtonGroup:
    def __init__(self, options, x, y, spacing, radius, font,
                 circle_color=(200,200,200), fill_color=(50,150,250), text_color=(255,255,255)):
        self.buttons = []
        for i, label in enumerate(options):
            self.buttons.append(RadioButton(x, y + i*spacing, radius, label, font,
                                            selected=(i==0), # First one selected by default
                                            circle_color=circle_color,
                                            fill_color=fill_color,
                                            text_color=text_color))

    def draw(self, surface, scroll=(0,0)):
        for btn in self.buttons:
            btn.draw(surface, scroll)

    def handle_event(self, mouse_pos, event, scroll=(0,0)):
        for i, btn in enumerate(self.buttons):
            if btn.handle_event(mouse_pos, event, scroll):
                # Deselect all others
                for b in self.buttons:
                    b.selected = False
                btn.selected = True
                return i  # return selected index
        return None

    def get_selected(self):
        for i, btn in enumerate(self.buttons):
            if btn.selected:
                return i, btn.label
        return None, None

pygame.init()
screen = pygame.display.set_mode((600,400))
font = pygame.font.SysFont(None, 28)

radio_group = RadioButtonGroup(["Option 1", "Option 2", "Option 3"],
                               x=100, y=100, spacing=40, radius=15, font=font)

running = True
while running:
    screen.fill((30,30,30))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        res = radio_group.handle_event(mouse_pos, event)
        if res is not None:
            print("Selected:", radio_group.get_selected())

    radio_group.draw(screen)
    pygame.display.flip()

