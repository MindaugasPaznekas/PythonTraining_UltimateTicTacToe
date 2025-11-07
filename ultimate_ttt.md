# Ultimate Tic-Tac-Toe

## 1. Game Overview

**Ultimate Tic-Tac-Toe (UTTT)** takes regular tic-tac-toe and adds a strategy layer.
You now play on nine mini 3×3 boards arranged in a global 3×3 grid.

**Key rules:**

* Each move determines where your opponent must play next.
* If that target board is already full or won, the next player may play anywhere.
* Win a mini-board to claim that position on the global board.
* Win the global board by taking three mini-boards in a row.

**Links**

https://bejofo.com/ttt

https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe

---

## 2. Scope

* Console (GUI is optional)
* Two human players (Computer opponent is optional)
* Unit-testable code
* Type hints & docstrings

---

## 3. Project Layout

```
ultimate_ttt/
├── core.py       # rules and main logic
├── models.py     # classes
├── cli.py        # command-line runner
├── tests/        # put unittests here
└── README.md     # instrucitons if needed
```

---

## 4. Steps:

### 1. Classic Tic-Tac-Toe

1. Board: `list[list[str]]` (3×3), cells in `{" ", "X", "O"}`.
2. Functions:

   * `make_move(board, row, column, player) -> bool`
   * `check_winner(board) -> {"X","O",None}`
   * `is_full(board) -> bool`
   * `render(board) -> str`
3. Loop: alternate `X`/`O`; validate input; stop on win/draw.
4. Unittest functions

---

### 2. MiniBoard class

1. create reusable 3×3 board class `class MiniBoard`:
   * Class instance attributes: `grid`, `status one of "empty","X","O","draw"`
   * Functions: 
        * `mark_cell(cell_idx, player)`, 
        * `update_status`, 
        * `is_full`, 
        * `render`
2. Original game still works via `MiniBoard`.
3. Tests still running

---

### 3. — Ultimate Board class

Create a `class UltimateBoard`:

* Holds 9 `MiniBoard`s
* Tracks big board status `super_board`
* Keeps `active_board` index (or `None` for “anywhere”)

1. Attributes:

   * `boards: list[MiniBoard]`
   * `super_board: MiniBoard` (tracks who won each mini-board)
   * `active_board: int | None` (None = any)

2. Functions:

   * `legal_moves() -> list[tuple[int, int]]` available (board_index, cell_index)
   * `apply(board_idx, cell_idx, player) -> None`
   * `check_global_winner() -> {"X","O",None}`
   * `render()` ultimate ttt board (3x3)

3. Implement rule: “your move sends opponent to that cell’s board”

    * After moking a move `(board, cell)`, next `active_board = cell`
    * If that board is closed, set `active_board = None`
    * Prevent illegal moves

4. Runner:

    * Print game state nicely in console
    * Prompt player input for (board + cell) -> optionally ask for board only when needed.
    * Handle bad inputs gracefully -> let user try again
    * Stop on win or draw

5. Tests:

    * with unittests cover board states and rule transitions
    (few tests are enough)

---

### 4. Extra
    * Simple random Computer Opponent
