import sys
import os
import numpy as np

class Day16:
    def __init__(self, filename: str = None) -> None:
        if filename == None: return
        with open(filename) as f:
            self.grid = np.array([list(line.strip()) for line in f.readlines()])
            self.energized = np.array([[0]*len(self.grid[0]) for _ in range(len(self.grid))])
            self.visited = [[[(0, 0)] for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
    
    def __str__(self) -> str:
        return '\n'.join([''.join(row) for row in self.grid])
    def printEnergy(self) -> None:
        for row in self.energized:
            print(''.join(["#" if x==1 else "." for x in row]))
    
    def traverse(self, row: int, col: int, drow: int, dcol: int) -> int:
        row_N = len(self.grid)
        col_N = len(self.grid[0])
        while 0 <= row < row_N and 0 <= col < col_N:
            # Check if this is a redundant motion:
            if (drow, dcol) in self.visited[row][col]:
                print("DEAD END", row, col, self.visited[row][col])
                return
            else:
                self.visited[row][col].append((drow, dcol))
            
            if row == 9 and col == 3: print("HERE")
            self.energized[row, col] = 1 # Energize this position
            pos = self.grid[row, col]
            # Turn if needed:
            if pos in "\\/":
                # JANKY?
                drow, dcol  = (-dcol, -drow) if pos == "/" else (dcol, drow)
            # We're at a dividor:
            elif pos == "|" and dcol != 0:
                self.traverse(row-1, col, -1, 0) # Recurse up
                self.traverse(row+1, col, 1, 0) # Recurse down
                return
            elif pos == "-" and drow != 0:
                self.traverse(row, col-1, 0, -1) # Recurse left
                self.traverse(row, col+1, 0, 1) # Recurse right
                return 
            # If ".", do nothing. 
            row, col = row + drow, col + dcol
        return

    def part1(self) -> int:
        self.traverse(0, 0, 0, 1) # grid[0,0], going right
        self.printEnergy()
        return np.sum(self.energized)
        
            
        
if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "input2.txt"
    day16 = Day16(filename)
    print(day16.part1())