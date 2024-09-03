from dataclasses import dataclass
from typing import Callable

import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UIButton, UILabel


@dataclass
class Button:
    name: str
    callback_func: Callable


class GUI:
    def __init__(self, max_button_count):
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
        self.manager = pygame_gui.UIManager(screen.size)
        self.unit_panel = UIPanel(
            pygame.Rect(0, 0, screen.width, screen.width / self.max_button_count),
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
        left_panel = UIPanel(relative_rect=pygame.Rect(0, screen.height - 100, 200, 100),
                             starting_height=4,
                             manager=self.manager)

        right_panel = (UIPanel(relative_rect=pygame.Rect(screen.width-200, screen.height - 100, 200, 100),
                               starting_height=4,
                               manager=self.manager))

        # Создание текстовых меток
        self.left_label = UILabel(relative_rect=pygame.Rect(10, 10, 200, 30),
                text='Монеты: 0',
                manager=self.manager,
                container=left_panel)

        self.right_label = UILabel(relative_rect=pygame.Rect(10, 10, 200, 30),
                text='Монеты: 0',
                manager=self.manager,
                container=right_panel)

    def update(self, time_delta, left_coins, right_coins):
        self.left_label.set_text(f"Монеты: {left_coins}")
        self.right_label.set_text(f"Монеты: {right_coins}")
        self.manager.update(time_delta)

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for i, uib in enumerate(self.uibuttons):
                if event.ui_element == uib:
                    self.buttons[i].callback_func(i)
        self.manager.process_events(event)

    def draw(self, surface):
        self.manager.draw_ui(surface)
