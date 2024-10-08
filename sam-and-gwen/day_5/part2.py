# import numpy as np
# from tqdm import tqdm

class RangeMap:
    def __init__(self, dest: int, src: int, ran: int):
        self.src = src
        self.dest = dest
        self.range = ran

    def contains(self, inp):
        return (self.src <= inp < self.src+self.range)
    def place(self, inp):
        return self.dest + (inp-self.src)    

def part2(input: str) -> int:
    p1Seeds = input[0]
    seeds = []
    maps = input[1]

    for i in range(0, len(p1Seeds), 2):
        seeds.append((p1Seeds[i], p1Seeds[i+1])); # list of (<base seed>, <range>)

    minLoc = float('inf')
    totseeds = sum([s[1] for s in seeds])
    print("Total seeds:", len(seeds), "| Total subseeds:", totseeds)
    for i in range(len(seeds)):
        seed = seeds[i][0]
        ran = seeds[i][1]
        for j in range(seed, seed+ran, 1):
        # for j in tqdm(range(seed, seed+ran, 1)):
            print(j, "/", totseeds, "|", (j-seed)/ran)
            temp = traverseAll(maps, j)
            if (temp < minLoc):
                minLoc = temp
    return minLoc

def traverseAll(maps, input: int):
    out = input
    for i in range(len(maps)):
        out = traverse(maps[i], out)
    return out

def traverse(maps, input: int):
    for i in range(len(maps)):
         rangeMap = maps[i]
         if (rangeMap.contains(input)):
            return rangeMap.place(input)
    return input

def parseInput(text: str):
    text = text.replace(r"r?\n/g", "\n")
    maps = text.split("\n\n")
    seeds = maps.pop(0)
    seeds = [int(x) for x in seeds.split("seeds: ")[1].split(" ")] # turns each seed into an int
    maps = [
        [
            
            RangeMap(*[int(x) for x in line.split(" ")])
            for line in map.split("\n")[1:]
        ]
        for map in maps
    ]
    
    return seeds, maps


if __name__ == "__main__":
    with open("input.txt") as f:
        inp = parseInput(f.read())
    
    print("Part 2:", part2(inp))
