"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

        <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as[ the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    # With the rule that there are at most 4 players
    copy = smart_players[:]
    goals = generate_goals(num_human + num_random + len(smart_players))
    players = []
    for index, goal in enumerate(goals):
        if num_human > 0:
            players.append(HumanPlayer(index, goal))
            num_human -= 1
        elif num_random > 0:
            players.append(RandomPlayer(index, goal))
            num_random -= 1
        else:
            players.append(SmartPlayer(index, goal, copy.pop(0)))
    return players


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    # Check if the cursor is inside the board and which quadrant it is in
    inside = True
    half_size = round(block.size / 2.0)
    horizontal_bisector = block.position[0] + half_size
    vertical_bisector = block.position[1] + half_size
    child_index = -1
    if (horizontal_bisector <= location[0] <
            block.position[0] + block.size) and \
            (vertical_bisector > location[1] >= block.position[1]):
        child_index = 0
    elif (block.position[0] <= location[0] < horizontal_bisector) and \
            (vertical_bisector > location[1] >= block.position[1]):
        child_index = 1
    elif (block.position[0] <= location[0] < horizontal_bisector) and \
            (block.position[1] + block.size > location[1] >=
             vertical_bisector):
        child_index = 2
    elif (horizontal_bisector <= location[0] <
          block.position[0] + block.size) and \
            (block.position[1] + block.size > location[1] >=
             vertical_bisector):
        child_index = 3
    else:
        inside = False
    # return the selected quadrant or block if found, otherwise return None
    if inside:
        if (not block.children) or level == 0:
            return block
        else:
            return _get_block(block.children[child_index], location, level - 1)
    else:
        return None


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """ Create a tuple such that the first index is the string from the first
    index of <action>, the second index is the item at the second index of
    <action>, and the third index is <block>.

    For illustration, the returned tuple is in the form:
        (<action>[0], <action>[1], <block>)
    """
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block int <board >that is currently selected by the player
         based on the position of the mouse on the screen and the player's
         desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


def _random_valid_move(player: Player, board: Block) -> Tuple[Tuple[str, int],
                                                              Tuple[int, int],
                                                              int]:
    """Returns a tuple consisting of a random valid action for a <player>
    at a random location on a random level within <board>.

    The first index is an action (represented by a tuple of 2 elements), the
    second index is another tuple representing the location where the action
    will be acted on, and the third index is an integer representing the level
    on which the action is acted on.

    This function does not mutate <board>.
    """
    valid = False
    possible_actions = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                        SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, COMBINE,
                        PAINT]
    while not valid:
        new_block = board.create_copy()
        rand_location = (random.randint(0, new_block.size - 1),
                         random.randint(0, new_block.size - 1))
        rand_level = random.randint(0, new_block.max_depth)
        rand_block = _get_block(new_block, rand_location, rand_level)
        rand_action = random.choice(possible_actions)
        if rand_block is not None:
            if rand_action == ROTATE_CLOCKWISE:
                valid = rand_block.rotate(1)
            elif rand_action == ROTATE_COUNTER_CLOCKWISE:
                valid = rand_block.rotate(3)
            elif rand_action == SWAP_HORIZONTAL:
                valid = rand_block.swap(0)
            elif rand_action == SWAP_VERTICAL:
                valid = rand_block.swap(1)
            elif rand_action == SMASH:
                valid = rand_block.smash()
            elif rand_action == COMBINE:
                valid = rand_block.combine()
            else:
                valid = rand_block.paint(player.goal.colour)
        if valid:
            return rand_action, rand_location, rand_level


class RandomPlayer(Player):
    """A player that plays randomly.
    """
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this RandomPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block on <board> that is currently selected by
        the RandomPlayer.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant mouse events made by the player based on
        the mapping in MOUSEBUTTONDOWN.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True
            print('clicked')

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        valid = _random_valid_move(self, board)

        self._proceed = False
        valid_block = _get_block(board, valid[1], valid[2])
        return _create_move(valid[0], valid_block)


class SmartPlayer(Player):
    """A player that plays by trying out a number of moves randomly,
    then plays the move that yields the highest score. Does not consider the
    costs of a move.

    Then number of moves the player tries is equal to the parameter
    <difficulty>.
    """
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    # _difficulty:
    #   An integer that represents the difficulty of this player
    #
    # == Representation Invariants concerning the private attributes ==
    #   _difficulty > 0

    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """Initialize this SmartPlayer with the given <renderer>, <player_id>,
        <goal> and <difficulty>.
        """
        Player.__init__(self, player_id, goal)
        self._difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block on <board> that is currently selected by
        the RandomPlayer.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant mouse events made by the player based on
            the mapping in MOUSEBUTTONDOWN.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("clicked \n")
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        score = self.goal.score(board)
        best_choice = (PASS, (0, 0), 0)
        for _ in range(self._difficulty):
            test_board = board.create_copy()
            valid = _random_valid_move(self, board)
            selected_block = _get_block(test_board, valid[1], valid[2])
            if valid[0][0] == 'rotate':
                selected_block.rotate(valid[0][1])
            elif valid[0][0] == 'swap':
                selected_block.swap(valid[0][1])
            elif valid[0][0] == 'smash':
                selected_block.smash()
            elif valid[0][0] == 'combine':
                selected_block.combine()
            else:
                selected_block.paint(self.goal.colour)
            if score < self.goal.score(test_board):
                score = self.goal.score(test_board)
                best_choice = valid
        if score == self.goal.score(board):
            best_choice = (PASS, best_choice[1], best_choice[2])

        self._proceed = False
        valid_block = _get_block(board, best_choice[1], best_choice[2])
        return _create_move(best_choice[0], valid_block)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
