from game import *
from actor import *
import pytest
import pygame
import os

# USE PYGAME VARIABLES INSTEAD
keys_pressed = [0] * 323

# Setting key constants because of issue on devices
pygame.K_RIGHT = 1
pygame.K_DOWN = 2
pygame.K_LEFT = 3
pygame.K_UP = 4
pygame.K_LCTRIL = 5
pygame.K_z = 6
RIGHT = pygame.K_RIGHT
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
UP = pygame.K_UP
CTRL = pygame.K_LCTRL
Z = pygame.K_z


def setup_map(map: str) -> 'Game':
    """Returns a game with map1"""
    game = Game()
    game.new()
    game.load_map(os.path.abspath(os.getcwd()) + '/maps/' + map)
    game.new()
    game._update()
    game.keys_pressed = keys_pressed
    return game


def set_keys(up, down, left, right, CTRL=0, Z=0):
    keys_pressed[pygame.K_UP] = up
    keys_pressed[pygame.K_DOWN] = down
    keys_pressed[pygame.K_LEFT] = left
    keys_pressed[pygame.K_RIGHT] = right


def test1_move_player_up():
    """
    Check if player is moved up correctly
    """
    game = setup_map("student_map1.txt")
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)

    assert result == True
    assert game.player.y == 1


def test2_move_player_down():
    """
    Check if player is moved down correctly
    """
    game = setup_map("student_map1.txt")

    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    assert result == True
    set_keys(0, 1, 0, 0)

    result = game.player.player_move(game)
    assert result == True
    assert game.player.y == 2


def test3_move_player_left():
    """
    Check if player is moved left correctly
    """
    game = setup_map("student_map1.txt")
    print(game.player.x)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    print(game.player.x)
    assert result == True
    assert game.player.x == 5


def test4_move_player_right():
    """
    Check if player is moved left correctly
    """
    game = setup_map("student_map2.txt")
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    assert result == True
    assert game.player.x == 3


def test5_check_bounderies_top_left():
    """
    Check if player is not allowed to leave bouderies for both top and left
    for bush
    """
    game = setup_map("student_map4.txt")
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    assert result == False

    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    assert result == False


def test6_check_bounderies_top_left():
    """
    Check if player is not allowed to leave bouderies for both top and left
    for bush
    """
    game = setup_map("student_map1.txt")
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    assert result == False

    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    assert result == False


def test7_push_block():
    """
    Check if player pushes block correctly
    """
    game = setup_map("student_map2.txt")
    set_keys(0, 0, 0, 1)
    wall = \
    [i for i in game._actors if isinstance(i, Block) and i.word == "Wall"][0]
    result = game.player.player_move(game)
    assert result == True
    assert game.player.x == 3
    assert wall.x == 4


def test8_create_rule_wall_is_push():
    """
    Check if player creates wall is push rule correctly
    """
    game = setup_map("student_map2.txt")
    set_keys(0, 0, 0, 1)
    wall = \
    [i for i in game._actors if isinstance(i, Block) and i.word == "Wall"][0]
    result = game.player.player_move(game)
    game._update()
    assert game._rules[1] == "Wall isPush"
    assert game.player.x == 3
    assert wall.x == 4


def test_9_follow_rule_wall_is_push():
    """
    Check if player follows rules correctly
    """
    game = setup_map("student_map3.txt")
    set_keys(0, 0, 0, 1)
    wall_object = game._actors[game._actors.index(game.player) + 1]
    result = game.player.player_move(game)
    assert game.player.x == 2
    assert wall_object.x == 3


def test_10_no_push():
    """
    Check if player is not able to push because of rule not existing
    """
    game = setup_map("student_map4.txt")
    set_keys(0, 0, 0, 1)
    wall_object = game._actors[game._actors.index(game.player) + 1]
    result = game.player.player_move(game)
    assert game.player.x == 2
    assert wall_object.x == 2


def test_11_yes_push():
    """
    Check if player is able to push once the rule is made on rock
    """
    game = setup_map("student_map4.txt")
    set_keys(0, 0, 0, 1)
    wall_object = game._actors[game._actors.index(game.player) + 1]
    result = game.player.player_move(game)
    result = game.player.player_move(game)
    result = game.player.player_move(game)
    assert game.player.x == 4
    assert wall_object.x == 2
    game._update()
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    result = game.player.player_move(game)

    assert game.player.x == 2
    assert wall_object.x == 1


def test_12_player_change():
    """
    Check if player is able to change into another character
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(11):
        result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    game._update()
    assert isinstance(game.player, actor.Rock) == True


def test_13_lose_rule():
    """
    Check if the game correctly sets the rule lose
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(3):
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    game._update()

    assert ("Wall isLose" in game._rules) is True


def test_14_game_lose():
    """
    Check if the game will lose when player touches Wall if set to lose
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(3):
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    game._update()

    assert ("Wall isLose" in game._rules) is True
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)

    set_keys(0, 1, 0, 0)
    for i in range(3):
        result = game.player.player_move(game)
    game.win_or_lose()
    assert game.player is None


def test_15_stop_rule():
    """
    Check if the rule stop is applied properly, and that player can't move if
    the object before it is stop
    """
    game = setup_map("student_map5.txt")
    game._update()

    assert ("Rock isStop" in game._rules) is True
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    assert result is False


def test_16_remove_rule():
    """
    Check if the rule is added and then removed from game
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)

    set_keys(0, 1, 0, 0)
    for i in range(3):
        result = game.player.player_move(game)

    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    game._update()
    assert ("Wall isLose" in game._rules) is True

    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    game._update()
    assert ("Wall isLose" in game._rules) is False


