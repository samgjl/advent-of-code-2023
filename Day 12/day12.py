import re
import sys
import tqdm
def readFile(filename: str) -> (list[str], list[list[int]]):
    content = []
    parities = []
    int_regex = re.compile(r'\d+')
    with open(filename) as f:
        content = f.readlines()
        for i in range(len(content)):
            parities.append([int(match) for match in int_regex.findall(content[i])]) # get parity info
            content[i] = content[i].split(" ")[0] # remove parity info   
    return content, parities
        
def isPossibleBranch(line: str, parity: list[int]) -> bool:
    h, q, p = line.count("#"), line.count("?"), sum(parity)
    if (h + q < p or h > p):
        return False
    return True
    
def isValidPermutation(line: str, parity: list[int]) -> int:
    parity_strings = ["#"*p for p in parity]
    for i in range(len(parity)):
        p = parity_strings[i]
        # Check beginning:
        if (line.startswith(p+".")):
            line = line.replace(p+".", "", 1)
        # Check middle (no front found):
        elif (line.find("."+p+".") != -1):
            ind = line.find("."+p+".")
            # Out of order:
            if "#" in line[:ind]:
                return 0
            # Remove parity from line:
            line = line[ind + (len("."+p+".")):] # BROKEN?
        # Check end (no middle found):
        elif (line.endswith("."+p)):
            # Out of order
            if "#" in line[:len(line) - len("."+p)] or parity[i+1:] != []:
                return 0
            else:
                return 1
        # Check identity (nothing else found):
        elif (line == p):
            line = line.replace(p, "", 1)
        # Nothing found:
        else:
            return 0
    # Final check:
    if "#" in line: 
        return 0
    return 1
    
        
def tallyPermutations(line: str, parities: list[list[int]]) -> int: 
    if (not isPossibleBranch(line, parities)):
        return 0   
    q_index = line.find("?")
    if (q_index == -1):
        # Base case:
        return isValidPermutation(line, parities)
    else:
        # Recursive case:
        if (line[:q_index].count("#") == 0):
            perm1 = line[q_index+1:]
            perm2 = "#" + line[q_index+1:]
        else:
            perm1 = line[:q_index] + "." + line[q_index+1:]
            perm2 = line[:q_index] + "#" + line[q_index+1:]
        return tallyPermutations(perm1, parities) + tallyPermutations(perm2, parities)

def unfold(lines: list[str], parities: list[list[int]]) -> (list[str], list[list[int]]):
    lines = ["?".join([line]*5) for line in lines]
    parities = [parity*5 for parity in parities]
    return lines, parities


DP = {}  
def tallyOptimized(line: str, parity: list[int]) -> int:
    # BASE CASES:
    if line == "": # Line is empty
        return 1 if len(parity) == 0 else 0
    elif len(parity) == 0: # parity is empty
        return 0 if "#" in line else 1
    # RECURSIVE CASES:
    key = (line, tuple(parity))
    if key in DP:
        return DP[key]
    
    rax = 0
    # If we could possibly put a "." in the first position:
    if line[0] in ".?":
        rax += tallyOptimized(line[1:], parity)
    # If we could possibly start a block here:
    if (line[0] in "#?"):
        # (block is not OOB) and (we don't run out of #/? before block end) and (block not too long)
        if (parity[0] <= len(line)) and ("." not in line[:parity[0]]) and ((parity[0] == len(line)) or (line[parity[0]] != "#")):
            rax += tallyOptimized(line[parity[0] + 1:], parity[1:])
    DP[key] = rax
    return rax

def count(cfg, nums):
    if cfg == "":
        return 1 if nums == () else 0

    if nums == ():
        return 0 if "#" in cfg else 1

    result = 0
    
    if cfg[0] in ".?":
        result += count(cfg[1:], nums)
        
    if cfg[0] in "#?":
        if nums[0] <= len(cfg) and "." not in cfg[:nums[0]] and (nums[0] == len(cfg) or cfg[nums[0]] != "#"):
            result += count(cfg[nums[0] + 1:], nums[1:])

    return result
            
def part1(lines: list[int], parities: list[list[int]]) -> int:
    num_permutations = 0
    for i in tqdm.tqdm(range(len(lines))):
        perm = tallyOptimized(lines[i], parities[i])
        num_permutations += perm
    return num_permutations

def part2(lines: list[int], parities: list[list[int]]) -> int:
    lines, parities = unfold(lines, parities)
    return part1(lines, parities)

if __name__ == "__main__":
    filename = "input2.txt"
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    lines, parities = readFile(filename)
    print("------ PART 1 -----")
    print(part1(lines, parities))
    print("------ PART 2 -----")
    print(part2(lines, parities))