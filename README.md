# Snake Game on Raspberry Pi

Snake game designed for Raspberry Pi! This project is implemented in Python and configured to work seamlessly with a 1602A LCD display and button-based control system.

[![Demo](/assets/rp-snake-thumbnail.jpg)](https://1drv.ms/v/s!Ag8izxa0g_0ej6ozPLPs9AAwhZjq5Q?e=o413TW "Demo")

## Hardware Requirements

- **Raspberry Pi**: The main platform for running the game.
- **1602A LCD Display**: Displays game information.
- **4 Buttons**: For gameplay control, linked to GPIO pins.

## Setup Instructions

1. **Clone the repository**: Obtain the source code.
2. **Install dependencies**: Run `pip install -r requirements.txt` to install required Python packages. Use `--break-system-packages` if needed.
3. **LCD Display Setup**: Connect the LCD display to your Raspberry Pi following the manufacturer's instructions, noting the I2C address.
4. **Button Configuration**: Attach buttons to the designated GPIO pins on your Raspberry Pi. Modify the `BUTTON_PINS` in the `config.py` file according to your setup.

## Configuration

Configure the game by adjusting settings in the `config.py` file:

- **BUTTON_PINS**: Assignments for the GPIO pins connected to the buttons.
- **DEFAULT_BOUNCE_TIME**: Debounce time for button presses.
- **DB_PATH**: Database path for storing game settings and high scores.
- **LCD_TYPE**: Type of the connected LCD display.
- **LCD_ADDRESS**: I2C address of the LCD display.

## Usage

To start the game, execute:

> python starter.py

## Menu Interactions

Use the following button-controlled actions to interact with the LCD menu:

- **Start Game**: Initiates a new game session.
- **Select Level**: Allows selection of difficulty level.
- **Allow Overflow**: Enables or disables the snake's ability to traverse screen edges.

## Game Mechanics

Control the snake to consume food while avoiding collisions with walls or itself, as dictated by the 'Allow Overflow' setting. The game ends if the snake encounters a wall or itself, with the LCD displaying the current score alongside the highest recorded score.

## Project Structure

- **starter.py**: Main entry point for launching the game.
- **config.py**: Stores configuration settings for the game.
- **games/base.py**: Abstract base class for all games.
- **games/snake.py**: Implementation specific to the Snake game.
- **helpers/buttons.py**: Handles button input logic.
- **helpers/common.py**: Contains utility functions and enums.
- **helpers/dal.py**: Acts as the data access layer for storing settings and scores.
- **helpers/menu.py**: Responsible for game menu management and navigation.
- **helpers/screen.py**: Handles LCD screen interactions and simulates extra display rows.