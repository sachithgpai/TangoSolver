from tkinter import *
import tkinter as tk
from PIL import ImageTk
from pulp import *



H = 1000
W = 800
curr_dir = '/Users/sachith/Hobby Projects/TangoSolver'

class ImageButton(Button):
    def __init__(self, master, iy_, ix_,  state_matrix_,image0, image1, image2, buttonH, buttonW, *args, **kwargs):
        self.ix = ix_
        self.iy = iy_
        self.state_matrix = state_matrix_

        self.emptyCell = ImageTk.PhotoImage(file=image0)       # 0
        self.sun = ImageTk.PhotoImage(file = image1)             # 1
        self.moon = ImageTk.PhotoImage(file = image2)           # 2
        super().__init__(master, image = self.emptyCell,height=buttonH,width=buttonW, *args, **kwargs)
        self.state_matrix[self.iy][self.ix] = 0
        self.bind("<Button-1>", self.leftClickFunction)
        self.bind("<Button-2>", self.rightClickFunction)


    def leftClickFunction(self, event = None):
        prev = self.state_matrix[self.iy][self.ix]
        if self.state_matrix[self.iy][self.ix] == 1:                       # sun to empty.
            self.state_matrix[self.iy][self.ix] = 0
            self.config(image = self.emptyCell)
        else:                                           # go from empty/moon to sun
            self.state_matrix[self.iy][self.ix] = 1
            self.config(image = self.sun)

        print('leftClickFunction',self.iy,self.ix,prev,' -> ',self.state_matrix[self.iy][self.ix])


    def rightClickFunction(self, event = None):
        prev = self.state_matrix[self.iy][self.ix]
        if self.state_matrix[self.iy][self.ix] == 2:                       # moon to empty.
            self.state_matrix[self.iy][self.ix] = 0
            self.config(image = self.emptyCell)
        else:                                           # go from empty/sun to sun
            self.state_matrix[self.iy][self.ix] = 2
            self.config(image = self.moon)
        
        print('leftClickFunction',self.iy,self.ix,prev,' -> ',self.state_matrix[self.iy][self.ix])

        

    def setState(self):
        if self.state_matrix[self.iy][self.ix] == 0:
            self.config(image = self.emptyCell)

        elif self.state_matrix[self.iy][self.ix] == 1:
            self.config(image = self.sun)

        elif self.state_matrix[self.iy][self.ix] == 2:
            self.config(image = self.moon)
        else:
            assert(False)




class TangoBoard(Canvas):

    def __init__(self, master, *args, **kwargs):

        super().__init__(master,  height=H, width=W,bg='white',*args, **kwargs)
        
        # Creates all vertical lines at intevals of 100
        for i in range(100, 701, 100):
            self.create_line([(i, 100), (i, 700)], tag='grid_line',fill='black',width=3)

        # Creates all horizontal lines at intevals of 100
        for i in range(100, 701, 100):
            self.create_line([(100, i), (700, i)], tag='grid_line',fill='black',width=3)




        self.state_matrix = [[0 for _ in range(6)] for _ in range(6) ]
        self.CellButtons = [[None for _ in range(6)] for _ in range(6) ]
        # print(self.CellButtons)

        for row in range(6):
            for col in range(6):
                self.CellButtons[row][col] = ImageButton(master,row,col,self.state_matrix,"dataset/empty.png","dataset/sun.png","dataset/moon.png",70,70)
                self.CellButtons[row][col].place(x=(100*col)+115,y=(100*row)+115)
 
        solve_button = Button(self,text='Solve!',command = self.solve_the_problem)
        solve_button.place(x=380,y=750)


        # new buttons for equality and inequality
        self.vertical_inequality_matrix = [[0 for _ in range(5)] for _ in range(6) ]
        self.InequalityButtonsVertical = [[None for _ in range(5)] for _ in range(6) ]
        for row in range(6):
            for col in range(5):
                self.InequalityButtonsVertical[row][col] = ImageButton(master,row,col,self.vertical_inequality_matrix,"dataset/empty.png","dataset/equals.png","dataset/opposite.png",20,20,borderwidth=1)
                self.InequalityButtonsVertical[row][col].place(x=(100*col)+190,y=(100*row)+140)


                # new buttons for equality and inequality
        self.horizontal_inequality_matrix = [[0 for _ in range(6)] for _ in range(5) ]
        self.InequalityButtonsHorizontal = [[None for _ in range(6)] for _ in range(5) ]
        for row in range(5):
            for col in range(6):
                self.InequalityButtonsHorizontal[row][col] = ImageButton(master,row,col,self.horizontal_inequality_matrix,"dataset/empty.png","dataset/equals.png","dataset/opposite.png",20,20,borderwidth=1)
                self.InequalityButtonsHorizontal[row][col].place(x=(100*col)+140,y=(100*row)+190)
    


    def solve_the_problem(self):
        # print(self.state_matrix)
        # print('horizontal_inequality_matrix')
        # for lst in self.horizontal_inequality_matrix:
        #     print(*lst)

        # print('vertical_inequality_matrix')
        # for lst in self.vertical_inequality_matrix:
        #     print(*lst)


        matrix_of_variable = LpVariable.dicts("Choice", (range(6), range(6)),lowBound=0, upBound=1, cat="Binary")

        prob = LpProblem("TangoSolver")

        # Adding the input constraints.
        for row in range(6):
            for col in range(6):
                if self.state_matrix[row][col]==1:
                    prob+= matrix_of_variable[row][col] == 0
                elif self.state_matrix[row][col]==2:
                    prob+= matrix_of_variable[row][col] == 1


        # Adding row wise restrictions.
        for row in range(6):
            prob += lpSum([matrix_of_variable[row][c] for c in range(6)]) == 3
            for start  in range(4):             ## 3 in a row cannot be same.
                prob += lpSum([matrix_of_variable[row][c] for c in range(start,start+3)]) >= 1
                prob += lpSum([matrix_of_variable[row][c] for c in range(start,start+3)]) <= 2
                
            
        
        # Adding col wise restrictions.
        for col in range(6):
            prob += lpSum([matrix_of_variable[r][col] for r in range(6)]) == 3
            for start  in range(4):
                prob += lpSum([matrix_of_variable[r][col] for r in range(start,start+3)]) >= 1
                prob += lpSum([matrix_of_variable[r][col] for r in range(start,start+3)]) <= 2

        
        # Adding Vertical Inequality
        for row in range(6):
            for col in range(5):
                if self.vertical_inequality_matrix[row][col] == 1:
                    prob+= lpSum([matrix_of_variable[row][col],-1*matrix_of_variable[row][col+1]])==0
                elif self.vertical_inequality_matrix[row][col] == 2:
                    prob+= lpSum([matrix_of_variable[row][col],matrix_of_variable[row][col+1]])==1


        # Adding Horizontal Inequality
        for row in range(5):
            for col in range(6):
                if self.horizontal_inequality_matrix[row][col] == 1:
                    prob+= lpSum([matrix_of_variable[row][col],-1*matrix_of_variable[row+1][col]])==0
                elif self.horizontal_inequality_matrix[row][col] == 2:
                    prob+= lpSum([matrix_of_variable[row][col],matrix_of_variable[row+1][col]])==1
        


        prob.solve(COIN_CMD(msg=0))
        
        print(self.state_matrix)

        for row in range(6):
            for col in range(6):
                self.state_matrix[row][col] = int(value(matrix_of_variable[row][col])+1)
                self.CellButtons[row][col].setState()

def main():
    root = Tk()
    ex = TangoBoard(root)
    ex.pack()
    root.mainloop()


if __name__ == '__main__':
    main()