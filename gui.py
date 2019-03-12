from tkinter import Tk, Canvas, Label

class Gui:
   def __init__(self, cell_size=50):
      self.width = cell_size * 9
      self.height = cell_size *9
      self.cells_x = 9
      self.cells_y = 9

      self.cell_size = cell_size

      self.window = Tk()
      self.canvas = Canvas(self.window, bg='white', width=self.width, height=self.height)

      self.draw_grid()

      self.canvas.pack()

   def draw_grid(self):
      # Creates all vertical lines at intevals of cell width
      for i in range(0, self.width, self.cell_size):
         if i % 3 == 0:
            width = 3
         else:
            width = 1
         self.canvas.create_line([(i, 0), (i, self.height)], width=width)

      # Creates all horizontal lines at intevals of cell height
      for i in range(0, self.width, self.cell_size):
         if i % 3 == 0:
            width = 3
         else:
            width = 1
         self.canvas.create_line([(0, i), (self.width, i)],width = width)

# ------------------------------------------------------------------------------

   def start(self, callback):
      self.loop(callback)
      self.window.mainloop()

   def loop(self, callback):
      callback()
      self.window.after(300, self.loop, callback)


# ------------------------------------------------------------------------------

   def draw_number(self, x, y, number):
      label = self.canvas.create_text((x+.5)*self.cell_size, (y+.5)*self.cell_size,anchor="center")
      self.canvas.itemconfig(label, text=number, font=("Arial", 30))

   def draw_small_number(self, x, y, numbers):

      labels = []

      for number in numbers:
         draw_x, draw_y = self.small_number_coords(x,y, number)
         label = self.canvas.create_text(draw_x, draw_y, anchor="center")
         self.canvas.itemconfig(label, text=number, font=("Arial", self.cell_size // 4))
         
         labels.append(label)

      return labels

   def small_number_coords(self, x,y, number):
      draw_x = (x + self.thirds_math((number-1) % 3)) * self.cell_size
      draw_y = (y + self.thirds_math((number-1) // 3)) * self.cell_size

      return draw_x,draw_y

   def remove_label(self, label):
      if label != None:
         self.canvas.delete(label)

   def thirds_math(self, ii):
      ratio = 0

      if ii == 0:
         ratio = 1/6
      elif ii == 1:
         ratio = 3/6
      elif ii == 2:
         ratio = 5/6

      return ratio
      
