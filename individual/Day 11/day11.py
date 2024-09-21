import numpy as np
import sys


def readInput(filename: str) -> (np.ndarray, list[(int, int)]):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        matrix = np.zeros((len(lines), len(lines[0])), dtype=int)
        galaxies = []
        for i in range(0, len(lines)):
            for j in range(0, len(lines[i])):
                if lines[i][j] == "#":
                    matrix[i, j] = 1
                    galaxies.append((i, j))
        return matrix, galaxies
    
def findShortestPaths(galaxies: list[(int, int)]) -> np.ndarray:
    confusion_matrix = np.zeros((len(galaxies), len(galaxies)), dtype=int)
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
                confusion_matrix[i, j] = abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
    return confusion_matrix

def heatExpansion(matrix: np.ndarray, galaxies: list[(int, int)], exp_multiplier = 2) -> (np.ndarray, list[(int, int)]):
    rows, columns = findHeatExpantionLocations(matrix, galaxies)
    index = len(rows) - 1
    # Expand the rows that are not occupied by galaxies
    for i in range(matrix.shape[0]-1, -1, -1):
        if index < 0:
            break
        if rows[index] == i:
            for _ in range(exp_multiplier-1):
                matrix = np.insert(matrix, i, 0, axis=0)
            index -= 1
    index = len(columns) - 1
    # Expand the columns that are not occupied by galaxies
    for i in range(matrix.shape[1]-1, -1, -1):
        if index < 0:
            break
        if columns[index] == i:
            for _ in range(exp_multiplier-1):
                matrix = np.insert(matrix, i, 0, axis=1)
            index -= 1
    row = list(np.where(matrix == 1)[0])
    col = list(np.where(matrix == 1)[1])
    new_galaxies = [(row[i], col[i]) for i in range(len(row))]
    return matrix, new_galaxies
            
def findHeatExpantionLocations(matrix: np.ndarray, galaxies: list[(int, int)]) -> (np.ndarray, np.ndarray): #  -> list[tuple[int, int]]
    rowsList = np.full(matrix.shape[0], 1, dtype=int)
    colsList = np.full(matrix.shape[1], 1, dtype=int)
    for galaxy in galaxies:
        rowsList[galaxy[0]] = 0
        colsList[galaxy[1]] = 0
    rowsList = np.where(rowsList == 1)[0]
    colsList = np.where(colsList == 1)[0]
    return rowsList, colsList

def part1(galaxies: list[(int, int)]) -> int:
    return findShortestPaths(galaxies)

def hexp2(matrix: np.ndarray, galaxies: list[(int, int)]) -> (np.ndarray, np.ndarray): #  -> list[tuple[int, int]]
    rowsList = np.full(matrix.shape[0], 1, dtype=int)
    colsList = np.full(matrix.shape[1], 1, dtype=int)
    for galaxy in galaxies:
        rowsList[galaxy[0]] = 0
        colsList[galaxy[1]] = 0
    return rowsList, colsList

def findShortestPart2(matrix: np.ndarray, galaxies: list[(int, int)], mult = 2):
    exp_rows, exp_cols = hexp2(matrix, galaxies)
    confusion_matrix = np.zeros((len(galaxies), len(galaxies)), dtype=int)
    for i in range(len(galaxies)):
        g1 = galaxies[i]
        for j in range(i+1, len(galaxies)):
            g2 = galaxies[j]
            r1, r2 = min(g1[0], g2[0]), max(g1[0], g2[0])
            c1, c2 = min(g1[1], g2[1]), max(g1[1], g2[1])
            dist = (r2-r1) + (c2-c1)
            # Find expansion locations that are between the galaxies
            for k in range(r1+1, r2):
                dist += (mult-1)*exp_rows[k]
            for k in range(c1+1, c2):
                dist += (mult-1)*exp_cols[k]        
            confusion_matrix[i, j] = dist
    return confusion_matrix

if __name__ == "__main__":
    filename = "input2.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    # PART 1
    matrix, galaxies = readInput(filename)
    matrix, galaxies = heatExpansion(matrix, galaxies)
    confusion_matrix = part1(galaxies)
    print(confusion_matrix)
    print(confusion_matrix.sum())    
    # PART 2
    m1, g1 = readInput(filename)
    confusion_matrix = findShortestPart2(m1, g1, mult=1000000)
    print(confusion_matrix)
    
    total = np.zeros(1, dtype=np.int64)    
    for i in range(len(g1)):
        for j in range(i+1, len(g1)):
            total[0] = total[0] + confusion_matrix[i, j]
    print(total)