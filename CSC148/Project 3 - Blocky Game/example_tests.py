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

This file contains some sample tests for Assignment 2.
Please use this as a starting point to check your work and write your own
tests!
"""
from typing import List, Optional, Tuple
import os
import pygame
import pytest
import copy

from block import Block, generate_board
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten
from player import _get_block
from renderer import Renderer
from settings import COLOUR_LIST


def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)


@pytest.fixture
def renderer() -> Renderer:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    return Renderer(750)


@pytest.fixture
def child_block() -> Block:
    """Create a reference child block with a size of 750 and a max_depth of 0.
    """
    return Block((0, 0), 750, COLOUR_LIST[0], 0, 0)


@pytest.fixture
def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_swap0() -> Block:
    """Create a reference board that is swapped along the horizontal plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    return board


@pytest.fixture
def board_16x16_rotate1() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def flattened_board_16x16() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]


def test_create_copy() -> None:
    """ Test create copy for deep copy
    """
    b1 = generate_board(5, 750)
    b2 = b1.create_copy()

    assert b1 == b2
    assert b1 is not b2

    b3 = copy.deepcopy(b1)
    assert b2 is not b3
    assert b2 == b3


def test_update_children_position():
    # Update regular positions
    b1 = Block((44, 44), 750, None, 0, 1)
    b2 = Block((0, 0), 750, COLOUR_LIST[0], 0, 1)
    b3 = Block((0, 0), 750, COLOUR_LIST[1], 0, 1)
    b4 = Block((0, 0), 750, COLOUR_LIST[2], 0, 1)
    b5 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b1.children = [b2, b3, b4, b5]

    b1._update_children_positions((0, 0))
    pos = b1._children_positions()
    lst = []
    for child in b1.children:
        lst.append(child.position)
    assert lst == pos

    # Update positions with children
    b6 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b7 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b8 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b9 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b2.children = [b6, b7, b8, b9]

    b1._update_children_positions((657, 5334))
    pos = b2._children_positions()
    lst = []
    for child in b2.children:
        lst.append(child.position)
    assert lst == pos


def test_smash():
    # Test for when function will NOT smash
    b1 = Block((44, 44), 750, None, 0, 1)
    b2 = Block((0, 0), 750, COLOUR_LIST[0], 0, 1)
    b3 = Block((0, 0), 750, COLOUR_LIST[1], 0, 1)
    b4 = Block((0, 0), 750, COLOUR_LIST[2], 0, 1)
    b5 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b1.children = [b2, b3, b4, b5]

    assert b1.smash() is False
    assert b2.position and b3.position and \
           b4.position and b5.position == (0, 0)

    b6 = Block((44, 44), 750, COLOUR_LIST[0], 1, 1)
    assert b6.smash() is False

    # Test for function WILL smash
    b7 = Block((0, 0), 750, COLOUR_LIST[0], 0, 1)
    assert len(b7.children) == 0
    assert b7.colour is COLOUR_LIST[0]
    b7.smash()
    assert len(b7.children) == 4
    assert b7.colour is None
    assert b7.max_depth == 1
    assert b7.level == 0

    lst = []
    for child in b7.children:
        assert child.level == 1
        assert child.max_depth == 1
        assert child.size == round(b7.size/2)
        assert child.smash() is False
        lst.append(child.position)
    assert lst == b7._children_positions()
    assert b7.smash() is False

    b8 = Block((0, 0), 750, COLOUR_LIST[0], 0, 5)
    b8.smash() # Level 1
    b8.children[1].smash() # 2
    b8.children[1].children[1].smash() # 3
    b8.children[1].children[1].children[1].smash() # 4
    b8.children[1].children[1].children[1].children[1].smash() # 5
    assert b8.children[1].children[1].children[1].children[1]\
        .children[1].smash() is False # 6

    b9 = b8.children[1].children[1].children[1].children[1].children[1]
    b10 = b8.children[1].children[1].children[1].children[1]
    assert b9.position == (0, 0)
    assert b8.colour is None
    assert b10.colour is None
    assert b10.level == 4
    for child in b10.children:
        assert child.level == 5
        assert child.max_depth == 5
        assert child.smash() is False
        assert child.size == round(b10.size/2)


def test_swap():
    b1 = Block((44, 44), 750, None, 0, 1)
    assert b1.swap(1) is False
    assert b1.swap(0) is False
    b2 = Block((0, 0), 750, COLOUR_LIST[0], 0, 1)
    b3 = Block((0, 0), 750, COLOUR_LIST[1], 0, 1)
    b4 = Block((0, 0), 750, COLOUR_LIST[2], 0, 1)
    b5 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b1.children = [b2, b3, b4, b5]

    temp_list = b1.children[:]

    b1.swap(1)
    assert b1.children == [b5, b4, b3, b2]
    b1.swap(1)
    assert b1.children == temp_list

    b1.swap(0)
    assert b1.children == [b3, b2, b5, b4]
    b1.swap(0)
    assert b1.children == temp_list


