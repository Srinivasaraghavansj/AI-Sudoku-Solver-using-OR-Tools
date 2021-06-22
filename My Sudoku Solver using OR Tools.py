'''
Srinivasaraghavan Seshadhri R00195470
Decision Analytics Assignment 1 Task 2
MSc Artificial Intelligence MTU 2020-2021 
'''

from ortools.sat.python import cp_model
import numpy as np
def main():
    #Given sudoku to be solved - Copied from assignment question
    sudoku_question = [[0, 0, 0, 0, 0, 0, 0, 3, 0],
                    [7, 0, 5, 0, 2, 0, 0, 0, 0],
                    [0, 9, 0, 0, 0, 0, 4, 0, 0],
                    [0, 0, 0, 0, 0, 4, 0, 0, 2],
                    [0, 5, 9, 6, 0, 0, 0, 0, 8],
                    [3, 0, 0, 0, 1, 0, 0, 5, 0],
                    [5, 7, 0, 0, 6, 0, 1, 0, 0],
                    [0, 0, 0, 3, 0, 0, 0, 0, 0],
                    [6, 0, 0, 4, 0, 0, 0, 0, 5],]


    #Function to print sudokus in a particular format
    def print_sudoku(sudoku):
        for i in sudoku:
            print("+ - "*9+"+")
            print("| ",end = "")
            for j in i:
                print(j,end=" | ")
            print()
        print("+ - "*9+"+")

    #Printing intial sudoku to be solved
    print("\n\nSUDUKO TO BE SOLVED:")
    print_sudoku(sudoku_question)
    print()

    #Task D - Output all the solutions
    #Solutions Printer Class to print intermediate solutions
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):

        def __init__(self, variables,solver,print_sudoku):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__variables = variables
            self.__solution_count = 0
            self.__solver = solver

        def on_solution_callback(self):
            self.__solution_count += 1
            print("Solution: ",self.__solution_count)
            sudoku = []
            for i in self.__variables:
                sudoku.append(self.Value(i))
            sudoku = np.array(sudoku).reshape(9,9)
            print_sudoku(sudoku)
            print()
                
        def solution_count(self):
            return self.__solution_count

    #Initializing model and solver objects from ortools
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    #Defining lists of the dimensions of sudoku and each block ie, 9 and 3 => 9x9 & 3x3 respectively
    line,block = range(0, 9),range(0, 3)

    #Task A - Identify and create the decision variables for the Sudoku puzzle 
    #Creating IntVars for each of the element in the sudoku
    grid = {}
    for i in line:
        for j in line:
            #Task B - Constraints that specify the digits, which are already given in the puzzle specification
            grid[(i, j)] = model.NewIntVar(1, 9, 'grid %i %i' % (i, j))

    #Task C - constraints that no digit can occur twice in any of the rows, in any of the columns, or in any of the 3x3 sub-grids
    #Creating condition that All values should be Different on corresponding rows and columns
    for i in line:
        model.AddAllDifferent([grid[(i, j)] for j in line])
        model.AddAllDifferent([grid[(j, i)] for j in line])

    #Creating condition that All values should be Different on appropriate blocks
    for i in block:
        for j in block:
            one_block = [grid[(i * 3 + di, j * 3 + dj)] for di in block for dj in block] 
            model.AddAllDifferent(one_block)

    #Adding Initial values
    for i in line:
        for j in line:
            if sudoku_question[i][j]:
                model.Add(grid[(i, j)] == sudoku_question[i][j]) #Adding constraint to not modify the available/given elements in the initial sudoku

    #Collecting all IntVars in a list for ease of handling while printing
    all_vars = [grid[(i, j)] for i in line for j in line]

    #Instantiating solution printer class
    sol_print = VarArraySolutionPrinter(all_vars,solver,print_sudoku)

    # Task D - Solve the CP-SATmodel and determine how many solutionscan be found for the above instance
    #Solve for all solutions
    solver.SearchForAllSolutions(model,sol_print)
    print("The number of possible solutions are:",sol_print.solution_count())

if __name__ == "__main__":
    main()