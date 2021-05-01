from player import _get_block, _random_valid_move
from player import *
from goal import *
from block import *
from blocky import *
from settings import *
from actions import *
import pytest


class Testsplayer:
    def test_create_player_no_players(self) -> None:
        assert [] == create_players(0, 0, [])

    def test_create_player_one_player(self) -> None:
        human = create_players(1, 0, [])
        random_ = create_players(0, 1, [])
        smart = create_players(0, 0, [5])
        assert human[0].id == 0
        assert random_[0].id == 0
        assert smart[0].id == 0
        assert smart[0]._difficulty == 5

    def test_create_multiple_players(self) -> None:
        players = create_players(1, 1, [5])
        players2 = create_players(0, 1, [5, 3, 4])
        players3 = create_players(1, 0, [1, 10, 8])
        assert players[0].id == 0 and type(players[0]) == HumanPlayer
        assert players[1].id == 1 and type(players[1]) == RandomPlayer
        assert players[2].id == 2 and type(players[2]) == SmartPlayer
        assert players2[0].id == 0 and type(players2[0]) == RandomPlayer
        assert players2[1].id == 1 and type(players2[1]) == SmartPlayer and \
               players2[1]._difficulty == 5
        assert players2[2].id == 2 and type(players2[2]) == SmartPlayer and \
               players2[2]._difficulty == 3
        assert players2[3].id == 3 and type(players2[3]) == SmartPlayer and \
               players2[3]._difficulty == 4

        assert players3[0].id == 0 and type(players3[0]) == HumanPlayer
        assert players3[1].id == 1 and type(players3[1]) == SmartPlayer and \
               players3[1]._difficulty == 1
        assert players3[2].id == 2 and type(players3[2]) == SmartPlayer and \
               players3[2]._difficulty == 10
        assert players3[3].id == 3 and type(players3[3]) == SmartPlayer and \
               players3[3]._difficulty == 8

    def test_get_block(self) -> None:
        single_block = Block((0, 0), 16, (0, 0, 0), 0, 0)
        one_level = Block ((0, 0), 16, None, 0, 1)
        one_level_upper_left = Block((0, 0), 8, None, 1, 1)
        one_level_upper_right = Block((8, 0), 8, PACIFIC_POINT, 1, 1)
        one_level_lower_left = Block((0, 8), 8, DAFFODIL_DELIGHT, 1, 1)
        one_level_lower_right = Block((8, 8), 8, BLACK, 1, 1)
        lul = Block((0, 0), 4, BLACK, 1, 1)
        lur = Block((4, 0), 4, PACIFIC_POINT, 1, 1)
        lll = Block((0, 4), 4, DAFFODIL_DELIGHT, 1, 1)
        llr = Block((4, 4), 4, WHITE, 1, 1)
        one_level.children = [one_level_upper_right, one_level_upper_left, one_level_lower_left, one_level_lower_right]
        one_level_upper_left.children = [lur, lul, lll, llr]

        assert None == _get_block(single_block, (16, 5), 0)
        assert None == _get_block(single_block, (5, 16), 0)
        assert single_block == _get_block(single_block, (0, 5), 0)
        assert single_block == _get_block(single_block, (5, 0), 0)
        assert single_block == _get_block(single_block, (5, 5), 0)
        assert single_block == _get_block(single_block, (5, 5), 0)
        assert one_level == _get_block(one_level, (0, 0), 0)
        assert one_level_upper_left == _get_block(one_level, (0, 0), 1)
        assert one_level_upper_right == _get_block(one_level, (8, 0), 1)
        assert one_level_lower_left == _get_block(one_level, (0, 8), 1)
        assert one_level_lower_right == _get_block(one_level, (8, 8), 1)
        assert one_level_upper_left == _get_block(one_level, (1, 5), 1)
        assert one_level_upper_right == _get_block(one_level, (9, 5), 1)
        assert one_level_lower_left == _get_block(one_level, (4, 14), 1)
        assert one_level_lower_right == _get_block(one_level, (13, 9), 1)

        assert lul == _get_block(one_level, (0, 0), 2)
        assert lur == _get_block(one_level, (4, 0), 2)
        assert lll == _get_block(one_level, (0, 4), 2)
        assert llr == _get_block(one_level, (4, 4), 2)
        assert lul == _get_block(one_level, (3, 2), 2)
        assert lur == _get_block(one_level, (5, 3), 2)
        assert lll == _get_block(one_level, (3, 6), 2)
        assert llr == _get_block(one_level, (5, 7), 2)

    def test_random_valid_move(self) -> None:
        single_block = Block((0, 0), 16, (0, 0, 0), 0, 1)
        one_level = Block((0, 0), 16, None, 0, 2)
        one_level_upper_left = Block((0, 0), 8, None, 1, 2)
        one_level_upper_right = Block((8, 0), 8, PACIFIC_POINT, 1, 2)
        one_level_lower_left = Block((0, 8), 8, DAFFODIL_DELIGHT, 1, 2)
        one_level_lower_right = Block((8, 8), 8, BLACK, 1, 2)
        lul = Block((0, 0), 4, BLACK, 2, 2)
        lur = Block((4, 0), 4, PACIFIC_POINT, 2, 2)
        lll = Block((0, 4), 4, DAFFODIL_DELIGHT, 2, 2)
        llr = Block((4, 4), 4, DAFFODIL_DELIGHT, 2, 2)
        one_level.children = [one_level_upper_right, one_level_upper_left, one_level_lower_left, one_level_lower_right]
        one_level_upper_left.children = [lur, lul, lll, llr]
        goal = PerimeterGoal(WHITE)
        player = RandomPlayer(0, goal)
        b1_ = False
        b2_ = False
        b3 = False
        b4 = False
        b5 = False
        b6 = False
        b7 = False
        for _ in range(1000):
            if _random_valid_move(player, one_level)[0] == PAINT:
                b1_ = True
        for _ in range(1000):
            if _random_valid_move(player, one_level)[0] == SMASH:
                b2_ = True
        for _ in range(1000):
            if _random_valid_move(player, one_level)[0] == SWAP_VERTICAL:
                b3 = True
        for _ in range(1000):
            if _random_valid_move(player, one_level)[0] == SWAP_HORIZONTAL:
                b4 = True
        for _ in range(1000):
            if _random_valid_move(player, one_level)[0] == ROTATE_COUNTER_CLOCKWISE:
                b5 = True
        for _ in range(1000):
            if _random_valid_move(player, one_level)[0] == ROTATE_CLOCKWISE:
                b6 = True
        for _ in range(1000):
            if _random_valid_move(player, one_level)[0] == COMBINE:
                b7 = True
        assert b1_
        assert b2_
        assert b3
        assert b4
        assert b5
        assert b6
        assert b7
        assert _random_valid_move(player, single_block)[0] == SMASH

    def test_random_generate_move(self) -> None:
        one_level = Block((0, 0), 16, None, 0, 2)
        one_level_upper_left = Block((0, 0), 8, None, 1, 2)
        one_level_upper_right = Block((8, 0), 8, PACIFIC_POINT, 1, 2)
        one_level_lower_left = Block((0, 8), 8, DAFFODIL_DELIGHT, 1, 2)
        one_level_lower_right = Block((8, 8), 8, BLACK, 1, 2)
        lul = Block((0, 0), 4, BLACK, 2, 2)
        lur = Block((4, 0), 4, PACIFIC_POINT, 2, 2)
        lll = Block((0, 4), 4, DAFFODIL_DELIGHT, 2, 2)
        llr = Block((4, 4), 4, DAFFODIL_DELIGHT, 2, 2)
        one_level.children = [one_level_upper_right, one_level_upper_left, one_level_lower_left, one_level_lower_right]
        one_level_upper_left.children = [lur, lul, lll, llr]
        goal = PerimeterGoal(WHITE)
        player = RandomPlayer(0, goal)
        copy_board = one_level.create_copy()
        for _ in range(10000):
            player._proceed = True
            assert player.generate_move(one_level)[0] != 'pass'
        b1_ = False
        b2_ = False
        b3 = False
        b4 = False
        b5 = False
        b6 = False
        b7 = False
        for _ in range(1000):
            player._proceed = True
            if player.generate_move(one_level)[0] == PAINT[0]:
                b1_ = True
        for _ in range(1000):
            player._proceed = True
            if player.generate_move(one_level)[0] == SMASH[0]:
                b2_ = True
        for _ in range(1000):
            player._proceed = True
            if player.generate_move(one_level)[0] == SWAP_VERTICAL[0]:
                b3 = True
        for _ in range(1000):
            player._proceed = True
            if player.generate_move(one_level)[0] == SWAP_HORIZONTAL[0]:
                b4 = True
        for _ in range(1000):
            player._proceed = True
            if player.generate_move(one_level)[0] == ROTATE_COUNTER_CLOCKWISE[0]:
                b5 = True
        for _ in range(1000):
            player._proceed = True
            if player.generate_move(one_level)[0] == ROTATE_CLOCKWISE[0]:
                b6 = True
        for _ in range(1000):
            player._proceed = True
            if player.generate_move(one_level)[0] == COMBINE[0]:
                b7 = True
        assert b1_
        assert b2_
        assert b3
        assert b4
        assert b5
        assert b6
        assert b7
        assert one_level == copy_board

    def test_smart_generate(self) -> None:
        one_level = Block((0, 0), 16, None, 0, 2)
        one_level_upper_left = Block((0, 0), 8, None, 1, 2)
        one_level_upper_right = Block((8, 0), 8, PACIFIC_POINT, 1, 2)
        one_level_lower_left = Block((0, 8), 8, DAFFODIL_DELIGHT, 1, 2)
        one_level_lower_right = Block((8, 8), 8, BLACK, 1, 2)
        lul = Block((0, 0), 4, BLACK, 2, 2)
        lur = Block((4, 0), 4, PACIFIC_POINT, 2, 2)
        lll = Block((0, 4), 4, DAFFODIL_DELIGHT, 2, 2)
        llr = Block((4, 4), 4, DAFFODIL_DELIGHT, 2, 2)
        one_level.children = [one_level_upper_right, one_level_upper_left, one_level_lower_left, one_level_lower_right]
        one_level_upper_left.children = [lur, lul, lll, llr]
        goal = PerimeterGoal(WHITE)
        player = SmartPlayer(0, goal, 10)
        for _ in range(1000):
            copy_board = one_level.create_copy()
            player._proceed = True
            move = player.generate_move(copy_board)
            assert copy_board == one_level
            if move[0] == PAINT[0]:
                move[2].paint(player.goal.colour)
                assert player.goal.score(copy_board) > player.goal.score(one_level)
            elif move[0] == ROTATE_CLOCKWISE[0]:
                move[2].rotate(ROTATE_CLOCKWISE[1])
                assert player.goal.score(copy_board) > player.goal.score(one_level)
            elif move[0] == ROTATE_COUNTER_CLOCKWISE[0]:
                move[2].rotate(ROTATE_COUNTER_CLOCKWISE[1])
                assert player.goal.score(copy_board) > player.goal.score(one_level)
            elif move[0] == SMASH[0]:
                move[2].smash()
                assert player.goal.score(copy_board) > player.goal.score(one_level)
            elif move[0] == SWAP_HORIZONTAL[0]:
                move[2].swap(SWAP_HORIZONTAL[1])
                assert player.goal.score(copy_board) > player.goal.score(one_level)
            elif move[0] == SWAP_VERTICAL[0]:
                move[2].swap(SWAP_VERTICAL[1])
                assert player.goal.score(copy_board) > player.goal.score(one_level)
            elif move[0] == COMBINE[0]:
                move[2].combine()
                assert player.goal.score(copy_board) > player.goal.score(one_level)
            else:
                assert move[0] == PASS[0]
                assert player.goal.score(copy_board) == player.goal.score(one_level)


if __name__ == '__main__':
    import pytest

    pytest.main(['a2_tests.py'])