def test_rotate():
    b1 = Block((44, 44), 750, None, 0, 1)
    assert b1.rotate(1) is False
    assert b1.rotate(3) is False
    b2 = Block((0, 0), 750, COLOUR_LIST[0], 0, 1)
    b3 = Block((0, 0), 750, COLOUR_LIST[1], 0, 1)
    b4 = Block((0, 0), 750, COLOUR_LIST[2], 0, 1)
    b5 = Block((0, 0), 750, COLOUR_LIST[3], 0, 1)
    b1.children = [b2, b3, b4, b5]

    temp_list = b1.children[:]

    b1.rotate(1)
    assert b1.children == [b3, b4, b5, b2]
    b1.rotate(3)
    assert b1.children == temp_list

    for child in b1.children:
        assert child.rotate(1) is False
        assert child.rotate(3) is False


def test_paint():
    b1 = Block((44, 44), 750, COLOUR_LIST[0], 0, 1)
    assert b1.paint(COLOUR_LIST[1]) is False
    b1 = Block((44, 44), 750, COLOUR_LIST[0], 1, 1)
    assert b1.paint(COLOUR_LIST[0]) is False

    b1 = Block((44, 44), 750, None, 0, 1)
    b2 = Block((0, 0), 750, COLOUR_LIST[0], 1, 1)
    b3 = Block((0, 0), 750, COLOUR_LIST[1], 1, 1)
    b4 = Block((0, 0), 750, COLOUR_LIST[2], 1, 1)
    b5 = Block((0, 0), 750, COLOUR_LIST[3], 1, 1)
    b1.children = [b2, b3, b4, b5]

    assert b1.paint(COLOUR_LIST[1]) is False

    assert b2.paint(COLOUR_LIST[1]) is True
    assert b3.paint(COLOUR_LIST[1]) is False
    assert b4.paint(COLOUR_LIST[1]) is True
    assert b5.paint(COLOUR_LIST[1]) is True
    assert b2.colour == COLOUR_LIST[1]
    assert b3.colour == COLOUR_LIST[1]
    assert b4.colour == COLOUR_LIST[1]
    assert b5.colour == COLOUR_LIST[1]


def test_combine():
    b1 = Block((44, 44), 750, None, 0, 1)
    assert b1.combine() is False
    b2 = Block((0, 0), 750, COLOUR_LIST[0], 1, 1)
    b3 = Block((0, 0), 750, COLOUR_LIST[1], 1, 1)
    b4 = Block((0, 0), 750, COLOUR_LIST[2], 1, 1)
    b5 = Block((0, 0), 750, COLOUR_LIST[3], 1, 1)
    b1.children = [b2, b3, b4, b5]

    assert b1.combine() is False
    b1.children = [b2, b2.create_copy(), b4, b5]
    assert b1.combine() is True
    assert b1.children == []
    assert b1.colour is COLOUR_LIST[0]
    b1.colour = None
    b1.children = [b2, b4, b2.create_copy(), b5]
    assert b1.combine() is True
    assert b1.children == []
    assert b1.colour is COLOUR_LIST[0]
    b1.colour = None
    b1.children = [b2, b4, b5, b2.create_copy()]
    assert b1.combine() is True
    assert b1.children == []
    assert b1.colour is COLOUR_LIST[0]

    b1.colour = None

    b1.children = [b2, b2.create_copy(), b4, b4.create_copy()]
    assert b1.combine() is False
    assert b1.colour is None
    b1.children = [b2, b4, b2.create_copy(), b4.create_copy()]
    assert b1.combine() is False
    assert b1.colour is None
    b1.children = [b2, b4, b4.create_copy(), b2.create_copy()]
    assert b1.combine() is False
    assert b1.colour is None

    b1.children = [b2, b2.create_copy(), b5, b2.create_copy()]
    assert b1.combine() is True
    assert b1.children == []
    assert b1.colour is COLOUR_LIST[0]
    b1.colour = None
    b1.children = [b2, b5, b2.create_copy(), b2.create_copy()]
    assert b1.combine() is True
    assert b1.children == []
    assert b1.colour is COLOUR_LIST[0]
    b1.colour = None
    b1.children = [b5, b2, b2.create_copy(), b2.create_copy()]
    assert b1.combine() is True
    assert b1.children == []
    assert b1.colour is COLOUR_LIST[0]
    b1.colour = None

    b1.children = [b2, b2.create_copy(), b2.create_copy(), b2.create_copy()]
    assert b1.combine() is True
    assert b1.children == []
    assert b1.colour is COLOUR_LIST[0]


