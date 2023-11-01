import random
from typing import Optional

from scences import (
    cave_scene,
    field_scene,
    house_scene,
)
from utils import clear_screen, highlight, mark


def play(antagonist: Optional[int] = None, weapon: Optional[int] = None,
         total_score: int = 0, from_some_where: int = False) -> None:
    """
    This function is what starts the game.
    It also facilitates transfaring state from one scene to the other
    and enables naviagating to different locations.

    :param antagonist: dictionary contains antagonist 'name' & 'health' points
    :param weapon: dictionary contains weapon 'name' & 'damage' points
    :param total_score: player's current total score
    :param from_some_where: to tell whether a player just entered the game or
    came from another scene

    :return: None
    """
    # Dictionary of antagonists and their health points
    possible_antagonists = [
        {"name": "troll", "health": 20},
        {"name": "dragon", "health":  20},
        {"name": "ghoul", "health": 20},
        {"name": "theif", "health": 10},
    ]

    # Dictionary of weapons and their damage points
    possible_regular_weapons = [
        {"name": "dager", "damage": 10},
        {"name": "magic wand", "damage": 10},
        {"name": "baseball bat", "damage": 10},
    ]

    # If a player just started the game, randomly pick an antagonist.
    if not antagonist:
        antagonist = random.choice(possible_antagonists)

    # If a player just started the game, randomly pick a weapon.
    if not weapon:
        weapon = random.choice(possible_regular_weapons)

    # If the player was coming from another scene, clean terminal.
    clear_screen()

    total_score, player_choice = field_scene(
        antagonist, weapon, total_score, from_some_where)

    if player_choice == "1":
        total_score, player_choice, termination_status = house_scene(
            antagonist, weapon, total_score)

        if player_choice == "1":
            play_again(termination_status, total_score)
        else:
            play(antagonist, weapon, total_score, from_some_where=True)
    else:
        total_score, weapon = cave_scene(weapon, total_score)
        play(antagonist, weapon, total_score, from_some_where=True)


def play_again(termination_status: str, total_score: int) -> None:
    """
    - The game came to an end? this is where we tell the player
    whether he/she won or lost.
    - And also give them the chance to play again.

    :param termination_status: whether the player won or lost
    :param total_score: player's final score

    :return: None
    """
    clear_screen()
    print(mark(termination_status))
    print(f"Your total score is: {highlight(total_score)}")

    response = input("Would you like to play again? (y/n)\n")
    while response not in ("y", "n"):
        response = input("valid answer are the letters y or n:\n")

    if response == "y":
        play()


if __name__ == "__main__":
    play()
