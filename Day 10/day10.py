from dataclasses import dataclass
import numpy as np
import queue as q
import sys

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
directionMap = {
    "-": [EAST, WEST],
    "|": [NORTH, SOUTH],
    "L": [NORTH, EAST],
    "J": [NORTH, WEST],
    "7": [SOUTH, WEST],
    "F": [SOUTH, EAST],
    ".": [], "S": [NORTH, SOUTH, EAST, WEST]
}

@dataclass
class BFSNode:
    pos: tuple[int, int]
    dist: int
@dataclass
class DFSNode:
    pos: tuple[int, int]
    path: list[tuple[int, int]]

def readLines(filename: str = "input2.txt") -> (list[str], tuple[int, int]):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines, findStart(lines)

# Returns (row, col), or (-1, -1) if not found
def findStart(lines: list[str]) -> tuple[int, int]:
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "S":
                return (i, j)
    return (-1, -1)

def canGo(lines: list[str], pos: tuple[int, int], dir: tuple[int, int]) -> bool:
    rows, cols = len(lines), len(lines[0])
    newPos = (pos[0] + dir[0], pos[1] + dir[1])
    # Out of bounds?
    if (newPos[0] < 0 or newPos[0] >= rows or newPos[1] < 0 or newPos[1] >= cols): return False
    # Connecting pipe?
    if ((dir[0]*-1, dir[1]*-1) not in directionMap[lines[newPos[0]][newPos[1]]]): return False
    # Ground?
    return (lines[newPos[0]][newPos[1]] != ".")

def pipeBFS(lines: list[str], startPos: tuple[int, int]) -> np.ndarray:
    rows, cols = len(lines), len(lines[0])
    posArray = np.full((rows, cols), -1, dtype=int)
    queue = q.Queue()
    queue.put(BFSNode(startPos, 0))
    while (not queue.empty()):
        node = queue.get()
        pos = node.pos
        dist = node.dist
        # Visited / Invalid?
        if ((posArray[pos] != -1) or (lines[pos[0]][pos[1]] == ".")): continue
        # Set distances
        posArray[pos] = dist
        directions = directionMap[lines[pos[0]][pos[1]]]
        for dir in directions:
            newPos = (pos[0] + dir[0], pos[1] + dir[1])
            if (canGo(lines, pos, dir)): queue.put(BFSNode(newPos, dist + 1))
    return posArray

def findLongestLoop(lines: list[str], start: tuple[int, int]) -> np.ndarray:
    # Perform a DFS to find the longest loop
    rows, cols = len(lines), len(lines[0])
    stack = q.LifoQueue()
    stack.put(DFSNode(start, []))
    visited = np.full((rows, cols), False, dtype=bool)
    longest = []
    while not stack.empty():
        node = stack.get()
        pos = node.pos
        # Check if this is a dead end / visited
        if lines[pos[0]][pos[1]] == "." or visited[pos]: continue
        # Visit node:
        visited[pos] = True
        path = node.path
        path.append(pos)
        directions = directionMap[lines[pos[0]][pos[1]]]
        for dir in directions:
            newPos = (pos[0] + dir[0], pos[1] + dir[1])  
            # Check if this is a loop
            if newPos == start and len(path) > len(longest):
                longest = path + [start]
            elif canGo(lines, pos, dir):
                stack.put(DFSNode(newPos, path[:]))        
        
    # Create a list of strings to represent the longest loop:
    loopArr = np.full((rows, cols), ".", dtype=str)
    for pos in longest: loopArr[pos] = lines[pos[0]][pos[1]]
    return loopArr

def findNodesInsideLoop(loop: np.ndarray) -> (int, np.ndarray):
    rows, cols = loop.shape
    limiter = rows if rows < cols else cols # The loop is always a square
    totalArr = np.full((rows, cols), 0, dtype=int)
    total = 0
    for row, line in enumerate(loop):
        for col, char in enumerate(line):
            if char != ".": continue
            # Check if this is enclosed by the loop (Raycasting!)
            numCrosses = 0
            drow, dcol = 0, 0
            while row+drow < rows and col+dcol < cols:
                c = loop[row+drow, col+dcol] # char at diagonal
                if c != "." and c != "L" and c != "7":
                    numCrosses += 1
                drow += 1
                dcol += 1
            # If we have an odd number of crosses, this is inside the loop
            if numCrosses % 2 == 1:
                totalArr[row, col] = 1
                total += 1
    return total, totalArr

def part2(lines: list[str], startPos: tuple[int, int]) -> int:
    loop = findLongestLoop(lines, startPos)
    numInside, _ = findNodesInsideLoop(loop)
    return numInside
                
    
    

''' IDEATION FOR PART 2:
    1. Find the longest loop in the graph (put it in 2D array) -> DONE
    2. Find out which nodes are enclosed by the loop
        How do I do this while allowing the squeezing between pipes?
        - Perhaps use some primitive raycasting?
        - PRIMITIVE RAYCASTING MY BELOVED
         
'''

def part1(lines: list[str]) -> int:
    startPos = findStart(lines)
    posArray = pipeBFS(lines, startPos)
    return posArray.max()

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "input2.txt"
    lines, startPos = readLines(filename)
    print("-----\nPART 1:")
    print(part1(lines))
    print("-----\nPART 2:")
    print(part2(lines, startPos))
    
    