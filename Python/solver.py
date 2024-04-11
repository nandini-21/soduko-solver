#!/usr/bin/env python3
import sys
import numpy as np

SUDOKU_LEN = 9
BLOCK_LEN = np.sqrt(SUDOKU_LEN)

NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

class SudokuSolver:
    """
    This class maintains a sudoku and contains logic to solve it.
    """
    def __init__(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as sudoku_file:
            self.starting_sudoku = [list(map(int, line.split())) for line in sudoku_file.readlines()]
        self.sudoku = np.array(self.starting_sudoku)
        self.num_iters = 0

    def print_sudoku(self):
        """Prints the sudoku in its current state."""
        for line in self.sudoku:
            print(line)

    def _is_valid(self, i, j, num):
        if np.any(self.sudoku[i, :] == num) or np.any(self.sudoku[:, j] == num):
            return False

        i0 = i // BLOCK_LEN
        j0 = j // BLOCK_LEN
        if np.any(self.sudoku[int(BLOCK_LEN * i0) : int(BLOCK_LEN * (i0 + 1)), int(BLOCK_LEN * j0) : int(BLOCK_LEN * (j0 + 1))] == num):
            return False
        return True

    def _has_no_unassigned_box(self):
        return np.sum(np.count_nonzero(self.sudoku, axis=1)) == SUDOKU_LEN ** 2

    def solve(self):
        """
        Main logic of the class, to recursively solve the sudoku using backtracking.
        """
        self.num_iters += 1
        for row in range(SUDOKU_LEN):
            for col in range(SUDOKU_LEN):
                if self.sudoku[row][col] == 0:
                    for num in NUMS:
                        if self._is_valid(row, col, num):
                            self.sudoku[row][col] = num
                            if self.solve():
                                return True
                            self.sudoku[row][col] = 0
                    return False
        return True



# Filepath of the Sudoku text file must be supplied as a command line argument.
def main():
    """Main function"""
    args = sys.argv[1:]
    filepath = args[0]
    solver = SudokuSolver(filepath)

    print("-------------------------------")
    print("Initial Sudoku: \n")
    for row in solver.sudoku:
        print(row)
    print("-------------------------------")

    solver.solve()

    print("-------------------------------")
    print("Solved Sudoku: \n")
    for row in solver.sudoku:
        print(row)
    print("-------------------------------")
    print(f"Number of iterations to solve: {solver.num_iters}")

main()
