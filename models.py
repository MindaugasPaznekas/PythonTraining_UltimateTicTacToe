import tkinter as tk
import pprint

SingleBoardSize = 3
UltimateBoardSize = 3
EMPTY = "."
X = "X"
O = "O"  # noqa: E741
DRAW = "Friendship"
DIRECTION_NEG = -1
DIRECTION_POS = 2


class MiniBoard:
    def __init__(self, root, parent_board = None):
        self.root = root # somehow works in Ultimate board when it is passing frame instead of root :?
        # self.root.title("MiniBoard") # TODO probably not for us to decide
        self.player: str = X
        self.winner: str = EMPTY

        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(padx=10, pady=10)
        self.board: list[list[str]] = [[EMPTY for _ in range(SingleBoardSize)] for _ in range(SingleBoardSize)]

        frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
        frame.grid(row=0, column=0, padx=3, pady=3)
        self.sub_grids = self.__create_sub_grid(frame)
        self.parent_board = parent_board

    def __on_button_click(self, row: int, col: int):
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
        if self.player not in {X, O}:
            raise ValueError(f"player:{self.player}, not valid. Acceptable players are:{X}, {O}")
        if self.is_full():
            self.set_board_inactive()
            print(f"Congrats player {self.winner}. You won!!!")
            return
        if self.board[row][col] != EMPTY:
            if self.parent_board:
                self.parent_board.changeTitle(f"Given x:{row}-y:{col} already marked:{self.board[row][col]}")

        self.board[row][col] = self.player
        button: tk.Button = self.sub_grids[row][col]
        button.config(text=self.player)
        button.flash()
        self.__set_button_inactive(button, self.__get_inactive_color())
        self.player = O if self.player is X else X
        if self.is_full():
            self.set_board_inactive()
            print(f"Congrats player {self.winner}. You won!!!")
        if self.parent_board:
            self.parent_board.render(self, row, col)


    def is_full(self) -> bool:
        """

        :return: true if bord is full
        """
        if self.check_winner() is not EMPTY: #we have winner board is unplayable
            return True
        for line in self.board:
            for mark in line:
                if mark is EMPTY:
                    return False
        # board is full but no winner yet = DRAW
        self.winner = DRAW
        return True

    def check_winner(self) -> str:
        self.render()
        return self.winner

    def render(self) -> bool:
        for row, line in enumerate(self.board):
            for col, cell in enumerate(line):
                if self.__check_single_cell(row, col):
                    return True
        return False

    # checks given position in all directions for a matching player mark
    # returns
    def __check_single_cell(self, row: int, col: int) -> bool:
        player: str = self.board[row][col]
        if player is EMPTY:
             return False
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

                self.winner = player
                return True

        return False

    def set_board_inactive(self) -> None:
        for row in self.sub_grids:
            for button in row:
                self.__set_button_inactive(button, self.__get_inactive_color())

    @staticmethod
    def __set_button_inactive(button: tk.Button, color: str) -> None:
        button.config(background=color)
        button.config(state="disabled")

    def set_board_active(self) -> None:
        if self.is_full():
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
                    command=lambda row=i, col=j: self.__on_button_click(row, col)
                    )
                btn.grid(row=i, column=j, padx=1, pady=1)
                button_row.append(btn)
            buttons.append(button_row)
        return buttons


class UltimateBoard:
    __ANY_BOARD: int = None
    def __init__(self, root):
        self.root = root
        self.player: str = X
        self.root.title(f"UltimateTicTacToe: Make a move Player:{self.player}")
        self.winner: str = EMPTY

        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(padx=10, pady=10)
        self.active_board = self.__ANY_BOARD

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

    def legal_moves(self) -> None:
        print ("TODO maybe not needed for UI?")

    def get_player(self) -> str:
        return self.player

    def check_global_winner(self) -> str:
        player_x_wins = 0
        player_o_wins = 0
        draws = 0

        for row in self.boards:
            for board in row:
                board_winner = board.check_winner()
                # No winner yet
                if board_winner is EMPTY:
                    return EMPTY # early return game is not finished while there are unwon boards
                if board_winner is X:
                    player_x_wins += 1
                if board_winner is O:
                    player_o_wins += 1
                if board_winner is DRAW:
                    draws += 1

        if player_o_wins == player_x_wins:
            self.winner = DRAW
        elif player_x_wins > player_o_wins:
            self.winner = X
        else:
            self.winner = O
        return self.winner

    def render(self, vaikas, row: int, col: int) -> None:
        if self.check_global_winner() is not EMPTY:
            self.root.title(f"UltimateTicTacToe: Congrats player:{self.winner} You Won!")
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
        if not board.is_full():
            board.set_board_active()
            return True
        return False


    def changeTitle(self, title: str) -> None:
        new_title = f"Turn for player {self.player}. " + title
        self.root.title(new_title)


if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateBoard(root)
    root.mainloop()