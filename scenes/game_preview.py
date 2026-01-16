import pygame

from core.game import Game
from core.window import Window
# -----------------------------
# Создаём класс игры
# -----------------------------
class SimpleGame(Game):
    def _set_game(self):
        # координаты и размер квадрата в "базовых" единицах
        self.rect_pos = [100, 100]
        self.rect_size = 50
        self.rect_color = (255, 0, 0)
        self.rect_speed = 200  # пикселей в секунду

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.VIDEORESIZE:
                # обновляем размеры окна в классе Window
                self._window.size = (event.w, event.h)

        keys = pygame.key.get_pressed()
        self.move_x = 0
        self.move_y = 0
        if keys[pygame.K_LEFT]:
            self.move_x = -1
        if keys[pygame.K_RIGHT]:
            self.move_x = 1
        if keys[pygame.K_UP]:
            self.move_y = -1
        if keys[pygame.K_DOWN]:
            self.move_y = 1

    def _update(self, dt: float):
        # движение квадрата с учётом dt
        self.rect_pos[0] += self.move_x * self.rect_speed * dt
        self.rect_pos[1] += self.move_y * self.rect_speed * dt

        # ограничение движения по базовым координатам
        base_width, base_height = 800, 600  # базовые размеры окна
        self.rect_pos[0] = max(0, min(self.rect_pos[0], base_width - self.rect_size))
        self.rect_pos[1] = max(0, min(self.rect_pos[1], base_height - self.rect_size))

    def _draw(self, screen):
        self._window.screen.fill((30, 30, 30))

        # масштабируем координаты и размер квадрата
        scaled_rect = pygame.Rect(
            *self._window(x=self.rect_pos[0], y=self.rect_pos[1]),
            *self._window(x=self.rect_size, y=self.rect_size),
        )

        pygame.draw.rect(screen, self.rect_color, scaled_rect)


# -----------------------------
# Запуск игры
# -----------------------------
if __name__ == "__main__":
    pygame.init()
    game = SimpleGame(Window(size=(800, 600), caption="Simple Game", FPS=60))
    game.start()
    pygame.quit()