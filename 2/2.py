import json
import os
from enum import Enum
from typing import Tuple


class Color(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"

FONT_FILE = "font.json"

if os.path.exists(FONT_FILE):
    with open(FONT_FILE, "r", encoding="utf-8") as file:
        FONT = json.load(file)
else:
    raise FileNotFoundError(FONT_FILE)

class Printer:
    def __init__(self, color: Color, position: Tuple[int, int] | None = None, symbol: str = "*"):
        self.color = color
        self.symbol = symbol
        self.original_position = (0, 0)
        self.position = position or self.original_position

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Color.RESET.value, end="")

    @staticmethod
    def print(text: str, color: Color, position: Tuple[int, int] | None = None, symbol: str = "*"):
        Printer._render_text(text, color, position, symbol)

    def print_text(self, text: str):
        Printer._render_text(text, self.color, self.position, self.symbol)

    @staticmethod
    def _render_text(text: str, color: Color, position: Tuple[int, int], symbol: str = None):
        position = position or (0, 0)
        coordinate_settings = f"\033[{position[1]};{position[0]}H"
        print(color.value, end="")

        lines = ["" for _ in range(FONT['height'])]
        for char in text.upper():
            if char in FONT["symbols"]:
                char_pattern = FONT["symbols"][char].split("\n")
                for i, line in enumerate(char_pattern):
                    if symbol:
                        line = line.replace("*", symbol)
                    lines[i] += line + "  "

        for line in lines:
            print(coordinate_settings, line)
        print(Color.RESET.value, end="")


if __name__ == "__main__":
    print('AAAAAAAAAAA')

    Printer.print("HELLO", Color.RED)

    with Printer(Color.GREEN, (66, 12), "Z") as printer:
        printer.print_text("WORLD")
        printer.print_text("HALAMADRID")