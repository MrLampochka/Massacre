import pygame as pg

import config
from core.game import BaseGame
from core.gui.gui import GUI
from core.players import BotPlayer, HumanPlayer, BasePlayer
from core.window import Window


class TowerDefense(BaseGame):
    def _set_game(self):
        self.players = [

        ]

        for player in self.players:
            player.set(self.screen)
            player.enemy = [p for p in self.players if p != player]

        self.gui = GUI(self.screen, 9, config.GUI_PADDING, self.players)
        self.surface = self.gui.field_surface

        # self.control = ControlComponent(
        #     self.player1.units.sprites()[0],
        #     lambda target_pos: BasePlayer.shot(
        #         self.player1.units.sprites()[0],
        #         target_pos - self.gui.field_surface_offset,
        #         self.player1,
        #         self.gui.field_surface.get_rect(),
        #     ),
        # )

        # self.collided = pg.sprite.Group(
        #     *self.players[0].targets_list,
        #     *self.players[1].targets_list
        # )

    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            elif not self.gui.event_handler(event):
                for p in self.players:
                    p.event_handler(event)

    def _update(self, dt):
        for p in self.players:
            p.update(dt)

        self.gui.update(dt)


        # # TODO: update collision method
        # if config.COLLISION:
        #     self.collided.empty()
        #     self.collided.add(*self.players[0].targets_list, *self.players[1].targets_list)
        #     pg.sprite.groupcollide(
        #         self.collided,
        #         self.collided,
        #         False,
        #         False,
        #         lambda x, y: Ball.resolve_collision(dt, x, y),
        #     )

    def _draw(self, screen):
        screen.fill((50, 50, 50))
        self.gui.draw(screen)
        for p in self.players:
            p.draw(self.surface)

        if config.DEBUG:
            for p in self.players:
                for u in p.units.sprites():
                    pg.draw.circle(self.gui.field_surface, (255, 125, 0), u.rect.center, int(u.targeting.radius), 2)
                    pg.draw.circle(self.gui.field_surface, (255, 0, 0), u.rect.center, int(u.weapon.radius), 2)

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
