import time
from typing import List
from helpers.buttons import Buttons
from helpers.screen import CHAR_ARROW_RIGHT, Screen
from helpers.common import *


class Menu:
    def __init__(self, screen: Screen, buttons: Buttons):
        self._screen = screen
        self._buttons = buttons

    def show_menu(self, items: List[str], selected_index: int = 0):
        self._btn = ''

        self._screen.reset()

        self._buttons.on_right(lambda: self._set_btn(Direction.RIGHT))
        self._buttons.on_left(lambda: self._set_btn(Direction.LEFT))
        self._buttons.on_up(lambda: self._set_btn(Direction.UP))
        self._buttons.on_down(lambda: self._set_btn(Direction.DOWN))

        needs_redraw = True

        while True:
            if needs_redraw:
                first_line = f"{chr(CHAR_ARROW_RIGHT)}{items[selected_index]}"
                second_line = items[selected_index + 1] if selected_index + 1 < len(items) else ''
                self._screen.write(first_line, second_line)
                needs_redraw = False

            time.sleep(0.05)

            if self._btn == Direction.RIGHT:
                return selected_index

            if self._btn == Direction.LEFT:
                return -1

            if self._btn == Direction.DOWN:
                if selected_index == len(items) - 1:
                    selected_index = -1
                needs_redraw = True
                selected_index += 1

            if self._btn == Direction.UP:
                if selected_index == 0:
                    selected_index = len(items)
                needs_redraw = True
                selected_index -= 1

            self._btn = ''

    def _set_btn(self, btn: str):
        self._btn = btn
