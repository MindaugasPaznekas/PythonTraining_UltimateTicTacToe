import tkinter as tk
import models


def singleBoardGame() -> None:
    root = tk.Tk()
    app = models.MiniBoard(root)
    root.mainloop()

def ultimateTTTGame() -> None:
    root = tk.Tk()
    app = models.UltimateBoard(root)
    root.mainloop()

if __name__ == "__main__":
    # singleBoardGame()
    ultimateTTTGame()