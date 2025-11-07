import tkinter as tk
import pprint

SingleBoardSize = 3
UltimateBoardSize = 3
EMPTY = ""
X = "X"
O = "O"  # noqa: E741
Draw_player = "*"
DRAW = "Friendship"
DIRECTION_NEG = -1
DIRECTION_POS = 2


class MiniBoard:
    def __init__(self, root, parent_board = None):
        self.player: str = X
        self.winner: str = EMPTY
        self.main_frame = root
        self.board: list[list[str]] = [[EMPTY for _ in range(SingleBoardSize)] for _ in range(SingleBoardSize)]

        frame = tk.Frame(self.main_frame, bg="violet", bd=2, relief="solid")
        frame.grid(row=0, column=0, padx=3, pady=3)
        self.sub_grids = self.__create_sub_grid(frame)
        self.parent_board = parent_board
        self.__change_title(f"Make a move Player:{self.player}")


    def make_move(self, row: int, col: int):
        """
        callback function that executes on button click
        this contains all the logic for small board game
        checks inputs, executes move, makes a callback to parent board if provided
        """
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError(
                f"Expected both position_x and position_y to be of type int, "
                f"but got {type(row).__name__} and {type(col).__name__}."
            )
        if row not in range(SingleBoardSize) or col not in range(SingleBoardSize):
            raise ValueError(f"given x:{row}, or y:{col} not in range:{SingleBoardSize}")
        if self.parent_board: #take parent player, otherwise use Your on for standalone mode
            self.player = self.parent_board.get_player()
        if self.player not in {X, O, Draw_player}:
            raise ValueError(f"player:{self.player}, not valid. Acceptable players are:{X}, {O}")
        if self.board[row][col] != EMPTY:
            self.__change_title(f"Given x:{row}-y:{col} already marked:{self.board[row][col]}")
            return

        self.board[row][col] = self.player
        button: tk.Button = self.sub_grids[row][col]
        button.config(text=self.player)
        button.flash()
        self.__set_button_inactive(button, self.__get_inactive_color())
        self.player = O if self.player is X else X
        if self.check_winner() is not EMPTY:
            self.set_board_inactive()
            self.__change_title(f"Congrats player {self.winner}. You won!!!")
        if self.parent_board:
            self.parent_board.move_made(self, row, col)
        self.__change_title(f"Make a move Player:{self.player}")

    def __is_full(self) -> bool:
        """
        :return: true if bord is full
        """
        for line in self.board:
            for mark in line:
                if mark is EMPTY:
                    return False
        return True

    def check_winner(self) -> str:
        for row, line in enumerate(self.board):
            for col, cell in enumerate(line):
                winner = self.__check_single_cell(row, col)
                if winner is not EMPTY:
                    self.winner = winner
        if self.winner is EMPTY and self.__is_full():
            self.winner = DRAW
            # board is full but no winner yet = DRAW
        return self.winner

    # checks given position in all directions for a matching player mark
    # returns
    def __check_single_cell(self, row: int, col: int) -> str:
        player: str = self.board[row][col]
        if player is EMPTY or player is Draw_player:
             return EMPTY
        pprint.pp(f"{self.board}")
        for dx in range(DIRECTION_NEG, DIRECTION_POS):
            for dy in range(DIRECTION_NEG, DIRECTION_POS):
                one_x = row + dx
                one_y = col + dy
                two_x = one_x + dx
                two_y = one_y + dy

                if (one_x not in range(SingleBoardSize) or one_y not in range(SingleBoardSize) or
                        two_x not in range(SingleBoardSize) or two_y not in range(SingleBoardSize)):
                    # out of bounds -> try diff directions
                    continue
                if one_x is row and two_x is row and one_y is col and two_y is col:
                    # did not move in all directions -> try diff directions
                    continue
                next_pos = self.board[one_x][one_y]
                next_next_pos = self.board[two_x][two_y]
                if player != next_pos or player != next_next_pos:
                    # print(f"return because {player} != {next_pos} or {next_next_pos} "
                    #       f"x:{row},{one_x},{two_x}-y:{col},{one_y},{two_y} ")
                    # Not our player -> continue diff directions
                    continue
                # print(f"winner found because {player} == {next_pos} == {next_next_pos} "
                #       f"x:{row},{one_x},{two_x}-y:{col},{one_y},{two_y} ")
                return player
        return EMPTY

    def set_board_inactive(self) -> None:
        for row in self.sub_grids:
            for button in row:
                self.__set_button_inactive(button, self.__get_inactive_color())

    @staticmethod
    def __set_button_inactive(button: tk.Button, color: str) -> None:
        button.config(background=color)
        button.config(state="disabled")

    def set_board_active(self) -> None:
        if self.check_winner() is not EMPTY:
            print("This board is filled, cannot activate")
            return
        for row_i, row in enumerate(self.sub_grids):
            for col_i, button in enumerate(row):
                if self.board[row_i][col_i] is EMPTY:# trust indexes as they are internal
                    self.__set_button_active(button)

    @staticmethod
    def __set_button_active(button: tk.Button) -> None:
        button.config(background="green")
        button.config(state="normal")

    def __get_inactive_color(self) -> str:
        if self.winner is X:
            return "blue"
        elif self.winner is O:
            return "orange"
        elif self.winner is DRAW:
            return "cyan"
        else:
            return "red"

    def __create_sub_grid(self, parent):
        buttons = list(list())
        for i in range(SingleBoardSize):
            button_row = []
            for j in range(SingleBoardSize):
                btn = tk.Button(
                    parent,
                    text=EMPTY,
                    width=4,
                    height=2,
                    font=("Arial", 14),
                    activebackground="blue",
                    background="green",
                    command=lambda row=i, col=j: self.make_move(row, col)
                    )
                btn.grid(row=i, column=j, padx=1, pady=1)
                button_row.append(btn)
            buttons.append(button_row)
        return buttons

    def __change_title(self, title: str) -> None:
        if not self.parent_board:
            self.main_frame.title(title)


