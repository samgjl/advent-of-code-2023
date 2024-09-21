import numpy as np
import sys
import tqdm

def read_input(filename: str) -> np.ndarray:
    with open(filename, "r") as f:
        lines = f.read().split("\n\n")
        for i in range(len(lines)):
            lines[i] = np.array([[char for char in line] for line in lines[i].split("\n")])
    return lines
         
         
def validReflection(line: str, ref: int) -> bool:
    # Edge cases:
    if ref == 0:
        return False
    i = 0.5 # "ref" is between line indices
    while ref-i >= 0 and ref+i < len(line):
        if line[int(ref-i)] != line[int(ref+i)]:
            # Eat the greedy swap if possible:
            return False
        i += 1
    # return whether or not we used the swap
    return True

def findReflections(lines) -> list[int]:    
    indices = []
    for i in range(len(lines[0])):
        check = 0
        for line in lines:
            if validReflection(line, i):
                check += 1
        if check == len(lines):
            indices.append(i)
    return indices               
    
def part1(lines: list[str]) -> int:
    horizontal_flips = []
    vertical_flips = []
    for i in tqdm.tqdm(range(len(lines)), desc="Finding reflections"):
        horizontal_flips += findReflections(lines[i])
        vertical_flips += findReflections(np.rot90(lines[i]))
    return sum(horizontal_flips) + 100*sum(vertical_flips)

def findDifference(arr1: list, arr2: list):
    # Must be a difference:
    if len(arr2) > len(arr1):
        return True
    # Either arr1 is empty, then there's no diff, 
    # or arr1 is full, then we only removed elements (handled in or statement)
    elif len(arr2) == 0:
        return False
    arr1.sort()
    arr2.sort()
    for i in range(len(arr2)):
        if arr1[i] != arr2[i]:
            return True

# Brute force approach:
def findReflectionsPart2(lines) -> list[list[int], list[int]]:
    originalHoriz = findReflections(lines)
    originalVert = findReflections(np.rot90(lines))
    for a in range(len(lines)):
        for b in range(len(lines[0])):
            # Create a new matrix with the proposed swap:
            newLines = np.copy(lines)
            if newLines[a, b] == "#":
                newLines[a, b] = "."
            else:
                newLines[a, b] = "#"
            # Find the new reflections:
            horiz = findReflections(newLines)
            vert = findReflections(np.rot90(newLines))
            # If either has a difference, we found a swap:
            if findDifference(originalHoriz, horiz) or findDifference(originalVert, vert):
                # We no longer want the old reflections:
                for item in originalHoriz:
                    if item in horiz:
                        horiz.remove(item)
                for item in originalVert:
                    if item in vert:
                        vert.remove(item)
                return [horiz, vert]
    return [[], []]
            

def part2(lines: list[str]) -> int:
    horizontal_flips = []
    vertical_flips = []
    for i in tqdm.tqdm(range(len(lines)), desc="Finding reflections"):
        l = findReflectionsPart2(lines[i])
        horizontal_flips += l[0]
        vertical_flips += l[1]
    return sum(horizontal_flips) + 100*sum(vertical_flips)

# PART 2 IDEA:
# Greedy algorithm:
# # For each tile:
# # # TileSwapUsed = False
# # # For each index:
# # # # 
    
if __name__ == "__main__":
    filename = "input2.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    lines = read_input(filename)
    print("-----\nPart 1")
    print("Answer: ", part1(lines))
    print("-----\nPart 2")
    print("Answer: ", part2(lines))