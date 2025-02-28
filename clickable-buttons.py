from tkinter import *
import tkinter as tk
from PIL import ImageTk
from pulp import *



H = 1000
W = 800
curr_dir = '/Users/sachith/Hobby Projects/TangoSolver'

class ImageButton(Button):
    def __init__(self, master, ix_, iy_,  state_matrix_, *args, **kwargs):
        self.ix = ix_
        self.iy = iy_
        self.state_matrix = state_matrix_

        self.emptyCell = ImageTk.PhotoImage(file="dataset/empty.png")       # 0
        self.sun = ImageTk.PhotoImage(file = "dataset/sun.png")             # 1
        self.moon = ImageTk.PhotoImage(file = "dataset/moon.png")           # 2
        super().__init__(master, image = self.emptyCell,height=70,width=70, *args, **kwargs)
        self.state_matrix[self.ix][self.iy] = 0
        self.bind("<Button-1>", self.leftClickFunction)
        self.bind("<Button-2>", self.rightClickFunction)


    def leftClickFunction(self, event = None):
        if self.cget("state") != "disabled": #Ignore click if button is disabled
            if self.state_matrix[self.ix][self.iy] == 1:                       # sun to empty.
                self.state_matrix[self.ix][self.iy] = 0
                self.config(image = self.emptyCell)
            else:                                           # go from empty/moon to sun
                self.state_matrix[self.ix][self.iy] = 1
                self.config(image = self.sun)
        print('row =',self.ix,'col = ',self.iy)
        print(self.state_matrix)


    def rightClickFunction(self, event = None):
        if self.cget("state") != "disabled": #Ignore click if button is disabled
            if self.state_matrix[self.ix][self.iy] == 2:                       # moon to empty.
                self.state_matrix[self.ix][self.iy] = 0
                self.config(image = self.emptyCell)
            else:                                           # go from empty/sun to sun
                self.state_matrix[self.ix][self.iy] = 2
                self.config(image = self.moon)
        
        print('row =',self.ix,'col = ',self.iy)
        print(self.state_matrix)

    def setState(self,event='<Return>'):
        print(self.ix,self.iy,self.state_matrix[self.ix][self.iy])
        if self.cget("state") != "disabled":
            if self.state_matrix[self.ix][self.iy] == 0:
                self.config(image = self.emptyCell)

            elif self.state_matrix[self.ix][self.iy] == 1:
                self.config(image = self.sun)

            elif self.state_matrix[self.ix][self.iy] == 2:
                self.config(image = self.moon)
        
            else:
                assert(False)
            
            self.invoke()


class TangoBoard(Canvas):

    def __init__(self, master, *args, **kwargs):

        super().__init__(master,  height=H, width=W,bg='white',*args, **kwargs)
        
        self.state_matrix = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        self.master_reference=master

        # Creates all vertical lines at intevals of 100
        for i in range(100, 701, 100):
            self.create_line([(i, 100), (i, 700)], tag='grid_line',fill='black',width=3)

        # Creates all horizontal lines at intevals of 100
        for i in range(100, 701, 100):
            self.create_line([(100, i), (700, i)], tag='grid_line',fill='black',width=3)

        self.CellButtons = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]]
        # print(self.CellButtons)

        for row in range(6):
            for col in range(6):
                self.CellButtons[col][row] = ImageButton(master,col,row,self.state_matrix)
                self.CellButtons[col][row].place(x=(100*row)+115,y=(100*col)+115)

        
        # self.verticalAlignedButtons = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
        # #Try to draw a between cell button
        # for row in range(6):
        #     for col in range(5):
        #         self.CellButtons[row][col] = Button(self,text=' ')
 
        solve_button = Button(self,text='Solve!',command = self.solve_the_problem)
        solve_button.place(x=380,y=750)


    def solve_the_problem(self):
        print(self.state_matrix)
        matrix_of_variable = LpVariable.dicts("Choice", (range(6), range(6)), cat="Binary")


        prob = LpProblem("TangoSolver")

        # Adding the input constraints.
        for row in range(6):
            for col in range(6):
                if self.state_matrix[col][row]==1:
                    prob+= matrix_of_variable[col][row] == 0
                elif self.state_matrix[col][row]==2:
                    prob+= matrix_of_variable[col][row] == 1


        # Adding row wise restrictions.
        for row in range(6):
            prob += lpSum([matrix_of_variable[c][row] for c in range(6)]) == 3
            for start  in range(4):             ## 3 in a row cannot be same.
                prob += lpSum([matrix_of_variable[c][row] for c in range(start,start+3)]) >= 1
                prob += lpSum([matrix_of_variable[c][row] for c in range(start,start+3)]) <= 2
                
            
        
        # Adding col wise restrictions.
        for col in range(6):
            prob += lpSum([matrix_of_variable[col][r] for r in range(6)]) == 3
            for start  in range(4):
                prob += lpSum([matrix_of_variable[col][r] for r in range(start,start+3)]) >= 1
                prob += lpSum([matrix_of_variable[col][r] for r in range(start,start+3)]) <= 2

        


        prob.writeLP("Tango_Solver_LP.lp")
        prob.solve()
        
        print(self.state_matrix)

        for row in range(6):
            for col in range(6):
                # print(row,col,self.state_matrix[col][row],int(value(matrix_of_variable[col][row])+1))
                self.state_matrix[col][row] = int(value(matrix_of_variable[col][row])+1)
                self.CellButtons[col][row].setState()
                
        print(self.state_matrix)



def main():
    root = Tk()
    ex = TangoBoard(root)
    ex.pack()
    root.mainloop()


if __name__ == '__main__':
    main()