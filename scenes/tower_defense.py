import pygame as pg

from components.ai_control import AIControl
from config.prefabs import unit_prefabs_sorted
from core.game import Game
from gui.gui import GUI
from entities.players import ControlledPlayer, Player, AIPlayer
from core.window import Window


class TowerDefense(Game):
    def _set_game(self):
        self.draw_order = ["units", "towers", "projectiles", "gui"]

        self.gui = GUI(self.screen, 0)
        self.players = [
            ControlledPlayer(self.gui.field_surface, Player.Side.LEFT, 1000),
            AIPlayer(self.gui.field_surface, Player.Side.RIGHT, 1000)
        ]

        for p in self.players:
            p.set(self.players)

        self.gui.set_players(self.players)

        units_list = unit_prefabs_sorted()
        self.gui.set_units_cb(units_list, self.players[0].buy_unit)
        self.set_unit_hotkeys_cb = {
            pg.K_1 + i: next(iter(units_list[i].keys()))
            for i in range(min(9, len(units_list)))
        }

    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stop()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.stop()
                elif event.key == pg.K_r:
                    self.start()
                elif event.key in self.set_unit_hotkeys_cb:
                    self.players[1].buy_unit(self.set_unit_hotkeys_cb[event.key])

            if self.gui and not self.gui.event_handler(event):
                for p in self.players:
                    p.event_handler(event)

    def _update(self, dt):
        for p in self.players:
            p.update(dt)
        self.gui.update(dt)

    def _draw(self, screen):
        screen.fill((50, 50, 50))

        self.gui.field_surface.fill((100, 100, 100))

        for p in self.players:
            p.draw(self.gui.field_surface)

        for group_name in self.draw_order:
            for p in self.players:
                if group := p.groups.get(group_name):
                    group.draw(self.gui.field_surface)

        self.gui.draw(screen)
        # self.debugging_draw(screen)

    def debugging_draw(self, screen):
        for p in self.players:
            for u in p.groups["units"].sprites():
                if comp := u.game_object.get_component(AIControl):
                    pg.draw.circle(self.gui.field_surface, (255, 125, 0), u.rect.center, comp.attack_radius, 1)
                    pg.draw.circle(self.gui.field_surface, (255, 0, 0), u.rect.center, comp.detect_radius, 1)

        fps = self._clock.get_fps()
        fps_text = pg.font.SysFont(None, 24).render(
            f"fps: {int(fps)}", True, (255, 255, 255)
        )

        screen.blit(fps_text, (10, 10))


if __name__ == "__main__":
    pg.init()
    # TowerDefense(Window(size=pg.display.get_desktop_sizes()[0], caption="Simple Game", FPS=120, flags=pg.FULLSCREEN | pg.DOUBLEBUF)).start()
    TowerDefense(
        Window(size=(1280, 720), caption="Simple Game", FPS=120, flags=pg.DOUBLEBUF)
    ).start()
    pg.quit()
