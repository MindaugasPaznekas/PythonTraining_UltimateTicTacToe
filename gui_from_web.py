
import tkinter as tk

SingleBoardSize = 3
EMPTY = "."
X = "X"
O = "O"  # noqa: E741
DIRECTION_NEG = -1
DIRECTION_POS = 2

class UltimateTicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic Tac Toe")
        self.player: str = X
        self.winner: str = EMPTY

        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(padx=10, pady=10)
        self.board: list[list[str]] = [[EMPTY for _ in range(SingleBoardSize)] for _ in range(SingleBoardSize)]

        frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
        frame.grid(row=0, column=0, padx=3, pady=3)
        self.sub_grids = self.create_sub_grid(frame)
        row = []
        self.sub_grids.append(self.create_sub_grid(frame))
        self.sub_grids.append(row)

        for i in range(3):
            row = []
            for j in range(3):
                frame = tk.Frame(self.main_frame, bg="black", bd=2, relief="solid")
                frame.grid(row=i, column=j, padx=3, pady=3)
                sub_grid = self.create_sub_grid(frame)
                row.append(sub_grid)
            self.sub_grids.append(row)

    def on_button_click(self, row: int, col: int):
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError(
                f"Expected both position_x and position_y to be of type int, "
                f"but got {type(row).__name__} and {type(col).__name__}."
            )
        if row not in range(SingleBoardSize) or col not in range(SingleBoardSize):
            raise ValueError(f"given x:{row}, or y:{col} not in range:{SingleBoardSize}")
        if self.player not in {X, O}:
            raise ValueError(f"player:{self.player}, not valid. Acceptable players are:{X}, {O}")
        if self.is_full():
            self.__set_inactive__()
            print(f"Congrats player {self.winner}. You won!!!")
            return

        if self.board[row][col] != EMPTY:
            raise ValueError(f"Given x:{row}-y:{col} already marked{self.board[row][col]}")

        self.board[row][col] = self.player
        button: tk.Button = self.sub_grids[row][col]
        button.config(text=self.player)
        button.flash()
        self.player = O if self.player is X else X
        if self.is_full():
            self.__set_inactive__()
            print(f"Congrats player {self.winner}. You won!!!")

    def is_full(self) -> bool:
        if self.check_winner() is not EMPTY: #we have winner board is unplayable
            return True
        for line in self.board:
            for mark in line:
                if mark is EMPTY:
                    return False
            self.winner
        return True

    def check_winner(self) -> str:
        self.render()
        return self.winner

    def render(self) -> bool:
        for row, line in enumerate(self.board):
            for col, cell in enumerate(line):
                if self.__check_single_cell__(row, col):
                    return True
        return False

    def __check_single_cell__(self, row: int, col: int) -> bool:
        player = self.board[row][col]
        if player is EMPTY:
             return False
        print (f"{self.board}")
        for dx in range(DIRECTION_NEG, DIRECTION_POS):
            for dy in range(DIRECTION_NEG, DIRECTION_POS):
                one_x = row + dx
                one_y = col + dy
                two_x = one_x + dx
                two_y = one_y + dy
                if (one_x not in range(SingleBoardSize) or one_y not in range(SingleBoardSize) or
                        two_x not in range(SingleBoardSize) or two_y not in range(SingleBoardSize)):
                    # out of bounds -> try diff directions
                    break
                next_pos = self.board[one_x][one_y]
                next_next_pos = self.board[two_x][two_y]
                if player != next_pos or player != next_next_pos:
                    print(f"return {player} != {next_pos} or {next_next_pos} x:{row}-y:{col} ")
                    # Not our player -> continue diff directions
                    break
                self.winner = player
                return True

        return False

    def __set_inactive__(self):
        for row in self.sub_grids:
            for button in row:
                button.config(background="red")


    def create_sub_grid(self, parent):
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
                    activebackground="red",
                    background="yellow",
                    command=lambda row=i, col=j: self.on_button_click(row, col)
                    )
                btn.grid(row=i, column=j, padx=1, pady=1)
                button_row.append(btn)
            buttons.append(button_row)
        return buttons


if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTicTacToeGUI(root)
    root.mainloop()
