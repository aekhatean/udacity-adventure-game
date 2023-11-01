from utils import (
    attack,
    clear_screen,
    get_player_choice,
    get_legendary_weapon,
    give_puzzle,
    highlight,
    impact_score,
    tell
)


# CONSTANTS: actions and how much score a user can gain by doing them
MOVEMENT_SCORE = 5
SOLVE_PUZZLE = 10
SUCCESSFUL_ATTACK = 20

# CONSTANTS: actions and how much score a user can lose by doing them
RUN_AWAY = -5


def field_scene(antagonist: dict[str, int],
                weapon: dict[str, int], total_score: int = 0,
                from_some_where: int = False) -> tuple[int, str]:
    """
    - First scene/location of the game, where the player hears about the
    antagonist for the first time, and a plave the player usually frequents to
    often as he/she navigates the game.
    - From this location, a player can either go to the house, or the cave.

    :param antagonist: dictionary contains antagonist 'name' & 'health' points
    :param weapon: dictionary contains weapon 'name' & 'damage' points
    :param total_score: player's current total score
    :param from_some_where: to tell whether a player just entered the game or
    came from another scene

    :return:
        - total_score - player's current score at the end of the scene
        - player_choice - player's choice where to go after
    """
    scene_tale = (
        "You find yourself standing in an open field,",
        "filled with grass and yellow wildflowers.",
        f"Rumor has it that a {antagonist['name']} is somewhere around here,",
        "and has been terrifying the nearby village.",
        "In front of you is a house.",
        "To your right is a dark cave.",
        "In your hand you hold your trusty (but not very effective) "
        + f"{weapon['name']}."
    )

    if from_some_where:
        scene_tale = (
            "You find yourself standing in an open field,",
        )

    scene_choices = (
        f"> Enter {highlight(1)} to knock on the door of the house.",
        f"> Enter {highlight(2)} to peer into the cave.",
    )

    tell(scene_tale)
    player_choice = get_player_choice(scene_choices)

    total_score = impact_score(total_score, MOVEMENT_SCORE)

    clear_screen()
    return total_score, player_choice


def house_scene(antagonist: dict[str, int], weapon: dict[str, int],
                total_score: int = 0) -> tuple[int, str, str]:
    """
    - This scene/ location where the player actually meets the antagonist,
    and choose whether to attack it or run away.
    - This is the only scene where a player can win or lose, by attacking
    the antagonist.

    :param antagonist: dictionary contains antagonist 'name' & 'health' points
    :param weapon: dictionary contains weapon 'name' & 'damage' points
    :param total_score: player's current total score

    :return:
        - total_score - player's current score at the end of the scene
        - player_choice - player's choice where to go after
        - termination_status - whether the player won or lost the battle
    """
    scene_tale = (
        "You approach the door of the house.",
        "You are about to knock when the door opens and out steps a"
        + f" {antagonist['name']}.",
        f"Eep! This is the {antagonist['name']}'s house!",
        f"The {antagonist['name']} finds you!",
        "Would you like to:",
    )
    scene_choices = (
        f"> {highlight('(1)')} Attack",
        f"> {highlight('(2)')} run away?"
    )
    tell(scene_tale)
    player_choice = get_player_choice(scene_choices)
    if player_choice == "1":
        attack_score = attack(weapon, antagonist)
        total_score = impact_score(total_score, attack_score)
        if attack_score >= 0 and total_score > 0:
            termination_status = "You won!"
        else:
            termination_status = "You lost!"
    else:
        total_score = impact_score(total_score, RUN_AWAY)
        termination_status = ""

    return total_score, player_choice, termination_status


def cave_scene(weapon: dict[str, int],
               total_score: int = 0) -> tuple[int, dict[str, int]]:
    """
    In this scence/location, a player has the chance to upgrade his/her
    weapon by successfully solving the puzzle given by the genie.

    :param weapon: dictionary contains weapon 'name' & 'damage' points
    :param total_score: player's current total score

    :return:
        - weapon - weapon defination dict containing {name, damage points}
        - total_score - player's current score at the end of the scene
    """
    pre_puzzle_scene_tale = (
        "You peer cautiously into the cave.",
        "you find a genie",
        "the genie gives you a ridle that reads:"
    )
    legendary_weapon = get_legendary_weapon()
    post_puzzle_scene_tale_puzzle_solved = (
        "It turns out to be only a very small cave.",
        "Your eye catches a glint of metal behind a rock.",
        f"You have found {legendary_weapon['name']}!",
        f"You discard your rusty old {weapon['name']} and take the "
        + f"{legendary_weapon['name']} with you.",
        "You walk back out to the field.",
    )
    post_puzzle_scene_tale_puzzle_not_solved = (
        "It turns out to be only a very small cave.",
        "Your eye catches a glint of metal behind a rock.",
        "But, it turns out to be a broken car wheel.",
        "You walk back out to the field.",
    )

    tell(pre_puzzle_scene_tale)

    puzzle_answered_correctly = give_puzzle()
    if puzzle_answered_correctly:
        weapon = legendary_weapon
        tell(post_puzzle_scene_tale_puzzle_solved)
        total_score = impact_score(total_score, SOLVE_PUZZLE)
    else:
        tell(post_puzzle_scene_tale_puzzle_not_solved)

    return total_score, weapon
