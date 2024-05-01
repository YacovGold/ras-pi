from enum import Enum, auto
from typing import Tuple
from games.base import Base
from collections import deque
from helpers.buttons import Buttons
from helpers.common import *
from helpers.dal import Dal
from helpers.menu import Menu
from helpers.screen import Screen
import random
import time


class Config:
    BEST_SCORE_DB_KEY = 'best_score'
    LEVEL_DB_KEY = 'level'
    ALLOW_OVERFLOW_DB_KEY = 'allow_overflow'
    LEVEL_MAP = {
        1: 0.8,
        2: 0.6,
        3: 0.5,
        4: 0.4,
        5: 0.3,
        6: 0.2,
        7: 0.1,
        8: 0.09,
        9: 0.08,
        10: 0.07,
        11: 0.06,
        12: 0.05,
        13: 0.04,
    }


class Snake(Base):
    def __init__(self, screen: Screen, buttons: Buttons, mnu: Menu, dal: Dal):
        super().__init__()
        self._screen = screen
        self._buttons = buttons
        self._mnu = mnu
        self._dal = dal
        self._config = Config()

    def start(self):
        self.best_score = int(self._dal.get_val(self._config.BEST_SCORE_DB_KEY, '0'))
        self.level = int(self._dal.get_val(self._config.LEVEL_DB_KEY, '5'))
        self.allow_overflow = bool(self._dal.get_val(self._config.ALLOW_OVERFLOW_DB_KEY, 'True'))

        while True:
            menu_sel = self._mnu.show_menu(['Start Game', 'Select Level', 'Allow Overflow'])

            if menu_sel == 0:
                self._init()
                self._start()
            elif menu_sel == 1:
                menu_sel = self._mnu.show_menu(
                    [f'Level {n + 1}' for n in range(len(self._config.LEVEL_MAP))], self.level)
                if menu_sel != -1:
                    self.level = menu_sel
                    self._dal.set_val(self._config.LEVEL_DB_KEY, str(self.level))
            elif menu_sel == 2:
                menu_sel = self._mnu.show_menu(['Yes', 'No'], 0 if self.allow_overflow else 1)
                if menu_sel != -1:
                    self.allow_overflow = menu_sel == 0
                    self._dal.set_val(self._config.ALLOW_OVERFLOW_DB_KEY, 'True' if menu_sel == 0 else 'False')
            else:
                break

    def _start(self):
        score = 0

        while True:
            time.sleep(self._config.LEVEL_MAP[self.level])

            new = self._calc_next_pos(self._snake[-1])

            if new == self.food_pos:
                self._place_food()
                self._left_to_grow += 2
                score += self.level

            x, y = new
            if new in self._snake or x < 0 or x >= self._screen.width or y < 0 or y >= self._screen.height:
                if score > self.best_score:
                    self._dal.set_val(self._config.BEST_SCORE_DB_KEY, str(score))
                    self.best_score = score
                show_game_over(self._buttons, self._screen, f':(  Score: {score}', f'Best Score: {self.best_score}')
                return

            self._snake.append(new)
            self._screen.fill_block(new)

            if self._left_to_grow == 0:
                to_clear = self._snake.popleft()
                self._screen.clear_block(to_clear)
            else:
                self._left_to_grow -= 1

    def _init(self):
        self._screen.reset()

        self._left_to_grow = 0
        self._dir = Direction.RIGHT

        self._buttons.on_right(lambda: self._set_dir(Direction.RIGHT))
        self._buttons.on_left(lambda: self._set_dir(Direction.LEFT))
        self._buttons.on_up(lambda: self._set_dir(Direction.UP))
        self._buttons.on_down(lambda: self._set_dir(Direction.DOWN))

        self._snake = deque()
        spx = self._screen.width // 2 - 2  # Start position x
        spy = self._screen.height // 2 - 1  # Start position y
        self._snake.extend([(spx - 2, spy), (spx - 1, spy), (spx, spy)])

        for p in self._snake:
            self._screen.fill_block(p)

        self._place_food()

    def _set_dir(self, new_dir: str):
        orig_dir = self._dir
        self._dir = new_dir
        cur_pos = self._snake[-1]
        next_pos = self._calc_next_pos(cur_pos)

        if next_pos == self._snake[-2]:
            self._dir = orig_dir

    def _calc_next_pos(self, cur: Tuple[int, int]):
        x, y = cur

        if self._dir == Direction.RIGHT:
            x += 1

        if self._dir == Direction.LEFT:
            x -= 1

        if self._dir == Direction.UP:
            y -= 1

        if self._dir == Direction.DOWN:
            y += 1

        if self.allow_overflow:
            if x >= self._screen.width:
                x = 0
            if x < 0:
                x = self._screen.width - 1

            if y >= self._screen.height:
                y = 0
            if y < 0:
                y = self._screen.height - 1

        return (x, y)

    def _place_food(self):
        available_positions = [(x, y) for x in range(self._screen.width) for y in range(self._screen.height)]
        available_positions = [p for p in available_positions if p not in self._snake]
        self.food_pos = random.choice(available_positions)
        self._screen.fill_block(self.food_pos)
