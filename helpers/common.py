from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from helpers.buttons import Buttons
    from helpers.screen import Screen


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


def is_even(num: int):
    return num % 2 == 0


def show_game_over(buttons: Buttons, screen: Screen, line1: str = 'Game Over', line2: str = ''):
    screen.reset()
    screen.write(line1, line2)
    time.sleep(0.5)

    is_btn_click = [False]

    def btn_click():
        is_btn_click[0] = True

    for button in [buttons.on_right, buttons.on_left, buttons.on_up, buttons.on_down]:
        button(btn_click)

    while not is_btn_click[0]:
        time.sleep(0.03)
