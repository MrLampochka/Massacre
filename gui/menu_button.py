import pygame


class SimpleMenuButton:
    def __init__(
        self,
        text,
        pos,
        size,
        callback=None,
        font=None,
        color=None,
        hover_color=None,
        text_color=None

    ):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = color or (50, 50, 50)
        self.default_color = color or (50, 50, 50)
        self.hover_color = hover_color or (100, 100, 100)
        self.text_color = text_color or (200, 200, 200)
        self.font = font or pygame.font.Font(None, 20)
        self.text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.button_serf = pygame.Surface(size)
        self.callback = callback

    def draw(self, surface):
        self.button_serf.fill(self.color)
        text_rect = self.text_surf.get_rect(
            center=(self.rect.width // 2, self.rect.height // 2)
        )
        self.button_serf.blit(self.text_surf, text_rect)
        surface.blit(self.button_serf, self.rect.topleft)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


    def update_color(self):
        self.color = self.hover_color if self.is_hovered() else self.default_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_hovered():
                if self.callback:
                    self.callback()  # вызываем действие кнопки

    def update_rect(self, pos, size):
        self.rect = pygame.Rect(pos, size)
