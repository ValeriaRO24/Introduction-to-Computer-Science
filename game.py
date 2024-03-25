"""
Assignment 1: Meepo is You

=== CSC148 Winter 2021 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains the Game class and the main game application.
"""

from typing import Any, Type, Tuple, List, Sequence, Optional
import pygame
from settings import *
from stack import Stack
import actor


class Game:
    """
    Class representing the game.
    """
    size: Tuple[int, int]
    width: int
    height: int
    screen: Optional[pygame.Surface]
    x_tiles: int
    y_tiles: int
    tiles_number: Tuple[int, int]
    background: Optional[pygame.Surface]

    _actors: List[actor.Actor]
    _is: List[actor.Is]
    _running: bool
    _rules: List[str]
    _history: Stack

    player: Optional[actor.Actor]
    map_data: List[str]
    keys_pressed: Optional[Sequence[bool]]

    def __init__(self) -> None:
        """
        Initialize variables for this Class.
        """
        self.width, self.height = 0, 0
        self.size = (self.width, self.height)
        self.screen = None
        self.x_tiles, self.y_tiles = (0, 0)
        self.tiles_number = (self.x_tiles, self.y_tiles)
        self.background = None

        # TODO Task 1: complete the initializer of the Game class
        self._actors = []
        self._is = []
        self._running = True
        self._rules = []
        self._history = Stack()
        self.player = None
        self.map_data = []
        self.keys_pressed = None

    def load_map(self, path: str) -> None:
        """
        Reads a .txt file representing the map
        """
        with open(path, 'rt') as f:
            for line in f:
                self.map_data.append(line.strip())

        self.width = (len(self.map_data[0])) * TILESIZE
        self.height = len(self.map_data) * TILESIZE
        self.size = (self.width, self.height)
        self.x_tiles, self.y_tiles = len(self.map_data[0]), len(self.map_data)

        # center the window on the screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def new(self) -> None:
        """
        Initialize variables to be object on screen.
        """
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.image.load(
            "{}/backgroundBig.png".format(SPRITES_DIR)).convert_alpha()
        for col, tiles in enumerate(self.map_data):
            for row, tile in enumerate(tiles):
                if tile.isnumeric():
                    self._actors.append(
                        Game.get_character(CHARACTERS[tile])(row, col))
                elif tile in SUBJECTS:
                    self._actors.append(
                        actor.Subject(row, col, SUBJECTS[tile]))
                elif tile in ATTRIBUTES:
                    self._actors.append(
                        actor.Attribute(row, col, ATTRIBUTES[tile]))
                elif tile == 'I':
                    is_tile = actor.Is(row, col)
                    self._is.append(is_tile)
                    self._actors.append(is_tile)

    def get_actors(self) -> List[actor.Actor]:
        """
        Getter for the list of actors
        """
        return self._actors

    def get_running(self) -> bool:
        """
        Getter for _running
        """
        return self._running

    def get_rules(self) -> List[str]:
        """
        Getter for _rules
        """
        return self._rules

    def _draw(self) -> None:
        """
        Draws the screen, grid, and objects/players on the screen
        """
        self.screen.blit(self.background,
                         (((0.5 * self.width) - (0.5 * 1920),
                           (0.5 * self.height) - (0.5 * 1080))))
        for actor_ in self._actors:
            rect = pygame.Rect(actor_.x * TILESIZE,
                               actor_.y * TILESIZE, TILESIZE, TILESIZE)
            self.screen.blit(actor_.image, rect)

        # Blit the player at the end to make it above all other objects
        if self.player:
            rect = pygame.Rect(self.player.x * TILESIZE,
                               self.player.y * TILESIZE, TILESIZE, TILESIZE)
            self.screen.blit(self.player.image, rect)

        pygame.display.flip()

    def _events(self) -> None:
        """
        Event handling of the game window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            # Allows us to make each press count as 1 movement.
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed = pygame.key.get_pressed()
                ctrl_held = self.keys_pressed[pygame.K_LCTRL]

                # handle undo button and player movement here
                if event.key == pygame.K_z and ctrl_held:   # Ctrl-Z
                    self._undo()
                else:
                    if self.player is not None:
                        assert isinstance(self.player, actor.Character)
                        save = self._copy()
                        if self.player.player_move(self) \
                                and not self.win_or_lose():
                            self._history.push(save)

        return

    def win_or_lose(self) -> bool:
        """
        Check if the game has won or lost
        Returns True if the game is won or lost; otherwise return False
        """
        assert isinstance(self.player, actor.Character)
        for ac in self._actors:
            if isinstance(ac, actor.Character) \
                    and ac.x == self.player.x and ac.y == self.player.y:
                if ac.is_win():
                    self.win()
                    return True
                elif ac.is_lose():
                    self.lose(self.player)
                    return True
        return False

    def run(self) -> None:
        """
        Run the Game until it ends or player quits.
        """
        while self._running:
            pygame.time.wait(1000 // FPS)
            self._events()
            self._update()
            self._draw()

    def set_player(self, actor_: Optional[actor.Actor]) -> None:
        """
        Takes an actor and sets that actor to be the player
        """
        self.player = actor_

    def remove_player(self, actor_: actor.Actor) -> None:
        """
        Remove the given <actor> from the game's list of actors.
        """
        self._actors.remove(actor_)
        self.player = None

    def _update(self) -> None:
        """
        Check each "Is" tile to find what rules are added and which are removed
        if any, and handle them accordingly.
        """

        # TODO Task 3: Add code here to complete this method
        # What you need to do in this method:
        # - Get the lists of rules that need to be added to and remove from the
        #   current list of rules. Hint: use the update() method of the Is
        # - The player may change if the "isYou" rule is updated. Make sure set
        #   self.player correctly after you update the rules. Note that
        #   self.player could be None in some cases.
        # - Update self._rules to the new list of rules.

        all_actors = self.get_actors()
        self._is = []
        for item in all_actors:
            if type(item) == actor.Is:
                self._is.append(item)

        new_rules = []

        for item in self._is:
            top = (item.x, item.y - 1)
            bottom = (item.x, item.y + 1)
            right_coord = (item.x + 1, item.y)
            left_coord = (item.x - 1, item.y)

            up = self.get_actor(top[0], top[1])
            down = self.get_actor(bottom[0], bottom[1])
            left = self.get_actor(left_coord[0], left_coord[1])
            right = self.get_actor(right_coord[0], right_coord[1])

            rule = item.update(up, down, left, right)
            for x in rule:
                if x != "":
                    new_rules.append(x)

        for item in self._rules:
            if item not in new_rules:
                self._remove_rules_helper(all_actors, item)
                self._rules.remove(item)

        for item in new_rules:
            if item not in self._rules:
                self._add_rules_helper(all_actors, item)
                self._rules.append(item)

    def _add_rules_helper(self, actors: List[actor.Actor], rule: str):
        words = rule.split()
        att = []
        sub = words[1]

        for item in actors:
            if isinstance(item, actor.Character):
                if words[0] == "Meepo" and type(item) == actor.Meepo:
                    att = item
                if words[0] == "Wall" and type(item) == actor.Wall:
                    att = item
                if words[0] == "Rock" and type(item) == actor.Rock:
                    att = item
                if words[0] == "Flag" and type(item) == actor.Flag:
                    att = item
        if sub == "isPush":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.set_push()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.set_push()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.set_push()

            elif type(att) == actor.Meepo:
                att.set_push()

        if sub == "isStop":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.set_stop()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.set_stop()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.set_stop()

            elif type(att) == actor.Meepo:
                att.set_stop()

        if sub == "isYou":
            self.set_player(att)
            att.set_player()

        if sub == "isVictory":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.set_win()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.set_win()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.set_win()
            else:
                att.set_win()

        if sub == "isLose":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.set_lose()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.set_lose()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.set_lose()
            elif type(att) == actor.Meepo:
                att.set_lose()

    def _remove_rules_helper(self, actors: List[actor.Actor], rule: str):
        words = rule.split()
        att = actors[0]
        sub = words[1]

        for item in actors:
            if isinstance(item, actor.Character):
                if words[0] == "Meepo" and type(item) == actor.Meepo:
                    att = item
                if words[0] == "Wall" and type(item) == actor.Wall:
                    att = item
                if words[0] == "Rock" and type(item) == actor.Rock:
                    att = item
                if words[0] == "Flag" and type(item) == actor.Flag:
                    att = item

        if sub == "isPush":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.unset_push()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.unset_push()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.unset_push()
            elif type(att) == actor.Meepo:
                att.unset_push()

        if sub == "isStop":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.unset_stop()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.unset_stop()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.unset_stop()

            elif type(att) == actor.Meepo:
                att.unset_stop()

        if sub == "isYou":
            att.unset_player()
            self.player = None

        if sub == "isVictory":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.unset_win()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.unset_win()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.unset_win()

            elif type(att) == actor.Meepo:
                att.unset_win()

        if sub == "isLose":
            if type(att) == actor.Wall:
                for item in actors:
                    if type(item) == actor.Wall:
                        item.unset_lose()

            elif type(att) == actor.Rock:
                for item in actors:
                    if type(item) == actor.Rock:
                        item.unset_lose()

            elif type(att) == actor.Flag:
                for item in actors:
                    if type(item) == actor.Flag:
                        item.unset_lose()

            elif type(att) == actor.Meepo:
                att.unset_lose()


    @staticmethod
    def get_character(subject: str) -> Optional[Type[Any]]:
        """
        Takes a string, returns appropriate class representing that string
        """
        if subject == "Meepo":
            return actor.Meepo
        elif subject == "Wall":
            return actor.Wall
        elif subject == "Rock":
            return actor.Rock
        elif subject == "Flag":
            return actor.Flag
        elif subject == "Bush":
            return actor.Bush
        return None

    def _undo(self) -> None:
        """
        Returns the game to a previous state based on what is at the top of the
        _history stack.
        """
        # TODO Task 4: Implement this undo method.
        # You'll need to restore the previous state the game using the
        # self._history stack
        # Find the code that pushed onto the stack to understand better what
        # is in the stack.

        new_game = self._history.pop()
        actors = new_game.get_actors()

        self._actors = []
        self.player = None

        for item in actors:
            self._actors.append(item)

        self._rules = []

        for item in new_game._rules:
            self._rules.append(item)

        self.set_player(new_game.player)

    def _copy(self) -> 'Game':
        """
        Copies relevant attributes of the game onto a new instance of Game.
        Return new instance of game
        """
        game_copy = Game()
        actors = self.get_actors()

        for item in actors:
            game_copy._actors.append(item.copy())

        for item in game_copy._actors:
            if isinstance(item, actor.Character):
                if item._is_player:
                    game_copy.player = item

        for item in self._rules:
            game_copy._rules.append(item)

        for item in self._is:
            game_copy._is.append(item)

        temp = []

        while not self._history.is_empty():
            temp.append(self._history.pop())

        for i in range(len(temp) - 1, -1, -1):
            self._history.push(temp[i])
            game_copy._history.push(temp[i])

        return game_copy

    def get_actor(self, x: int, y: int) -> Optional[actor.Actor]:
        """
        Return the actor at the position x,y. If the slot is empty, Return None
        """
        for ac in self._actors:
            if ac.x == x and ac.y == y:
                return ac
        return None

    def win(self) -> None:
        """
        End the game and print win message.
        """
        self._running = False
        print("Congratulations, you won!")

    def lose(self, char: actor.Character) -> None:
        """
        Lose the game and print lose message
        """
        self.remove_player(char)
        print("You lost! But you can have it undone if undo is done :)")


if __name__ == "__main__":

    game = Game()
    # load_map public function
    game.load_map(MAP_PATH)
    game.new()
    game.run()




    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['settings', 'stack', 'actor', 'pygame']
    # })
