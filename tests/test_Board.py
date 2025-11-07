from dataclasses import dataclass
from math import exp
import pytest
from models import SingleBoardSize, X, O, EMPTY

@pytest.mark.parametrize(
    "x", range(SingleBoardSize)
)
@pytest.mark.parametrize(
    "y", range(SingleBoardSize)
)
@pytest.mark.parametrize(
    "player", [X, O]
)
def test_make_move_possible_positions(x, y, player):
    board = Board(x, y)
    board.make_move(x, y, player)
    assert (board.check_winner() == EMPTY
        #result == exp_result
    ), f"Winner is not empty"

@pytest.mark.parametrize(
   ["x", "y", "player", "exception"],
    [
        (-5, 1, "X", ValueError),
        (0, -1, X, ValueError),
        (0, -1, X, ValueError),
        (0, 0.1, X, TypeError),
        (0, 3, X, ValueError),
        (0, 0, EMPTY, ValueError),
        (0, 0, 0, TypeError),
        (0, 0, None, TypeError),
        (None, 0, X, TypeError),
        (0, None, X, TypeError),
        (0, 0.0, X, TypeError),
        (0.0, 0, X, TypeError),
        (0, 0, "a", ValueError),
        (0, 0, "x", ValueError),

    ]
)

def test_invalid_inputs(x, y, player, exception):
    board = Board(x, y)
    with pytest.raises(exception):
        board.make_move(x, y, player)

# retired logic
class Board:
    def __init__(self, position_x, position_y):
        self.board_index: int = 0  # TODO
        self.winner: str = EMPTY
        self.board: list[list[str]] = [[EMPTY for _ in range(SingleBoardSize)] for _ in range(SingleBoardSize)]

    def make_move(self, position_x: int, position_y: int, player: str):
        if not isinstance(position_x, int) or not isinstance(position_y, int) or not isinstance(player, str):
            raise TypeError(
                f"Expected both position_x and position_y to be of type int, "
                f"but got {type(position_x).__name__} and {type(position_y).__name__}."
            )
        if position_x not in range(SingleBoardSize) or position_y not in range(SingleBoardSize):
            raise ValueError(f"given x:{position_x}, or y:{position_y} not in range:{SingleBoardSize}")
        if player not in {X, O}:
            raise ValueError(f"player:{player}, not valid. Acceptable players are:{X}, {O}")
        if self.board[position_x][position_y] != EMPTY:
            raise ValueError(
                f"Given x:{position_x}-y:{position_y} already marked{self.board[position_x][position_y]}")
        self.board[position_x][position_y] = player

    def check_winner(self) -> str:
        # TODO more logic here
        return self.winner

    def is_full(self) -> bool:
        if self.check_winner() is not EMPTY:  # we have winner board is unplayable
            return True
        for line in self.board:
            for mark in line:
                if mark is EMPTY:
                    return False
        return True

        # make_move(board, row, column, player) -> bool
        # check_winner(board) -> {"X", "O", None}
        # is_full(board) -> bool
        # render(board) -> str