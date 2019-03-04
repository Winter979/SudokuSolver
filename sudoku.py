
from solver import Solver

class Sudoku:

   template2 = [[5,3,0,0,7,0,9,1,0],
               [6,0,0,1,9,0,3,0,0],
               [1,9,8,0,0,0,0,6,7],
               [8,0,9,7,6,0,0,0,3],
               [4,0,6,0,5,3,0,0,1],
               [7,0,3,0,2,0,0,0,6],
               [9,6,1,0,0,0,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,0,0,0,8,0,1,7,9]]

   template = [[5,3,0,0,7,0,0,0,0],
               [6,0,0,1,9,0,0,0,0],
               [0,9,8,0,0,0,0,6,0],
               [8,0,0,0,6,0,0,0,3],
               [0,0,0,0,0,3,0,0,1],
               [7,0,0,0,2,0,0,0,6],
               [0,6,0,0,0,0,2,8,0],
               [0,0,0,4,1,9,0,0,5],
               [0,0,0,0,8,0,0,7,9]]

   def __init__(self, gui):
      self.gui = gui
      self.create_grid()
      self.update_gui()
      self.solver = Solver()


   def create_grid(self):
      self.grid = [[Cell() for ii in range(9)] for jj in range(9)]

      self.small_labels = [[[None for kk in range(9)] for ii in range(9)] for jj in range(9) ]

      for ii in range(9):
         for jj in range(9):
            value = self.template[jj][ii]
            x = ii
            y = jj
            if value != 0:
               self.grid[x][y].setValue(value)
               self.gui.draw_number(ii, jj, value)
            else:
               self.small_labels[x][y] = self.gui.draw_small_number(x,y,[1,2,3,4,5,6,7,8,9])

   def iterate_solve(self):
      self.solve_vertical()
      self.solve_horizontal()
      self.solve_square()

      self.update_gui()

   def solve_vertical(self):

      for ii in range(9):
         line = [None]*9
         for jj in range(9):
            line[jj] = self.grid[ii][jj]
         
         self.solve_array(line,"column")

   def solve_horizontal(self):
      for ii in range(9):
         line = [None]*9
         for jj in range(9):
            line[jj] = self.grid[jj][ii]
         
         self.solve_array(line,"row")

   def solve_square(self):

      print("*"*80)

      for ii in range(9):
         line = [0]*9
         for jj in range(9):
            x = jj % 3 + ii % 3 *3
            y = jj // 3 + ii // 3 *3
            line[jj] = self.grid[x][y]

         self.solve_array(line, "square")

   def solve_array(self, array, shape):
      if shape == "row" or shape == "column" or shape == "square":
         self.solver.begin_simple(array, shape)

   def update_gui(self):   
      for x in range(9):
         for y in range(9):
            cell = self.grid[x][y]
            if cell.changed:
               for label in self.small_labels[x][y]:
                  self.gui.remove_label(label)

               if cell.value == 0: # value not known. update the small numbers
                  self.small_labels[x][y] =  self.gui.draw_small_number(x,y, cell.numbers)
               else: # The value is known
                  self.gui.draw_number(x,y,cell.value)  
               cell.changed = False

class Cell:
   def __init__(self):
      self.remaining = 9
      self.numbers = [1,2,3,4,5,6,7,8,9]
      self.value = 0
      self.changed = False

   def remove_number(self, number):
      if number in self.numbers:
         self.numbers.remove(number)
         self.remaining -=1
         self.changed = True

         if self.remaining == 1:
            self.setValue(self.numbers.pop())

   def setValue(self, value):
      self.changed = True
      self.value = value
      self.remaining = 0
      self.numbers = []

   def getValue(self):
      return self.value