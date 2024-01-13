import sys
import re

class Day5:
    def __init__(self, filename: str = None):
        self.lines = []
        self.number_regex = re.compile(r'(\d+)')
        '''self.seeds = {
            SEED: {
                string (category): int (value)
            }
        }'''
        self.seeds = {}
        ''' self.categories = {
            "X-to-Y": [
                (int min, int max): int output
            ]
        }'''
        self.categories = {}
        
        self.filename = filename            
        # Parse the input file if any
        if (self.filename is not None):            
            self.parseInput(self.filename)
            
    
    def parseInput(self, filename: str, partTwo: bool = False):
        # Parse the input file
        self.lines = []
        self.seeds = {}
        self.categories = {}
        i = 0
        with open(filename, 'r') as file:
            self.lines = file.read()
            self.lines = self.lines.split('\n\n') # Splits into groups
            # parse the first line: ("seeds: number number number")
            subline = self.lines[0].split(" ")[1:]
            if (not partTwo):
                for number in subline:
                    if (number != ""):
                        self.seeds[number] = {"seed": int(number)}
                        i += 1                
            else:
                for i in range(0, len(subline), 2):
                    num1 = subline[i]
                    num2 = subline[i+1]
                    self.seeds[(num1, num2)] = {"seeds": (int(num1), int(num2))}
                
            # parse the rest of the lines:
            for category in self.lines[1:]:
                category = category.split('\n')
                cat = category[0].split(' ')[0]
                self.categories[cat] = []
                for line in category[1:]:
                    line = line.split(" ")
                    min = int(line[1])
                    max = min + int(line[2]) - 1
                    self.categories[cat].append((min, max, int(line[0]))) # (min, max, out)
    
    def Part1(self, seeds: dict = None):
        if (seeds == None):
            seeds = self.seeds
            
        # Part 1
        for cat in self.categories:
            category = self.categories[cat]
            input_name = cat.split('-')[0]
            output_name = cat.split('-')[-1]
            
            for seed in seeds:
                seed = seeds[seed]
                inp = seed[input_name]
                for min, max, out in category:
                    if (inp >= min and inp <= max):
                        seed[output_name] = out + (inp-min)
                if (output_name not in seed.keys()):
                    seed[output_name] = seed[input_name]
        
        return self.findMinDict(seeds, "location")
        
    def Part2(self):
        self.parseInput(self.filename, True)
        minSeed = None
        for seed in self.seeds:
            seed_range = self.seeds[seed]["seeds"]
            for subseed in range(seed_range[0], seed_range[0]+seed_range[1]):
                subseedDict = { subseed: {"seed": subseed}}
                self.Part1(subseedDict)
                # find minimum:
                if (minSeed is None) or (minSeed[1] > subseedDict[subseed]["location"]):
                    minSeed = (subseed, subseedDict[subseed]["location"])
        
        return minSeed
                
                
                        
                
        # return self.Part1()
        
        
                        
    def findMinDict(self, dict: dict, focusKey: str):
        minimum = None
        for key in dict:
            if (minimum is None or dict[key][focusKey] < dict[minimum[0]][focusKey]):
                minimum = (key, dict[key][focusKey])                
        return minimum
        
                
            
                    


if __name__ == "__main__":
    filename = "input2.txt"
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    day5 = Day5(filename)  
    print("Part 1:")
    print(day5.Part1())
    print("Part 2:")
    print(day5.Part2())      