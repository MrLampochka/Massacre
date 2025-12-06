import pygame as pg

import config
from core.ball import Ball
from core.game import BaseGame
from core.control import SpriteControl
from core.gui.gui import GUI
from core.players import BotPlayer, HumanPlayer, BasePlayer
from core.window import Window


class TowerDefense(BaseGame):
    def _set_game(self):
        self.player1 = HumanPlayer(side=BasePlayer.Side.LEFT)
        self.player2 = BotPlayer(side=BotPlayer.Side.RIGHT)

        self.player1.enemy, self.player2.enemy = self.player2, self.player1
        self.players = [self.player1, self.player2]

        # for player in self.players:
        self.player2.set(self.screen)
        self.player1.set(self.screen)



        self.gui = GUI(self.screen, 9, config.GUI_PADDING, self.players)

        self.control = SpriteControl(
            self.player1.units.sprites()[0],
            lambda target_pos: BasePlayer.shot(
                self.player1.units.sprites()[0],
                target_pos - self.gui.field_surface_offset,
                self.player1,
                self.gui.field_surface.get_rect(),
            ),
        )

        self.collided = pg.sprite.Group(
            *self.players[0].targets_list, *self.players[1].targets_list
        )

    def _events(self):
        for event in pg.event.get():
            self.gui.handler(event)
            self.control.handler(event, self.start, self.stop)

    def _update(self, dt):
        [p.update(dt) for p in self.players]
        self.gui.update(dt)

        # TODO: improve control
        self.control.update(dt)

        # TODO: update collision method
        if config.COLLISION:
            self.collided.empty()
            self.collided.add(*self.players[0].targets_list, *self.players[1].targets_list)
            pg.sprite.groupcollide(
                self.collided,
                self.collided,
                False,
                False,
                lambda x, y: Ball.resolve_collision(dt, x, y),
            )

    def _draw(self, screen):
        screen.fill((50, 50, 50))
        self.gui.draw(screen)

        if config.DEBUG:
            fps = self._clock.get_fps()
            fps_text = pg.font.SysFont(None, 24).render(
                f"fps: {int(fps)}", True, (255, 255, 255)
            )  # Белый цвет
            screen.blit(fps_text, (10, 10))  # В левом верхнем углу


if __name__ == "__main__":
    pg.init()
    # TowerDefense(Window(size=pg.display.get_desktop_sizes()[0], caption="Simple Game", FPS=120, flags=pg.FULLSCREEN | pg.DOUBLEBUF)).start()
    TowerDefense(
        Window(size=(1280, 720), caption="Simple Game", FPS=120, flags=pg.DOUBLEBUF)
    ).start()
    pg.quit()
