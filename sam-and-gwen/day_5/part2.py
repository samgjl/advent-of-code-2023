# import numpy as np
from tqdm import tqdm
import mac_imessage

class RangeMap:
    def __init__(self, dest: int, src: int, ran: int):
        self.src = src
        self.dest = dest
        self.range = ran

    def contains(self, inp):
        return (self.src <= inp < self.src+self.range)
    def inverse_contains(self, out):
        return (self.dest <= out < self.dest+self.range)
    def place(self, inp):
        return self.dest + (inp-self.src)   
    def inverse_place(self, out):
        return self.src + (out-self.dest)

def inverse_part2(input: list) -> int:
    oldSeeds = input[0]
    seeds: list[RangeMap] = []
    for i in range(0, len(oldSeeds), 2):
        seeds.append(RangeMap(-1, oldSeeds[i], oldSeeds[i+1]))
    maps = input[1]
    
    i = 0
    while True:
        print(i)
        out = inverse_traverseAll(maps, i)
        for seed in seeds:
            if seed.contains(out):
                return i
        i += 1
    

def inverse_traverse(maps: list[RangeMap], inp: int) -> int:
    for i in range(len(maps)):
         rangeMap: RangeMap = maps[i]
         if (rangeMap.inverse_contains(inp)):
            return rangeMap.inverse_place(inp)
    return inp

def inverse_traverseAll(maps: list[list[RangeMap]], inp: int) -> int:
    out = inp
    for map in reversed(maps):
        out = inverse_traverse(map, out)
    return out
    


def part2(input: list) -> int:
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
        # for j in range(seed, seed+ran, 1):
        for j in tqdm(range(seed, seed+ran, 1)):
            # print(j, "/", totseeds, "|", (j-seed)/ran)
            temp = traverseAll(maps, j)
            if (temp < minLoc):
                minLoc = temp
    return minLoc

def traverseAll(maps, input: int):
    out = input
    for i in range(len(maps)):
        out = traverse(maps[i], out)
    return out

def traverse(maps: list[RangeMap], input: int):
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
    import sys
    inp = "sample.txt"
    if len(sys.argv) > 1:
        inp = sys.argv[1]
    with open(inp) as f:
        inp = parseInput(f.read())

    solution = inverse_part2(inp)
    phone = "YOUR PHONE # HERE!!!!" #!  YOUR PHONE NUMBER HERE
    mac_imessage.send(
        message=f"Part 2: {solution}",
        phone_number=phone,
        medium="imessage"
    )
    # imessage.send("6264370664", f"Part 2: {solution}")
    
    print("Part 2:", inverse_part2(inp))
