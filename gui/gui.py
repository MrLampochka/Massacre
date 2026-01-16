from functools import partial
from typing import Optional, Callable

import pygame as pg
import pygame_gui as pg_gui
from pygame_gui.elements import UIPanel, UIButton, UILabel, UIStatusBar
from dataclasses import dataclass

from components.money import Money
from components.health import Health
from entities.players import Player


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
        player: Player

    def __init__(
        self,
        screen: pg.Surface,
        padding=0,
        max_button_count: int = 9,
        players: Optional[list[Player]] = None,
        units: Optional[list[dict]] = None,
        on_unit_click: Optional[Callable[[dict], None]] = None,
    ) -> None:
        self._screen = screen
        self._padding = padding
        self._manager = pg_gui.UIManager(
            screen.get_size(), f"config/gui_theme.json"
        )
        self._max_button_count = max_button_count
        self._calculate_layout()

        self._side_panels = {}
        self._unit_panel: UIPanel | None = None
        self._unit_button: list[Button] = []
        self._on_unit_click = on_unit_click

        # initialize UI manager
        self._add_side_panels(players)
        self._add_units_panel(units)
        self._add_bottom_panel()
        self._add_field()

        # control buttons
        self._add_exit_button()
        self._add_restart_button()

    def _calculate_layout(self) -> None:
        side_panel_w = self._screen.get_width() / 6
        bottom_h = side_panel_w / 2

        self._positions = {
            "exit_button": pg.Rect(
                self._padding,
                self._padding,
                exit_button_w := self._screen.get_width() / 15,
                top_buttons_h := self._screen.get_width() / 50,
            ),
            "restart_button": pg.Rect(
                self._padding + exit_button_w,
                self._padding,
                exit_button_w,
                top_buttons_h,
            ),
            "units_panel": pg.Rect(
                self._padding,
                top_buttons_h + self._padding,
                units_panel_w := self._screen.get_width() - self._padding * 2,
                units_panel_h := self._screen.get_width() / self._max_button_count / 2,
            ),
            Player.Side.LEFT: pg.Rect(
                self._padding,
                bottom_y := self._screen.get_height() - bottom_h - self._padding,
                side_panel_w,
                bottom_h,
            ),
            Player.Side.RIGHT: pg.Rect(
                left_panel_x := units_panel_w - side_panel_w + self._padding,
                bottom_y,
                side_panel_w,
                bottom_h,
            ),
            "bottom_panel": pg.Rect(
                bottom_panel_x := self._padding + side_panel_w + self._padding / 2,
                bottom_y,
                left_panel_x - self._padding / 2 - bottom_panel_x,
                bottom_h,
            ),
            "field": pg.Rect(
                self._padding,
                start_y := self._padding / 2 + (units_panel_h + top_buttons_h) + self._padding,
                units_panel_w,
                bottom_y - self._padding / 2 - start_y,
            ),
        }

    def set_players(self, players: list[Player]) -> None:
        self._add_side_panels(players)
        self._add_bottom_panel()
        self._add_field()

    def set_units_cb(self, units: list[dict] = None, on_unit_click=None) -> None:
        self._on_unit_click = on_unit_click or self._on_unit_click
        self._add_units_buttons(units)

    def update(self, dt: float) -> None:
        if self._side_panels:
            self._update_labels()

        self._manager.update(dt)

    def _update_labels(self) -> None:
        for side_panel in self._side_panels.values():
            player = side_panel.player

            if money := player.get_component(Money):
                side_panel.label.set_text(f"Монеты: {money.amount}")

            if health := player.get_component(Health):
                side_panel.health_label.set_text(
                    f"{health.value.current} / {health.value.max}"
                )
                side_panel.progress_bar.percent_full = max(
                    0, health.value.current / health.value.max
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
        pg.draw.rect(
            self.field_surface, (125, 125, 125, 255), self.field_surface.get_rect(), 2
        )
        self._manager.draw_ui(surface)

    def _add_exit_button(self):
        Button(
            relative_rect=self._positions["exit_button"],
            text="Close",
            manager=self._manager,
            callback=lambda: pg.event.post(pg.event.Event(pg.QUIT)),
        )

    def _add_restart_button(self):
        Button(
            relative_rect=self._positions["restart_button"],
            text="Restart",
            manager=self._manager,
            callback=lambda: pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_r)),
        )

    def _add_units_panel(self, units):
        self._unit_panel = UIPanel(
            self._positions["units_panel"],
            starting_height=4,
            manager=self._manager,
        )

        self._add_units_buttons(units) if units else None

    def _add_units_buttons(self, units: list[dict]):
        if not self._unit_panel:
            return

        self._unit_button = []
        for u in units:
            padding = self._unit_panel.rect.height / 20
            width = (
                self._unit_panel.rect.width - padding * (self._max_button_count + 1)
            ) / self._max_button_count
            height = self._unit_panel.rect.height - padding * 2
            x, y = padding + len(self._unit_button) * (width + padding), padding

            unit_name, value = next(iter(u.items()))
            self._unit_button.append(
                Button(
                    callback=partial(self._on_unit_click, unit_name),
                    container=self._unit_panel,
                    relative_rect=pg.Rect(x, y, width, height),
                    text=f"{value.get('name')} {value.get('cost')}",
                    manager=self._manager,
                )
            )

    def _add_field(self):
        self.field_surface = self._screen.subsurface(self._positions["field"])

    def _add_bottom_panel(self):
        self.bottom_panel = UIPanel(
            self._positions["bottom_panel"],
            starting_height=4,
            manager=self._manager,
        )

    def _add_side_panels(self, players) -> None:
        self._side_panels = {}

        if players:
            for player in players:
                panel = UIPanel(
                    relative_rect=self._positions[player.side],
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

                self._side_panels[player.side] = self.SidePanel(
                    panel=panel,
                    label=label,
                    progress_bar=progress_bar,
                    health_label=health_label,
                    player=player,
                )
