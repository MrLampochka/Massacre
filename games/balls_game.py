import pygame as pg
from core.ball import Ball, Hole
from core.game import BaseGame
from core.menu import SimpleMenuButton
from core.window import Window


class BallsGame(BaseGame):
    def _set_game(self):
        # Создаем шары
        self.sprites = pg.sprite.Group()
        self.sprites.add(Ball((x, y), 25) for x in range(100, 400, 55) for y in range(200, 400, 55))
        self.sprites.add(Ball((1000, 300), 25))
        # self.sprites.add(Ball((200, 300), 25))

        self.holes = pg.sprite.Group(*self._create_holes())
        self.boundary_lines = self._create_boundary_lines()

        self.exit_button = SimpleMenuButton("Выход", (10, 10),(50, 25), self.stop)

    def _create_holes(self, radius=50):
        rect = self.screen.get_rect()
        positions = [
            (radius, radius),  # top-left
            (rect.width // 2, radius),  # top-center
            (rect.width - radius, radius),  # top-right
            (radius, rect.height - radius),  # bottom-left
            (rect.width // 2, rect.height - radius),  # bottom-center
            (rect.width - radius, rect.height - radius),  # bottom-right
        ]
        # Смещаем чуть ближе к краям
        margin = 10
        adjustments = [(-margin, -margin), (0, -margin), (margin, -margin),
                       (-margin, margin), (0, margin), (margin, margin)]
        positions = [(x + dx, y + dy) for (x, y), (dx, dy) in zip(positions, adjustments)]
        return [Hole(pos, radius) for pos in positions]

    def _create_boundary_lines(self):
        centers = [hole.rect.center for hole in self.holes]
        return [
            (centers[0], centers[1]),
            (centers[1], centers[2]),
            (centers[2], centers[5]),
            (centers[5], centers[4]),
            (centers[4], centers[3]),
            (centers[3], centers[0]),
        ]

    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stop()
            for ball in self.sprites:
                ball.handle_event(event)

            self.exit_button.handle_event(event)

    def _update(self, dt: float):
        self._handle_collisions(dt)
        self._handle_boundaries()
        self._handle_holes()
        self.sprites.update(self.screen.get_rect(), dt)

    def _draw(self, screen):
        screen.fill((25, 120, 50))
        for start, end in self.boundary_lines:
            pg.draw.line(screen, (0, 0, 0), start, end, 20)
        self.holes.draw(screen)
        self.sprites.draw(screen)
        self.exit_button.draw(screen)

    def _handle_collisions(self, dt):
        for ball in self.sprites:
            pg.sprite.spritecollide(ball, self.sprites, False, lambda a,b: Ball.resolve_collision(dt, a, b))
            ball.update(self.screen.get_rect(), dt)

    def _handle_boundaries(self):
        for ball in self.sprites:
            for start, end in self.boundary_lines:
                self._reflect_ball_on_line(ball, start, end)

    def _reflect_ball_on_line(self, ball, start, end):
        line_vec = pg.math.Vector2(end) - pg.math.Vector2(start)
        if line_vec.length() == 0:
            return
        line_dir = line_vec.normalize()
        to_ball = pg.math.Vector2(ball.rect.center) - pg.math.Vector2(start)
        proj = to_ball.dot(line_dir)
        closest = pg.math.Vector2(start) + max(0.0, min(proj, line_vec.length())) * line_dir
        diff = pg.math.Vector2(ball.rect.center) - closest
        if diff.length() < ball.radius and diff.length() != 0:
            n = diff.normalize()
            ball.velocity -= 2 * ball.velocity.dot(n) * n
            ball.pos += n * (ball.radius - diff.length())

    def _handle_holes(self):
        for ball in list(self.sprites):
            if any(hole.is_ball_inside(ball) for hole in self.holes):
                self.sprites.remove(ball)




if __name__ == "__main__":
    pg.init()
    BallsGame(Window(size=(800, 600), caption="Simple Game", FPS=60)).start()
    pg.quit()