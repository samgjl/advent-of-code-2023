import re
import numpy as np
import sys

class Day7:
    def __init__(self, filename: str) -> None:
        with open(filename) as f:
            self.lines = f.read().upper().splitlines()
        self.lines = [line.split(" ") for line in self.lines]
        '''Structure:
        [
            (cards, bid),
            (cards, bid),
            ...
        ]'''
        self.lines = [(line[0], int(line[1])) for line in self.lines]
        ''' Used for ranking cards.'''
        self.cardDict = {
            "A": 0xe, "K": 0xd, "Q": 0xc, "J": 0xb,
            "T": 0xa, "9": 0x9, "8": 0x8, "7": 0x7, 
            "6": 0x6, "5": 0x5, "4": 0x4, "3": 0x3, 
            "2": 0x2 
        }
        self.cardDictPart2 = {
            "A": 0xe, "K": 0xd, "Q": 0xc, "J": 0x1,
            "T": 0xa, "9": 0x9, "8": 0x8, "7": 0x7, 
            "6": 0x6, "5": 0x5, "4": 0x4, "3": 0x3, 
            "2": 0x2 
        }
            
    def part1(self) -> int:
        # Sort self.lines using the compare() function that I'll define below.
        lines = [self.hashCard(line) for line in self.lines]
        lines.sort(key=lambda x: x[0])
        total = 0
        for i in range(len(lines)):
            # print(f"{lines[i][1]} * {i+1}")
            print(f"Hex: {hex(lines[i][0])} | Bid: {lines[i][1]} | Rank: {i+1}")
            total += (lines[i][1] * (i+1))
        return total
    
    def hashCard(self, cardSet: (str, int)) -> (int, int): # returns (hash, bid)
        cards = cardSet[0]
        pairs, of_a_kind = 0, 0
        # Check for pairs using regex:
        for key in self.cardDict:
            found = re.findall(r'('+key+r')', cards)
            numFound = len(found)
            if numFound == 2:
                pairs += 1
            elif numFound > 2:
                of_a_kind = numFound
        # Hash:
        total = 0x0
        for char in cards:
            total *= 0x10
            total += self.cardDict[char]
        # Hash based on of-a-kind vs. pairs
        total += 0x100000 * pairs
        total += 0x1000000 * of_a_kind
        return (total, cardSet[1])
    
    def part2(self) -> int:
        # Sort self.lines using the compare() function that I'll define below.
        lines = [self.p2Hash(line) for line in self.lines]
        lines.sort(key=lambda x: x[0])
        total = 0
        for i in range(len(lines)):
            total += (lines[i][1] * (i+1))
        return total

    def p2Hash(self, cardSet: (str, int)) -> (int, int):
        cards = cardSet[0]
        cardsWithJokers = self.replaceJokers(cards)
        pairs, of_a_kind = 0, 0
        most_popular = (None, 1)
        # Check for pairs using regex:
        for key in self.cardDictPart2:
            found = re.findall(r'('+key+r')', cardsWithJokers)
            numFound = len(found)
            if numFound == 2:
                pairs += 1
            elif numFound > 2:
                of_a_kind = numFound
            if numFound > most_popular[1]:
                most_popular = (key, numFound)
        # Hash:
        total = 0x0
        for char in cards:
            total *= 0x10
            total += self.cardDictPart2[char]
        # Hash based on of-a-kind vs. pairs
        total += 0x100000 * pairs
        total += 0x1000000 * of_a_kind
        return (total, cardSet[1])
    
    def replaceJokers(self, cards: str) -> str:
        most_popular = ("J", 0)
        for char in cards:
            found = len(re.findall(r'('+char+r')', cards))
            if found > most_popular[1] and char != "J":
                most_popular = (char, found)
        return cards.replace("J", most_popular[0])
        
        
    
if __name__ == "__main__":
    filename = "input2.txt"
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    day7 = Day7(filename)
    # print(day7.part1())   
    print(day7.part2()) 