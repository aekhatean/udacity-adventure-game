import time
import random
import os


def attack(weapon: dict[str, int], antagonist: dict[str, int]) -> int:
    """
    Attack the antagonist using the weapon currently help by the player

    If the weapon has damage points that match antagonist's health points
    or exceeds them, then the player can defeat the antagonist,
    otherwise the player loses score equal to
    [antagonist health points] - [weapon damage points]

    :param weapon: dictionary contains weapon 'name' & 'damage' points
    :param antagonist: dictionary contains antagonit 'name' & 'health' points

    :return: [antagonist health points] - [weapon damage points]

    """
    attack_score = weapon["damage"] - antagonist["health"]

    successful_attack_scene = (
        f"As the {antagonist['name']} moves to attack you, ",
        f"you raise your new {weapon['name']}.",
        f"The {weapon['name']} shines brightly in your hand as you "
        + "brace yourself for the attack.",
        f"But the {antagonist['name']} takes one look at your shiny new "
        + f"{weapon['name']} and runs away!",
        f"You have rid the town of the {antagonist['name']}. "
        + "You are victorious!",
    )
    failed_attack_scene = (
        "You do your best...",
        f"but your rusty old {weapon['name']} is no match for the "
        + f"{antagonist['name']}. You have been defeated!"
    )

    if attack_score < 0:
        tell(failed_attack_scene)
    else:
        tell(successful_attack_scene)

    return attack_score


def tell(tale: tuple[str]) -> None:
    """
    A function that takes a tuple of transcript lines of a game
    scene, and prints it to the player line by line.

    :param tale: list of transcript lines

    :return: None
    """
    for sentence in tale:
        delay_print(sentence)


def delay_print(sentence: str) -> None:
    """
    A function that prints a sentence then pauses for 2 seconds.

    :param sentence: to be printed

    :return: None
    """
    print(sentence)
    time.sleep(2)


def highlight(text: str) -> str:
    """
    Wraps the text in -bash- shell code to give it
    green foreground when printed in the terminal.

    :param text: to be highlighted

    :return: the text after being highlighted
    """
    return f"\033[92m{text}\033[0m"


def mark(text: str) -> str:
    """
    Wraps the text in -bash- shell code to give it
    black foreground, and yellow background when printed in the terminal.

    :param text: to be marked

    :return: the text after being highlighted
    """
    return f"\033[103m\033[30m{text}\033[0m\033[0m"


def get_player_choice(scene_choices: tuple[str]) -> str:
    """
    Takes a tuple of choices give to a player in a scene,
    and prints it out in the terminal, the prompts the player
    for his/her choice.

    :param scence_choices: which player can pick from

    :return: None
    """
    tell(scene_choices)
    highest_number = len(scene_choices)
    player_choice = input(
        "What would you like to do? (Please enter a number):\n")

    valid_options = [str(option) for option in range(1, highest_number + 1)]
    while player_choice not in valid_options:
        player_choice = input(
            "Valid choices are the numbers between "
            + f"{highlight(1)} and {highlight(highest_number)} only:\n")

    return player_choice


def clear_screen() -> None:
    """
    Clears the terminal content

    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def give_puzzle() -> bool:
    """
    Gives a player a random puzzle, and returns a boolean
    that is True if the puzzle was solved correctly and False otherwise.

    :return: whether the player solved the puzzle
    """
    puzzles = [
        {
            "question": "What is the third month of year?",
            "choices": [
                "1. March.",
                "2. June.",
                "3. October."
            ],
            "answer": "1"
        },
        {
            "question": "How many fingers in a hand?",
            "choices": [
                "1. 5 fingers.",
                "2. 4 fingers, and a thumb.",
                "3. 5 toes"
            ],
            "answer": "2"
        },
        {
            "question": "How many minutes in an hour?",
            "choices": [
                "1. 60",
                "2. 100",
                "3. 13"
            ],
            "answer": "1"
        },
    ]
    puzzle = random.choice(puzzles)
    delay_print(puzzle["question"])
    player_answer = get_player_choice(puzzle["choices"])

    return player_answer == puzzle["answer"]


def get_legendary_weapon() -> dict[str, int]:
    """
    Picks randomly one of the most powerful weapons
    in the game.

    :return: weapon defination dict containing {name, damage points}
    """
    return random.choice([
        {"name": "golden dager", "damage": 50},
        {"name": "the magical Wand of Ogoroth", "damage": 75},
        {"name": "egyptian sword", "damage": 100},
    ])


def impact_score(total_score: int, *actions_score: list[int]) -> int:
    """
    a function that modifies the total score depending on an action
    that the player took (ie. solved a puzzle, ran away,
    or attacked the antagonist).
    and then prints that score to the user.

    :param total_score: player's current total score
    :param actions_score: score(s) of action or combination of actions
    that a player made

    :return: new total score after player's action
    """
    for action_score in actions_score:
        total_score += action_score
    clear_screen()
    delay_print(f"{mark('Your current total score is:')} "
                + f"{highlight(total_score)}")
    return total_score
