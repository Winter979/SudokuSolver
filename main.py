

from gui import Gui
from sudoku import Sudoku
  

def main():
   gui = Gui()

   sudoku = Sudoku(gui)

   gui.start(sudoku.iterate_solve)

if __name__ == "__main__":
   main()

