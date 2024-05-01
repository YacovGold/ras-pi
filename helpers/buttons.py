from gpiozero import Button
from typing import Callable
from config import DEFAULT_BOUNCE_TIME


class Buttons:
    def __init__(self, up_pin: int, down_pin: int, left_pin: int, right_pin: int):
        
        self.up_button = Button(up_pin, bounce_time=DEFAULT_BOUNCE_TIME)
        self.down_button = Button(down_pin, bounce_time=DEFAULT_BOUNCE_TIME)
        self.left_button = Button(left_pin, bounce_time=DEFAULT_BOUNCE_TIME)
        self.right_button = Button(right_pin, bounce_time=DEFAULT_BOUNCE_TIME)

    def on_up(self, callback: Callable[[], None]):
        self.up_button.when_pressed = callback

    def on_down(self, callback: Callable[[], None]):
        self.down_button.when_pressed = callback

    def on_left(self, callback: Callable[[], None]):
        self.left_button.when_pressed = callback

    def on_right(self, callback: Callable[[], None]):
        self.right_button.when_pressed = callback
