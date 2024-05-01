from typing import Dict, Tuple
from RPLCD.i2c import CharLCD

from helpers.common import is_even

CHAR_FULL = 0
CHAR_EMPTY = 1
CHAR_HALF_UP = 2
CHAR_HALF_DOWN = 3
CHAR_ARROW_RIGHT = 4

e = 0b00000
f = 0b11111
full = (f,) * 8
empty = (e,) * 8
half_up = (f,) * 4 + (e,) * 4
half_down = (e,) * 4 + (f,) * 4


arrow_right = (
    0b00000,
    0b00100,
    0b00110,
    0b11111,
    0b00110,
    0b00100,
    0b00000,
    0b00000,
)


class Screen:
    def __init__(self, lcd: CharLCD):
        self._lcd = lcd
        self._patterns: Dict[Tuple[int, int], Tuple[int, int]] = {}

        self.width = 16
        self.height = 4

    def reset(self):
        self._lcd.clear()
        self._patterns.clear()

        self._lcd.create_char(CHAR_FULL, full)
        self._lcd.create_char(CHAR_EMPTY, empty)
        self._lcd.create_char(CHAR_HALF_UP, half_up)
        self._lcd.create_char(CHAR_HALF_DOWN, half_down)
        self._lcd.create_char(CHAR_ARROW_RIGHT, arrow_right)

    def fill_block(self, pos: Tuple[int, int]):
        self._validate(pos)

        x, y = pos

        if pos not in self._patterns:
            self._patterns[pos] = pos

        c = CHAR_HALF_UP if is_even(y) else CHAR_HALF_DOWN

        if is_even(y) and (x, y + 1) in self._patterns:
            c = CHAR_FULL

        if not is_even(y) and (x, y - 1) in self._patterns:
            c = CHAR_FULL

        self._lcd.cursor_pos = (y // 2, x)
        self._lcd.write_string(f"{chr(c)}")

    def clear_block(self, pos: Tuple[int, int]):
        self._validate(pos)

        x, y = pos

        if pos in self._patterns:
            del self._patterns[pos]

        c = CHAR_EMPTY

        if is_even(y) and (x, y + 1) in self._patterns:
            c = CHAR_HALF_DOWN

        if not is_even(y) and (x, y - 1) in self._patterns:
            c = CHAR_HALF_UP

        self._lcd.cursor_pos = (y // 2, x)
        self._lcd.write_string(f"{chr(c)}")

    def _validate(self, pos: Tuple[int, int]):
        x, y = pos

        if x >= self.width or x < 0:
            raise Exception(f"x: {x} must be between 0 and {self.width}")

        if y // 2 >= self.height or y < 0:
            raise Exception(f"x: {y} must be between 0 and {self.height}")

    def write(self, line1: str, line2: str = ''):
        self._lcd.clear()
        self._lcd.cursor_pos = (0, 0)
        self._lcd.write_string(line1)
        self._lcd.cursor_pos = (1, 0)
        self._lcd.write_string(line2)
