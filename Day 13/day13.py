import numpy as np
import sys
import math

def read_input(filename: str) -> np.ndarray:
    with open(filename, "r") as f:
        lines = f.read().replace("#", "1").replace(".", "0").split("\n\n")
        for i in range(len(lines)):
            lines[i] = np.array([[int(item) for item in l] for l in lines[i].split("\n")])
    return lines

def isValidFlip(tile: np.ndarray, ref: float) -> bool:
    print(ref)
    ref = math.ceil(ref)
    print(tile)
    if ref > tile.shape[0]/2: # Over halfway
        t2 = tile[ref:] # second half
        t1 = tile[ref-t2.shape[0]:ref] # first half
    else:
        t1 = tile[:ref]# first half
        t2 = tile[ref:ref+t1.shape[0]] # second half
    return np.array_equal(t1, np.fliplr(t2))

def findHorizontalReflections(tiles: np.ndarray):
    indices = np.zeros((tiles.shape[0]), dtype=np.float32)
    for i in range(tiles.shape[1]-1):
        check = 0
        for j in range(tiles.shape[0]):
            if isValidFlip(tiles[j,:], i+.5):
                check += 1
        if check == tiles.shape[1]:
            indices[i] = i+.5
    print(indices)
    return indices
    
        

if __name__ == "__main__":
    filename = "input2.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    lines = read_input(filename)
    for i in range(len(lines)):
        horizontal_flips = findHorizontalReflections(lines[i])