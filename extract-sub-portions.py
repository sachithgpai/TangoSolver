import tkinter as tk
H = 800
W = 800

def create_grid(event=None):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(100, 701, 100):
        c.create_line([(i, 100), (i, 700)], tag='grid_line',fill='black',width=3)

    # Creates all horizontal lines at intevals of 100
    for i in range(100, 701, 100):
        c.create_line([(100, i), (700, i)], tag='grid_line',fill='black',width=3)






root = tk.Tk()

c = tk.Canvas(root, height=H, width=W,bg='white')
c.pack(fill=tk.BOTH, expand=True)

def cell_click():
   print("click click!")

button_list  = []
B = tk.Button(c,bitmap='@./dataset/moon.xbm',command = cell_click)
B.place(x=105,y=105,height=90,width=90)

c.bind('<Configure>', create_grid)

root.mainloop()
