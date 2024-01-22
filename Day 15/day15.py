import sys
import tqdm

class Day15:
    
    def __init__(self, filename = "input2.txt"):
        self.parseInput(filename)
        self.HASHMAP = {i:[] for i in range(256)}
    
    def parseInput(self, filename) -> list[str]:
        # Example: rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        with open(filename) as f:
            self.lines = f.read().strip("\n").split(",")
        return self.lines
            
    def HASH(self, s: str) -> int:
        if len(s) == 0: return 0
        # HASH algo:
        total = 0
        for c in s:
            # Add ASCII val -> Multiply by 17 -> mod 256
            total = ((total + ord(c)) * 17) % 256
        return total

    def part1(self, lines: list[str] = None) -> int:
        lines = lines if lines != None else self.lines
        total = 0
        for i in tqdm.tqdm(range(len(lines))):
            total += self.HASH(lines[i])
        return total

    def findInList(self, l: list[int], key: str) -> int:
        for i in range(len(l)):
            if l[i][0] == key:
                return i
        return -1
    
    def updateMap(self, s: str) -> None:
        op = "=" if s.find("=") != -1 else "-" # What operation is being done?
        str_k = s.split(op)[0] # key, before "="/"-", string
        key = self.HASH(str_k) # key, hashed before "="/"-". Guaranteed to be in hashmap
        val = int(s.split(op)[1]) if op == "=" else None # value, after "="/"-", integer
        # If the operation is "=", then:
        # a. If the val is already in the key's list, swap values.
        # b. Otherwise, append the val to the END of the key's list.
        index = self.findInList(self.HASHMAP[key], str_k)
        if op == "=":
            if index != -1:
                self.HASHMAP[key][index][1] = val
            else:
                self.HASHMAP[key].append([str_k, val])
        # If the operation is "-", then:
        # a. If the val is already in the key's list, remove it.
        # b. Otherwise, do nothing.
        elif index != -1:
            self.HASHMAP[key].pop(index)
        
    def part2(self, lines: list[str] = None) -> int:
        lines = lines if lines != None else self.lines
        for i in tqdm.tqdm(range(len(lines))):
            self.updateMap(lines[i])
        # Sum together the boxes in the hashmaps (only their first values)
        total = 0
        for box in self.HASHMAP:
            subtotal = 0
            for i in range(len(self.HASHMAP[box])):
                subtotal += self.HASHMAP[box][i][1] * (i+1)
            total += (subtotal * (box+1))
        return total
        

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "input2.txt"
    day15 = Day15(filename)
    print("-----\nPart 1:")
    print(day15.part1())
    print("-----\nPart 2:")
    print(day15.part2())
    print("-----")