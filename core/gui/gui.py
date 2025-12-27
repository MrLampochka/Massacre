from functools import partial
from typing import Callable, Optional

import pygame
import pygame as pg
import pygame_gui as pg_gui
from pygame import Vector2
from pygame_gui.elements import UIPanel, UIButton, UILabel, UIStatusBar
from dataclasses import dataclass

from core.players import BasePlayer


class Button(UIButton):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    def click(self) -> None:
        self.callback()


class GUI:
    @dataclass
    class SidePanel:
        panel: UIPanel
        label: UILabel
        progress_bar: UIStatusBar
        health_label: UILabel

    def __init__(
        self,
        screen: pg.Surface,
        max_button_count: int,
        padding,
        players: Optional[list[BasePlayer]] = None,
        units: Optional[list[dict]] = None,
        player_buttons = None,
    ) -> None:
        self._screen = screen
        self._units: list[dict] = units or []
        self._players = players or []
        self._player_buttons = player_buttons or self._players[0] if self._players else None
        self._padding = padding

        self._max_button_count = max_button_count
        self._side_panels = {}
        self._buttons = []
        self.unit_panel = None

        self._manager = pg_gui.UIManager(screen.get_size(), "core/gui/themes/theme.json")
        self._bottom_panels_y = self._screen.get_height() - 100 - self._padding
        self._add_units_button()
        self._add_side_panel()
        self._add_bottom_button()
        self._add_exit_button()
        self._add_restart_button()
        self._add_field()

    def update(self, dt: float) -> None:
        if self._side_panels:
            self._update_labels()

        self._manager.update(dt)

    def _update_labels(self) -> None:
        for player in self._players:
            side_panel = self._side_panels[player.side]
            side_panel.label.set_text(f"Монеты: {player.coins}")
            side_panel.health_label.set_text(
                f"{player.health.value.current} / {player.health.value.max}"
            )
            side_panel.progress_bar.percent_full = max(
                0, player.health.value.current / player.health.value.max
            )

    def event_handler(self, event: pg.event.Event) -> bool:
        self._manager.process_events(event)

        if event.type == pg_gui.UI_BUTTON_PRESSED:
            ui = event.ui_element
            if isinstance(ui, Button):
                ui.click()
            return True

        return False

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.rect(self.field_surface, (75, 75, 75, 0), self.field_surface.get_rect(), 5)
        surface.blit(self.field_surface, self.field_surface_offset)
        self._manager.draw_ui(surface)

    def _add_exit_button(self):
        self._buttons.append(
            Button(
                relative_rect=pg.Rect(
                    self._padding, 0, self._padding * 5, self._padding
                ),
                text="Close",
                manager=self._manager,
                callback=lambda: pg.event.post(
                    pg.event.Event(pg.QUIT)
                ),
            )
        )

    def _add_restart_button(self):
        self._buttons.append(
            Button(
                relative_rect=pg.Rect(
                    self._padding * 6, 0, self._padding * 5, self._padding
                ),
                text="Restart",
                manager=self._manager,
                callback=lambda: pg.event.post(
                    pg.event.Event(pg.K_r)
                ),
            )
        )

    def _add_units_button(self):
        if self._player_buttons:
            self._add_unit_panel()

            for unit in self._units:
                self._add_button(
                    f"{unit['name']} {unit['cost']}",
                    partial(self._player_buttons.add_unit, unit),
                )

    def _add_field(self):
        start_y = self._padding + (self.unit_panel.rect.height + self._padding / 2) if self.unit_panel else 0
        end_y = self._bottom_panels_y - self._padding / 2 if self._side_panels else self._screen.get_height() - self._padding
        self.field_surface = pg.Surface((self._screen.get_width() - 2 * self._padding, end_y - start_y), pygame.SRCALPHA)
        self.field_surface_offset = Vector2(self._padding, start_y)


    def _add_bottom_button(self):
        if not self._side_panels:
            return

        start_x = self._padding + self._padding / 2 + next(iter(self._side_panels.values())).panel.rect.width
        self.bottom_panel = UIPanel(
            pg.Rect(
                start_x,
                self._bottom_panels_y,
                self._screen.get_width() - start_x - self._padding - self._padding / 2 - next(iter(self._side_panels.values())).panel.rect.width,
                next(iter(self._side_panels.values())).panel.rect.height,
            ),
            starting_height=4,
            manager=self._manager,
        )

    def _add_unit_panel(self) -> None:
        self.unit_panel = UIPanel(
            pg.Rect(
                self._padding,
                self._padding,
                self._screen.get_width() - self._padding * 2,
                self._screen.get_width() / self._max_button_count / 2,
            ),
            starting_height=4,
            manager=self._manager,
        )

    def _add_side_panel(self) -> None:
        positions = {
            BasePlayer.Side.LEFT: (
                self._padding,
                self._bottom_panels_y,
            ),
            BasePlayer.Side.RIGHT: (
                self._screen.get_width() - 200 - self._padding,
                self._bottom_panels_y,
            ),
        }
        for p in self._players:
            panel = UIPanel(
                relative_rect=pg.Rect(*positions[p.side], 200, 100),
                starting_height=4,
                manager=self._manager,
            )
            label = UILabel(
                relative_rect=pg.Rect(10, 10, 200, 30),
                text="",
                manager=self._manager,
                container=panel,
            )
            progress_bar = UIStatusBar(
                relative_rect=pg.Rect(10, 50, 180, 30),
                manager=self._manager,
                container=panel,
                object_id=pg_gui.core.ObjectID("#progress_bar", "@UIStatusBar"),
            )
            health_label = UILabel(
                relative_rect=pg.Rect(10, 50, 180, 20),
                text="",
                manager=self._manager,
                container=panel,
            )

            self._side_panels[p.side] = self.SidePanel(
                panel=panel,
                label=label,
                progress_bar=progress_bar,
                health_label=health_label,
            )

    def _add_button(self, name: str, callback: Callable) -> None:
        padding = self.unit_panel.rect.height / 20
        width = (
            self.unit_panel.rect.width - padding * (self._max_button_count + 1)
        ) / self._max_button_count
        height = self.unit_panel.rect.height - padding * 2
        x, y = padding + len(self._buttons) * (width + padding), padding

        button_rect = pg.Rect(x, y, width, height)

        self._buttons.append(
            Button(
                callback=callback,
                container=self.unit_panel,
                relative_rect=button_rect,
                text=name,
                manager=self._manager,
            )
        )