def test_17_victory_rule():
    """
    Check if game is able to apply the victory rule correctly, and game wins
    when object is interacted
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(3):
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(6):
        result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(2):
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    for i in range(2):
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    game._update()
    assert ("Wall isVictory" in game._rules) is True

    set_keys(0, 1, 0, 0)
    for i in range(2):
        result = game.player.player_move(game)

    game.win_or_lose()
    assert game._running == False


def test_18_Flag():
    """
    Check if game properly sets a rule with character flag and executes that rule
    correctly
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(3):
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    game._update()
    print(game.player.x, game.player.y)
    assert ("Flag isLose" in game._rules) is True
    set_keys(0, 0, 0, 1)
    for i in range(8):
        result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    game.win_or_lose()
    assert game.player is None


def test_19_Undo():
    """
    Check if game properly undoes a move
    """
    keys_pressed[pygame.K_z] = 1
    keys_pressed[pygame.K_LCTRIL] = 1
    game = setup_map("student_map3.txt")
    game._update()
    assert game.player.x == 1
    game._history.push(game._copy())
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    assert game.player.x == 2


    game._undo()

    assert game.player.x == 1


def test_20_overriding_rules():
    """
    Check if game properly takes two rules and preforms the correct one
    """
    game = setup_map("student_map5.txt")
    game._update()
    assert ("Rock isStop" in game._rules) is True
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    assert result is False

    set_keys(0, 0, 1, 0)
    for i in range(3):
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(10):
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    game._update()
    assert ("Rock isPush" in game._rules) is True

    set_keys(1, 0, 0, 0)
    for i in range(7):
        result = game.player.player_move(game)

    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    assert result is True


def test_21_removing_character():
    """
    Check if game properly removes the player rule block
    """
    game = setup_map("student_map5.txt")
    game._update()
    assert ("Meepo isYou" in game._rules) is True
    assert isinstance(game.player, actor.Meepo) is True

    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)

    set_keys(0, 1, 0, 0)
    for i in range(13):
        result = game.player.player_move(game)
    game._update()
    assert ("Meepo isYou" in game._rules) is False
    assert game.player is None


def test_22_bounderies_no_bush():
    """
    Check if the player doesn't go past the bounderies beyond bush
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 0, 1, 0)
    for i in range(4):
        result = game.player.player_move(game)

    set_keys(0, 1, 0, 0)
    for i in range(8):
        result = game.player.player_move(game)

    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    assert result is False


def test_23_push_item_past_bounderies():
    """
    Check if the player can't push item beyond the bounderies
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(10):
        result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    for i in range(2):
        result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    for i in range(4):
        result = game.player.player_move(game)

    x = game.player.x
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)

    assert x == game.player.x


def test_24_walk_through_wall():
    """
    Check if the player can walk through a wall when there is no
    rule that let's it push or make stop
    """
    game = setup_map("student_map3.txt")
    game._update()
    set_keys(0, 0, 0, 1)
    for i in range(3):
        result = game.player.player_move(game)

    set_keys(0, 1, 0, 0)
    for i in range(6):
        result = game.player.player_move(game)
    assert result is True


def test_25_make_game_copy():
    """
    Check if when a copy of game is made, there is no ailsing
    """
    game = setup_map("student_map1.txt")
    game._update()
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    game._events()
    game2 = game._copy()
    assert game != game2
    assert game.player != game2.player
    assert game.player.x == game2.player.x
    assert type(game.player) == type(game2.player)
    assert game._rules == game2._rules
    assert game._rules is not game2._rules
    assert game._is is not game2._is
    assert game._is == game2._is
    assert type(game2._history) is Stack
    assert game._actors != game2._actors
    assert len(game._actors) == len(game2._actors)


def test_26_game_copy_History():
    """
    Check if when a copy of game is made then the history stack is
    copied correctly
    """
    game = setup_map("student_map1.txt")
    game._update()
    game._history.push(1)
    game._history.push(2)
    game._history.push(3)
    game2 = game._copy()
    assert game._history.pop() == game2._history.pop()


def test_27_rule_undo():
    """
    Check if the game can undo a rule being made
    """
    game = setup_map("student_map5.txt")
    game._update()
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)

    set_keys(0, 0, 1, 0)
    for i in range(3):
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    for i in range(10):
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    for i in range(4):
        result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    game._history.push(game._copy())
    assert ("Rock isPush" in game._rules) is False
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    game._update()
    assert ("Rock isPush" in game._rules) is True
    game._undo()
    assert ("Rock isPush" in game._rules) is False


def test_28_is_colour_change():
    """
    Check if the is block image changes after a rule is called
    """
    game = setup_map("student_map2.txt")
    game._update()
    image = ''
    is_block = ''
    for item in game._is:
        if item.x == 5:
            image = item.image
            is_block = item

    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    game._update()
    assert image != is_block.image




if __name__ == "__main__":

    import pytest
    pytest.main(['student_tests.py'])

