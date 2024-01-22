import sys
import tqdm
import numpy as np


class Day16:
    def __init__(self, filename: str = None) -> None:
        if filename == None: return
        self.filename = filename
        with open(filename) as f:
            self.oldgrid = np.array([list(line.strip()) for line in f.readlines()])
            self.grid = self.oldgrid.copy()
            self.oldEnergy = np.array([[0]*len(self.grid[0]) for _ in range(len(self.grid))])
            self.energized = self.oldEnergy.copy()
            self.visited = [[[(0, 0)] for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
    
    def reset(self) -> None: # CRAZY OVERHEAD ON HERE FOR EACH ITERATION...
        with open(self.filename) as f:
            self.grid = self.oldgrid.copy()
            self.energized = self.oldEnergy.copy()
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
                return
            else:
                self.visited[row][col].append((drow, dcol))
            
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

    def part1(self, row=0, col=0, drow=0, dcol=1) -> int:
        self.traverse(row, col, drow, dcol) # grid[0,0], going right
        total = np.sum(self.energized)
        self.reset()
        return total
    
    def traverseFromAllSides(self) -> int:
        # Brute force, babey!
        maxEnergy = 0
        for row in tqdm.tqdm(range(len(self.grid))):
            for col in range(len(self.grid[0])):
                if row == 0 or row == len(self.grid)-1 or col == 0 or col == len(self.grid[0])-1:
                    energy = max(self.part1(row, col, 1, 0), self.part1(row, col, -1, 0), self.part1(row, col, 0, 1), self.part1(row, col, 0, -1))
                    if energy > maxEnergy:
                        maxEnergy = energy 
        return maxEnergy
    
    def part2(self) -> int:
        return self.traverseFromAllSides()
                
            
        
        
            
        
if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "input2.txt"
    day16 = Day16(filename)
    print("-----\nPart 1:")
    print(day16.part1())
    print("-----\nPart 2:")
    print(day16.part2())