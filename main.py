import os
import time

from collections import defaultdict
from random import randint
from typing import List, Optional

import getch
from prettytable import DOUBLE_BORDER, PrettyTable

MAX_COMBO_LEN = 5
DEFAULT_SEQUENCE_LEN = 150

LEVEL_1 = ["j", "f"]
LEVEL_2 = LEVEL_1 + ["k", "d"]
LEVEL_3 = LEVEL_2 + ["l", "s"]
LEVEL_4 = LEVEL_3 + [";", "a"]
LEVEL_5 = LEVEL_4 + ["g", "h"]
LEVEL_6 = LEVEL_5 + ["b", "n"]
LEVEL_7 = LEVEL_6 + ["v", "c"]
LEVEL_8 = LEVEL_7 + ["x", "z"]
LEVEL_9 = LEVEL_8 + ["m", ",", "."]

LEVEL_MAP = {
    1: LEVEL_1,
    2: LEVEL_2,
    3: LEVEL_3,
    4: LEVEL_4,
    5: LEVEL_5,
    6: LEVEL_6,
    7: LEVEL_7,
    8: LEVEL_8,
    9: LEVEL_9,
}


class TermColour:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def generate_level(level: List[str], len_: Optional[int] = DEFAULT_SEQUENCE_LEN) -> str:
    i = len_
    final_sequence = ""
    while i > 0:
        sequence_length = randint(2, MAX_COMBO_LEN)
        sequence = [level[randint(0, len(level) - 1)] for _ in range(sequence_length)]
        # Don't add leading spaces
        if i == len_:
            final_sequence += "".join(sequence)
        else:
            final_sequence += f" {''.join(sequence)}"
        i -= sequence_length
    return final_sequence


def clear_screen() -> None:
    os.system("clear")


def display_mistakes(mistakes: dict) -> None:
    if not mistakes:
        print(
            TermColour.OKGREEN
            + "Congrats! You completed the level with no mistakes: that's awesome! ✨💖"
            + TermColour.ENDC
        )
        return
    table = PrettyTable()
    table.field_names = ["Character", "Mistakes"]
    for char, mistake_count in mistakes.items():
        if char == " ":
            # It's not very informative to display an empty space here...
            char = "<Space>"
        table.add_row([char, mistake_count])
    table.set_style(DOUBLE_BORDER)
    print(table)


def display_words_per_minute(words: int, time_taken: float) -> None:
    words_per_minute = words / time_taken * 60  # Time taken is in seconds
    table = PrettyTable()
    table.field_names = ["Words", "Time taken (s)", "Words per minute"]
    table.add_row(
        [
            words,
            f"{time_taken:.2f}",
            TermColour.OKGREEN + f"{words_per_minute:.2f}" + TermColour.ENDC,
        ]
    )
    table.set_style(DOUBLE_BORDER)
    print(table)


def display_accuracy(mistakes: dict, total_chars: int) -> None:
    total_mistakes = sum(mistakes.values())
    accuracy = (1 - total_mistakes / total_chars) * 100
    table = PrettyTable()
    table.field_names = ["Total characters", "Total mistakes", "Accuracy"]
    table.add_row(
        [
            total_chars,
            total_mistakes,
            TermColour.OKGREEN + f"{int(accuracy)}%" + TermColour.ENDC,
        ]
    )
    table.set_style(DOUBLE_BORDER)
    print(table)


def main():
    level_str = input(
        "Please enter the level [1-9] you would like to play and press 'Enter': "
    )
    try:
        level = int(level_str)
    except ValueError:
        print("Please enter a valid level number between 1 and 9.")
        return
    level = LEVEL_MAP.get(level)
    characters_to_type = generate_level(level)
    i = 0
    num_words = len(characters_to_type.split(" "))
    current_char = characters_to_type[i]
    mistakes = defaultdict(int)
    start_time = time.time()
    while i < len(characters_to_type):
        colourised_level = (
            characters_to_type[:i]
            + TermColour.FAIL
            + characters_to_type[i]
            + TermColour.ENDC
            + TermColour.OKBLUE
            + characters_to_type[i + 1 :]
            + TermColour.ENDC
        )
        print(colourised_level)
        user_input = getch.getch()
        # Start timing as soon as we get user input
        # TODO: fix this.
        # start_time = time.time()
        while user_input != current_char:
            mistakes[current_char] += 1
            user_input = getch.getch()
        if user_input == current_char:
            if i == len(characters_to_type) - 1:
                break
            i += 1
            current_char = characters_to_type[i]
            clear_screen()  # TODO: The action of this is a bit 'jerky': consider a better way to clear the screen
    end_time = time.time()
    time_taken = end_time - start_time
    clear_screen()
    display_words_per_minute(num_words, time_taken)
    display_accuracy(mistakes, len(characters_to_type))
    display_mistakes(mistakes)


if __name__ == "__main__":
    main()