class UltimateBoard:
    def __init__(self, root):
        self.root = root
        self.player: str = X
        self.root.title(f"UltimateTicTacToe: Make a move Player:{self.player}")
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(padx=10, pady=10)

        frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
        frame.grid(row=0, column=0, padx=3, pady=3)

        self.boards: list[list[MiniBoard]] = []
        for i in range(UltimateBoardSize):
            row: list[MiniBoard] = []
            for j in range(UltimateBoardSize):
                frame = tk.Frame(self.main_frame, bg="violet", bd=2, relief="solid")
                frame.grid(row=i, column=j, padx=3, pady=3)
                row.append(MiniBoard(frame, self))
            self.boards.append(row)
        hidden_frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
        self.mini_board = MiniBoard(hidden_frame, self)

    def get_player(self) -> str:
        return self.player

    def __play_mini_move(self, child):
        board_winner = child.check_winner()
        # No winner yet
        if board_winner is EMPTY:
            return EMPTY  # early return game is not finished while there are unwon boards

        # find which child won, and mark the correct cell on mini board
        for row, board_row in enumerate(self.boards):
            for col, board in enumerate(board_row):
                if child == board:
                    # play the move
                    prev_player = self.player
                    self.player = board_winner
                    self.mini_board.make_move(row, col)
                    self.player = prev_player

    def check_global_winner(self) -> str:
        return self.mini_board.check_winner()

    def move_made(self,child: MiniBoard, row: int, col: int) -> None:
        """
        - Executes logic after child board made a move with given index
        - If board in provided index is playable set's only it active, otherwise set's all playable boards active
        - Checks if there is a global winner.
        :param row: row index
        :param col: column index
        :return: None
        """
        self.__play_mini_move(child)
        winner = self.check_global_winner()
        if self.check_global_winner() is not EMPTY:
            self.root.title(f"UltimateTicTacToe: Congrats player:{winner} You Won!")
            self.__disable_all_boards()
            return
        # switch player
        self.player = O if self.player is X else X
        self.__disable_all_boards()
        # if last clicked board cords available set it active otherwise set all boards active
        if not self.__try_to_enable_single_board(self.boards[row][col]):
            self.__enable_all_boards()
        self.root.title(f"UltimateTicTacToe: Make a move Player:{self.player}")

    def __disable_all_boards(self) -> None:
        for row in self.boards:
            for board in row:
                board.set_board_inactive()

    def __enable_all_boards(self) -> None:
        for row in self.boards:
            for board in row:
                self.__try_to_enable_single_board(board)

    @staticmethod
    def __try_to_enable_single_board(board: MiniBoard) -> bool:
        if board.check_winner() is EMPTY:
            board.set_board_active()
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateBoard(root)
    root.mainloop()
