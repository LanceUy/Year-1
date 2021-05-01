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
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    colour_list = COLOUR_LIST[:]
    goals = ['perimeter', 'blob']
    random.shuffle(colour_list)
    goal = random.choice(goals)
    output_goals = []
    for i in range(num_goals):
        if goal == 'perimeter':
            output_goals.append(PerimeterGoal(colour_list[i]))
        else:
            output_goals.append(BlobGoal(colour_list[i]))
    return output_goals


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    outer = []
    inner = []
    grid_size = 2 ** (block.max_depth - block.level)
    # Generate a starting grid with list of list of tuples
    for _ in range(grid_size):
        inner.append((0, 0, 0))
    for _ in range(grid_size):
        outer.append(inner[:])

    if not block.children:
        #  No children then make a grid with block.colour
        for r in range(grid_size):
            for c in range(grid_size):
                outer[r][c] = block.colour
        return outer

    child_grid_size = round(grid_size / 2)

    #  Split children in order to recurse
    top_right = _flatten(block.children[0])
    top_left = _flatten(block.children[1])
    bottom_left = _flatten(block.children[2])
    bottom_right = _flatten(block.children[3])

    for r in range(grid_size):
        for c in range(grid_size):
            #  TOP RIGHT
            if c < child_grid_size <= r:
                outer[r][c] = top_right[r - child_grid_size][c]
            #  TOP LEFT
            elif r < child_grid_size and c < child_grid_size:
                outer[r][c] = top_left[r][c]
            #  BOTTOM LEFT
            elif r < child_grid_size <= c:
                outer[r][c] = bottom_left[r][c - child_grid_size]
            #  BOTTOM RIGHT
            elif r >= child_grid_size and c >= child_grid_size:
                outer[r][c] = \
                    bottom_right[r - child_grid_size][c - child_grid_size]
    return outer


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A player goal in the game of Blocky.

    The purpose of this goal is to cover the perimeter with <colour> as much
    as possible.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given <board>.

        The score is always greater than or equal to 0.
        """
        new_board = board.create_copy()
        grid = _flatten(new_board)
        score = 0
        for i in range(len(grid)):
            if grid[0][i] == self.colour:  # Left Downwards
                score += 1
            if grid[i][0] == self.colour:  # Top Rightwards
                score += 1
            if grid[len(grid) - 1][i] == self.colour:  # Right Downwards
                score += 1
            if grid[i][len(grid) - 1] == self.colour:  # Bottom Rightwards
                score += 1
        return score

    def description(self) -> str:
        """ Returns the goal of the player on the bottom right section of
        the game screen. This goal is for PerimeterGoal.
        """
        colour = colour_name(self.colour)
        return 'Goal: Fill the perimeter with {0}.'.format(colour)


class BlobGoal(Goal):
    """A player goal in the game of Blocky.

    The purpose of this goal is to create the largest possible connected "blob"
    of the colour <colour>.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given <board>.

        The score is always greater than or equal to 0.
        """
        max_blob = 0
        flattened_board = _flatten(board)
        visited = [[-1 for _ in range(len(flattened_board[x]))]
                   for x in range(len(flattened_board))]
        for column in range(len(flattened_board)):
            for row in range(len(flattened_board)):
                if flattened_board[column][row] == self.colour:
                    max_blob = max(max_blob,
                                   self._undiscovered_blob_size((column, row),
                                                                flattened_board,
                                                                visited))
        return max_blob

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        x = pos[0]
        y = pos[1]
        # make sure there are no negative indices
        if x < 0 or y < 0:
            return 0
        # check if pos is in the board
        try:
            visited[x][y]
        except IndexError:
            return 0
        # only check this cell if if wasn't checked already
        if visited[x][y] == -1:
            visited[x][y] = int(board[x][y] == self.colour)
            if visited[x][y]:
                size = 1 + \
                       self._undiscovered_blob_size((x + 1, y), board, visited)\
                       + self._undiscovered_blob_size((x - 1, y), board,
                                                      visited) + \
                       self._undiscovered_blob_size((x, y - 1), board,
                                                    visited) + \
                       self._undiscovered_blob_size((x, y + 1), board, visited)
                return size
            else:
                return 0
        # if cell was already checked then return 0
        else:
            return 0

    def description(self) -> str:
        """ Returns the goal of the player on the bottom right section of
        the game screen. This goal is for BlobGoal.
        """
        colour = colour_name(self.colour)
        return 'Goal: Create the largest blob with {0}.'.format(colour)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
