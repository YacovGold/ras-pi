from RPLCD.i2c import CharLCD
from games.snake import Snake
from helpers.buttons import Buttons
from helpers.dal import Dal
from helpers.menu import Menu
from helpers.screen import Screen
from config import LCD_TYPE, LCD_ADDRESS, BUTTON_PINS, DB_PATH

lcd = CharLCD(LCD_TYPE, LCD_ADDRESS)
lcd.clear()

screen = Screen(lcd)
buttons = Buttons(left_pin=BUTTON_PINS['left_pin'],
                  right_pin=BUTTON_PINS['right_pin'],
                  up_pin=BUTTON_PINS['up_pin'],
                  down_pin=BUTTON_PINS['down_pin'])

mnu = Menu(screen, buttons)


snake = Snake(screen, buttons, mnu, Dal('snake', DB_PATH))

snake.start()