def test_block_to_squares():
    b1 = Block((0, 0), 750, COLOUR_LIST[1], 0, 1)
    assert _block_to_squares(b1) == [((COLOUR_LIST[1]), (0, 0), 750)]
    b2 = Block((0, 0), 375, COLOUR_LIST[0], 1, 1)
    b3 = Block((0, 0), 375, COLOUR_LIST[1], 1, 1)
    b4 = Block((0, 0), 375, COLOUR_LIST[2], 1, 1)
    b5 = Block((0, 0), 375, COLOUR_LIST[3], 1, 1)
    b1.children = [b2, b3, b4, b5]
    assert set(_block_to_squares(b1)) == {((COLOUR_LIST[0]), (0, 0), 375),
                                          ((COLOUR_LIST[1]), (0, 0), 375),
                                          ((COLOUR_LIST[2]), (0, 0), 375),
                                          ((COLOUR_LIST[3]), (0, 0), 375)}

    b2.children = [b2.create_copy(), b3.create_copy(), b4.create_copy(),
                   b5.create_copy()]
    assert set(_block_to_squares(b1.create_copy())) == {((COLOUR_LIST[0]), (0, 0), 375),
                                          ((COLOUR_LIST[1]), (0, 0), 375),
                                          ((COLOUR_LIST[2]), (0, 0), 375),
                                          ((COLOUR_LIST[3]), (0, 0), 375),
                                          ((COLOUR_LIST[1]), (0, 0), 375),
                                          ((COLOUR_LIST[2]), (0, 0), 375),
                                          ((COLOUR_LIST[3]), (0, 0), 375)}


def test_perimeter_score():
    g = PerimeterGoal(COLOUR_LIST[0])
    # depth 0
    b1 = Block((0, 0), 750, COLOUR_LIST[0], 0, 0)
    assert g.score(b1) == 4
    # depth 1
    b1 = Block((0, 0), 750, None, 0, 1)
    b2 = Block((0, 0), 375, COLOUR_LIST[0], 1, 1)
    b3 = Block((0, 0), 375, COLOUR_LIST[1], 1, 1)
    b4 = Block((0, 0), 375, COLOUR_LIST[2], 1, 1)
    b5 = Block((0, 0), 375, COLOUR_LIST[3], 1, 1)
    b1.children = [b2, b3, b4, b5]
    assert g.score(b1) == 2
    b1.children = [b2, b2.create_copy(), b2.create_copy(), b2.create_copy()]
    assert g.score(b1) == 8
    # depth 2
    b6 = Block((0, 0), 375, None, 0, 2)
    b7 = Block((0, 0), 375, None, 1, 2)
    b8 = Block((0, 0), 375, COLOUR_LIST[2], 1, 2)
    b9 = Block((0, 0), 375, COLOUR_LIST[3], 1, 2)
    b10 = Block((0, 0), 375, COLOUR_LIST[0], 1, 2)
    b6.children = [b7, b8, b9, b10]
    b7a = Block((0, 0), 375, COLOUR_LIST[0], 2, 2)
    b8a = Block((0, 0), 375, COLOUR_LIST[2], 2, 2)
    b9a = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b10a = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b7.children = [b7a, b8a, b9a, b10a]
    assert g.score(b6) == 6
    # 4 corners only
    b11 = Block((0, 0), 375, None, 0, 2)
    b12 = Block((0, 0), 375, None, 1, 2)
    b13 = Block((0, 0), 375, None, 1, 2)
    b14 = Block((0, 0), 375, None, 1, 2)
    b15 = Block((0, 0), 375, None, 1, 2)
    b11.children = [b12, b13, b14, b15]
    # top right
    b12a = Block((0, 0), 375, COLOUR_LIST[0], 2, 2)
    b13a = Block((0, 0), 375, COLOUR_LIST[2], 2, 2)
    b14a = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b15a = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b12.children = [b12a, b13a, b14a, b15a]
    # top left
    b12b = Block((0, 0), 375, COLOUR_LIST[1], 2, 2)
    b13b = Block((0, 0), 375, COLOUR_LIST[0], 2, 2)
    b14b = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b15b = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b13.children = [b12b, b13b, b14b, b15b]
    # bottom left
    b12c = Block((0, 0), 375, COLOUR_LIST[1], 2, 2)
    b13c = Block((0, 0), 375, COLOUR_LIST[2], 2, 2)
    b14c = Block((0, 0), 375, COLOUR_LIST[0], 2, 2)
    b15c = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b14.children = [b12c, b13c, b14c, b15c]
    # bottom right
    b12d = Block((0, 0), 375, COLOUR_LIST[1], 2, 2)
    b13d = Block((0, 0), 375, COLOUR_LIST[2], 2, 2)
    b14d = Block((0, 0), 375, COLOUR_LIST[3], 2, 2)
    b15d = Block((0, 0), 375, COLOUR_LIST[0], 2, 2)
    b15.children = [b12d, b13d, b14d, b15d]
    assert g.score(b11) == 8


