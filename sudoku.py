
from solver import Solver
import copy

class Sudoku:

   template1 = [[5,3,0,0,7,0,9,1,0],
               [6,0,0,1,9,0,3,0,0],
               [1,9,8,3,4,2,5,6,7],
               [8,0,9,7,6,0,4,0,3],
               [4,2,6,0,5,3,7,9,1],
               [7,0,3,0,2,0,8,0,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,0,0,0,8,0,1,7,9]]
   
   template1 = [[5,3,0,0,7,0,9,1,0],
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
               [8,0,0,0,0,0,0,0,3],
               [0,0,0,0,0,3,0,0,1],
               [7,0,0,0,2,0,0,0,6],
               [0,6,0,0,0,0,2,8,0],
               [0,0,0,4,1,9,0,0,5],
               [0,0,0,0,8,0,0,7,9]]
   
   template1 = [[5,3,0,0,7,0,0,0,0],
               [6,0,0,1,9,0,0,0,0],
               [0,9,8,0,0,0,0,6,0],
               [8,0,0,0,6,0,0,0,3],
               [0,0,0,0,0,0,0,0,1],
               [7,0,0,0,2,0,0,0,6],
               [0,6,0,0,0,0,2,8,0],
               [0,0,7,4,0,9,0,0,5],
               [0,0,0,0,0,0,0,7,9]]

   def __init__(self, gui):
      self.gui = gui
      self.create_grid()

      self.update_gui()
      self.solver = Solver()

      self.group_count = 9+9+9
      self.group_ii = 0

   def start_solve(self):
      self.gui.start(self.stepping_solve)

   def stepping_solve(self):

      print(self.group_ii)

      self.solver.begin_simple(self.groups[self.group_ii])
      self.group_ii = (self.group_ii +1 )% self.group_count
      self.update_gui()
      pass

   def create_grid(self):
      # Create the grid and setup the groups
      self.grid = [[Cell() for ii in range(9)] for jj in range(9)]
      self.create_groups()

      # Setup for the small labels
      self.small_labels = [[None for ii in range(9)] for jj in range(9)] 

      for ii in range(9):
         for jj in range(9):
            value = self.template[jj][ii]
            x = ii
            y = jj
            if value != 0:
               self.grid[x][y].set_value(value)
               self.gui.draw_number(ii, jj, value)
            else:
               self.small_labels[x][y] = self.gui.draw_small_number(x,y,[1,2,3,4,5,6,7,8,9])

   def create_groups(self):
      self.groups = []
      print("Creating Rows")
      self.groups.extend(self.get_rows())
      print("Creating Cols")
      self.groups.extend(self.get_cols())
      print("Creating Boxes")
      self.groups.extend(self.get_boxes())

   def get_rows(self):
      groups = []
      for y in range(9):
         row = []
         for x in range(9):
            row.append(self.grid[x][y])
         group = Group(row, "row")
         groups.append(group)
         
      return groups

   def get_cols(self):
      groups = []
      for x in range(9):
         col = []
         for y in range(9):
            col.append(self.grid[x][y])
         group = Group(col, "col")
         groups.append(group)
         
      return groups

   def get_boxes(self):
      groups = []
      for ii in range(9):
         box = []
         for jj in range(9):
            x = jj % 3 + ii % 3 *3
            y = jj // 3 + ii // 3 *3
            box.append(self.grid[x][y])
         group = Group(box, "box")
         groups.append(group)
      
      return groups

   def update_gui(self):
      pass   
      for x in range(9):
         for y in range(9):
            cell = self.grid[x][y]
            if True: #Check if any changed have happened
               labels = self.small_labels[x][y]
               if labels != None:
                  for label in labels:
                     self.gui.remove_label(label)

               if cell.value == 0: # value not known. update the small numbers
                  self.small_labels[x][y] =  self.gui.draw_small_number(x,y, cell.possible_values)
               else: # The value is known
                  self.gui.draw_number(x,y,cell.value)

class Group:
   def __init__(self, cells, type):
      self.remaining = 9
      self.possible_values = [1,2,3,4,5,6,7,8,9]
      self.cells = cells
      self.type=type

      self.changed = False

      self.unknown_cells = []

      for cell in cells:
         self.unknown_cells.append(cell)
         cell.add_group(self)



   def new_cell_value(self, cell, value):

      if value in self.possible_values:
         self.changed = True

         self.remaining -=1
         self.possible_values.remove(value)
         self.unknown_cells.remove(cell)

         for unknown_cell in self.unknown_cells:
            unknown_cell.remove_number(value)

   def has_changed(self):
      return self.changed

class Cell:
   def __init__(self):
      self.remaining = 9
      self.possible_values = [1,2,3,4,5,6,7,8,9]
      self.value = 0

      self.groups = []
      self.changed = False

   def add_group(self, group):
      self.groups.append(group)

   def remove_number(self, value):
      if value in self.possible_values:
         self.possible_values.remove(value)
         self.remaining -= 1

         if self.remaining == 1:
            self.set_value(self.possible_values[0])

   def set_value(self, value):
      self.changed = True
      self.value = value
      self.remaining = 0
      self.numbers = []

      for group in self.groups:
         group.new_cell_value(self, value)

   def get_possible_values(self):
      return self.possible_values

   def get_value(self):
      return self.value

   def has_value(self):
      return self.value != 0

   def has_changed(self):
      return self.changed