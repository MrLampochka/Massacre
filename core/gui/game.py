from dataclasses import dataclass
from typing import Callable

import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIPanel, UIButton, UILabel, UIStatusBar

import config


@dataclass
class Button:
    name: str
    callback_func: Callable


class GUI:
    def __init__(self, max_button_count):
        self.right_health_label = None
        self.left_health_label = None
        self.right_progress_bar = None
        self.left_progress_bar = None
        self.GUI_padding = None
        self.right_label = None
        self.left_label = None
        self.button_size = None
        self.button_height = None
        self.button_width = None
        self.button_padding = None
        self.unit_panel = None
        self.manager = None
        self.buttons = []
        self.uibuttons = []
        self.max_button_count = max_button_count

    def add_button(self, name, callback):
        self.buttons.append(Button(name, callback))

    def set(self, screen):
        self.uibuttons = []
        self.GUI_padding = config.GUI_PADDING
        self.manager = pygame_gui.UIManager(screen.size, 'core/gui/themes/gui_theme.json')
        self.unit_panel = UIPanel(
            pygame.Rect(self.GUI_padding, self.GUI_padding, screen.width - self.GUI_padding * 2, screen.width / self.max_button_count),
            starting_height=4,
            manager=self.manager
        )
        self.button_padding = self.unit_panel.rect.h / 20
        self.button_width = ((self.unit_panel.rect.width - self.button_padding) / self.max_button_count) - self.button_padding
        self.button_height = self.unit_panel.rect.height - self.button_padding - self.button_padding
        self.button_size = self.button_width, self.button_height

        for i, b in enumerate(self.buttons):
            pos = (self.button_width + self.button_padding) * i + self.button_padding, self.button_padding
            self.uibuttons.append(
                UIButton(
                    container=self.unit_panel,
                    relative_rect=pygame.Rect(pos, self.button_size),
                    text=f'{b.name}',
                    manager=self.manager
                )
            )

        # Создание панелей для нижнего левого и нижнего правого углов
        left_panel = UIPanel(relative_rect=pygame.Rect(self.GUI_padding, screen.height - 100 - self.GUI_padding, 200, 100),
                             starting_height=4,
                             manager=self.manager)

        right_panel = (UIPanel(relative_rect=pygame.Rect(screen.width - 200 - self.GUI_padding, screen.height - 100 - self.GUI_padding, 200, 100),
                               starting_height=4,
                               manager=self.manager))

        # Создание текстовых меток
        self.left_label = UILabel(
            relative_rect=pygame.Rect(10, 10, 200, 30),
            text='Монеты: 0',
            manager=self.manager,
            container=left_panel,
        )

        self.right_label = UILabel(
            relative_rect=pygame.Rect(10, 10, 200, 30),
            text='Монеты: 0',
            manager=self.manager,
            container=right_panel,
        )



        self.left_progress_bar = UIStatusBar(
            relative_rect=pygame.Rect(10, 50, 180, 30),
            manager=self.manager,
            container=left_panel,
            object_id=ObjectID('#progress_bar', '@UIStatusBar')
        )

        self.right_progress_bar = UIStatusBar(
            relative_rect=pygame.Rect(10, 50, 180, 30),
            manager=self.manager,
            container=right_panel,
            object_id=ObjectID('#progress_bar', '@UIStatusBar')
        )

        self.left_health_label = UILabel(
            relative_rect=pygame.Rect(10, 50, 180, 20),
            text='Здоровье',
            manager=self.manager,
            container=left_panel,
        )

        self.right_health_label = UILabel(
            relative_rect=pygame.Rect(10, 50, 180, 20),
            text='Здоровье',
            manager=self.manager,
            container=right_panel,
        )

    def update(self, time_delta, player_one, player_two):
        self.left_label.set_text(f"Монеты: {player_one.coins}")
        self.right_label.set_text(f"Монеты: {player_two.coins}")
        self.left_health_label.set_text(f"{player_one.health} / {player_one.max_health}")
        self.right_health_label.set_text(f"{player_two.health} / {player_two.max_health}")
        self.left_progress_bar.percent_full = max(0, (player_one.health / player_one.max_health))
        self.right_progress_bar.percent_full = max(0, (player_two.health / player_two.max_health))
        self.manager.update(time_delta)

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for i, uib in enumerate(self.uibuttons):
                if event.ui_element == uib:
                    self.buttons[i].callback_func(i)
        self.manager.process_events(event)

    def draw(self, surface):
        self.manager.draw_ui(surface)