def test_block_to_squares_leaf(child_block) -> None:
    """Test that a board with only one block can be correctly trasnlated into
    a square that would be rendered onto the screen.
    """
    squares = _block_to_squares(child_block)
    expected = [(COLOUR_LIST[0], (0, 0), 750)]

    assert squares == expected


def test_block_to_squares_reference(board_16x16) -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.
    squares = set(_block_to_squares(board_16x16))
    expected = {((1, 128, 181), (563, 0), 188),
                ((199, 44, 58), (375, 0), 188),
                ((199, 44, 58), (375, 188), 188),
                ((255, 211, 92), (563, 188), 188),
                ((138, 151, 71), (0, 0), 375),
                ((199, 44, 58), (0, 375), 375),
                ((255, 211, 92), (375, 375), 375)
                }

    assert squares == expected


class TestRender:
    """A collection of methods that show you a way to save the boards in your
    test cases to image (i.e., PNG) files.

    NOTE: this requires that your blocky._block_to_squares function is working
    correctly.
    """
    def test_render_reference_board(self, renderer, board_16x16) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('reference-board.png')

    def test_render_reference_board_swap0(self, renderer, board_16x16,
                                          board_16x16_swap0) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_swap0))
        renderer.save_to_file('reference-swap-0.png')

        # Render what your swap does to the reference board
        board_16x16.swap(0)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-swap-0.png')

    def test_render_reference_board_rotate1(self, renderer, board_16x16,
                                            board_16x16_rotate1) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_rotate1))
        renderer.save_to_file('reference-rotate-1.png')

        # Render what your swap does to the reference board
        board_16x16.children[0].rotate(1)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-rotate-1.png')


class TestBlock:
    """A collection of methods that test the Block class.

    NOTE: this is a small subset of tests - just because you pass them does NOT
    mean you have a fully working implementation of the Block class.
    """
    def test_smash_on_child(self, child_block) -> None:
        """Test that a child block cannot be smashed.
        """
        child_block.smash()

        assert len(child_block.children) == 0
        assert child_block.colour == COLOUR_LIST[0]

    def test_smash_on_parent_with_no_children(self, board_16x16) -> None:
        """Test that a block not at max_depth and with no children can be
        smashed.
        """
        block = board_16x16.children[1]
        block.smash()

        assert len(block.children) == 4
        assert block.colour is None

        for child in block.children:
            if len(child.children) == 0:
                # A leaf should have a colour
                assert child.colour is not None
                # Colours should come from COLOUR_LIST
                assert child.colour in COLOUR_LIST
            elif len(child.children) == 4:
                # A parent should not have a colour
                assert child.colour is None
            else:
                # There should only be either 0 or 4 children (RI)
                assert False

    def test_swap0(self, board_16x16, board_16x16_swap0) -> None:
        """Test that the reference board can be correctly swapped along the
        horizontal plane.
        """
        board_16x16.swap(0)
        assert board_16x16 == board_16x16_swap0

    def test_rotate1(self, board_16x16, board_16x16_rotate1) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly rotated clockwise.
        """
        board_16x16.children[0].rotate(1)
        assert board_16x16 == board_16x16_rotate1


class TestPlayer:
    """A collection of methods for testing the methods and functions in the
    player module.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation.
    """
    def test_get_block_top_left(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-left corner of the board.
        """
        top_left = (0, 0)
        assert _get_block(board_16x16, top_left, 0) == board_16x16
        assert _get_block(board_16x16, top_left, 1) == board_16x16.children[1]

    def test_get_block_top_right(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-right corner of the board.
        """
        top_right = (board_16x16.size - 1, 0)
        assert _get_block(board_16x16, top_right, 0) == board_16x16
        assert _get_block(board_16x16, top_right, 1) == board_16x16.children[0]
        assert _get_block(board_16x16, top_right, 2) == \
            board_16x16.children[0].children[0]


class TestGoal:
    """A collection of methods for testing the sub-classes of Goal.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation of the Goal sub-classes.
    """
    def test_block_flatten(self, board_16x16, flattened_board_16x16) -> None:
        """Test that flattening the reference board results in the expected list
        of colours.
        """
        result = _flatten(board_16x16)

        # We are expected a "square" 2D list
        for sublist in result:
            assert len(result) == len(sublist)

        assert result == flattened_board_16x16

    def test_blob_goal(self, board_16x16) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 1),
            (COLOUR_LIST[1], 4),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check the results
        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_16x16) == expected

    def test_perimeter_goal(self, board_16x16):
        correct_scores = [
            (COLOUR_LIST[0], 2),
            (COLOUR_LIST[1], 5),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_16x16) == expected


if __name__ == '__main__':
    pytest.main(['example_tests.py'])
