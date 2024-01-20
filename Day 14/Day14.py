import sys
import tqdm
import numpy as np

class Day14:
    def __init__(self, filename: list[str] = "input2.txt"):
        with open(filename, "r") as f:
            self.lines = [list(line.strip()) for line in f.readlines()]
            self.gridDict = {}
        
    
    def tilt(self, grid: list[list[str]], direction: (int, int), cycle = 0) -> list[list[str]]:
        # DP Attempt
        hashGrid = hash("\n".join(["".join(row) for row in grid]))
        if (hashGrid, direction) in self.gridDict:
            return self.gridDict[(hashGrid, direction)], cycle
        
        # Find all rocks, move them
        for r in range(0, len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == "O":
                    # remove rock form current spot
                    grid[r][c] = "."
                    # slide rock in a cardinal direction:
                    
                    # North/South
                    if direction[0] != 0:
                        i = r
                        while i < len(grid) and i >= 0 and grid[i][c] == ".":
                            i += direction[0]
                        grid[i-direction[0]][c] = "O"
                    # East/West
                    else:
                        i = c
                        while i < len(grid[0]) and i >= 0 and grid[r][i] == ".":
                            i += direction[1]
                        grid[r][i-direction[1]] = "O"
        
        # self.gridDict[(hashGrid, direction)] = grid    
        return grid
    
    def countNorthernWeight(self, grid: list[list[str]]) -> int:
        total = 0
        heft = len(grid)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "O":
                    total += heft - i
        return total
    
    def part1(self):
        grid = self.tilt(self.lines, direction = (-1, 0))
        return self.countNorthernWeight(grid)

    def part2(self, spins: int = 1000000000):
        grid = self.lines
        NWSE = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        # Tilt it a billion fucking times:
        i = 0
        while i < spins:
            i += 1
            for j in range(4):
                direction = NWSE[j]
                #  N -> W -> S -> E
                grid = self.tilt(grid, direction)
                
            # Try to hash:
            hashGrid = hash("\n".join(["".join(row) for row in grid]))
            # WHAT THE HELL AM I DOING HERE????
            
            # if hashGrid in self.gridDict and i + i - self.gridDict[hashGrid] <= spins:
            #     jumpAmount = i - self.gridDict[hashGrid]
            #     print(f"At {i} | Last Seen {self.gridDict[hashGrid]} | Cycle Length {jumpAmount}")
            #     i += jumpAmount
            # else:
            #     self.gridDict[hashGrid] = i
        
        return self.countNorthernWeight(grid)

    
def printMatrix(grid: list[list[str]]):
    for row in grid:
        print(row)
    

if __name__ == "__main__":
    filename = "input2.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    day14 = Day14(filename)
    print("-----\nPart 1:")
    print(day14.part1())
    print("-----\nPart 2:")
    print(day14.part2())