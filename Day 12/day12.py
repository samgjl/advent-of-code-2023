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
        
        
def isValidPermutation(line: str, parity: list[int]) -> int:
    # make regular expressions for each parity:
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
    q_index = line.find("?")
    if (q_index == -1):
        # Base case:
        return isValidPermutation(line, parities)
    else:
        # Recursive case:
        perm1 = line[:q_index] + "." + line[q_index+1:]
        perm2 = line[:q_index] + "#" + line[q_index+1:]
        return tallyPermutations(perm1, parities) + tallyPermutations(perm2, parities)

def unfold(lines: list[str], parities: list[list[int]]) -> (list[str], list[list[int]]):
    for i in range(len(lines)):
        lines[i] = ((lines[i]+"?")*5)[:-1]
        parities[i] = parities[i]*5
    return lines, parities
    
            
def part1(lines: list[int], parities: list[list[int]]) -> int:
    num_permutations = 0
    for i in tqdm.tqdm(range(len(lines))):
        perm = tallyPermutations(lines[i], parities[i])
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
    # print("------ PART 1 -----")
    # print(part1(lines, parities))
    print("------ PART 2 -----")
    print(part2(lines, parities))