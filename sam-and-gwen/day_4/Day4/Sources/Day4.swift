// The Swift Programming Language
// https://docs.swift.org/swift-book
// 
// Swift Argument Parser
// https://swiftpackageindex.com/apple/swift-argument-parser/documentation

import ArgumentParser
import Foundation

class Card: CustomStringConvertible {
    var id: Int
    var winners: [Int:Bool]
    var numbers: [Int]

    init(id: Int, winners: [Int:Bool], numbers: [Int]) {
        self.id = id
        self.winners = winners
        self.numbers = numbers
    }

    var description: String {
        return "Card \(self.id) : \(self.winners) | \(self.numbers)\n"
    }

    func calculatePoints() -> Int {
        var points = 0
        var matches = 0

        for num in numbers {
            if winners[num] != nil {
                matches += 1
                
                if matches == 1 {
                    points += 1
                } 
                else {
                    points *= 2
                }
            }
        }
        return points
    }

    func countMatches() -> Int {
        var matches = 0;
        for num in numbers {
            if winners[num] != nil {
                matches += 1
            }
        }
        return matches
    }
}

@main
struct Day4: ParsableCommand {
    @Option(help: "Specify the input file")
    public var file: String = "../sample.txt"
    @Flag(help: "Add --v to make Part 2 verbose")
    public var v: Bool = false

    mutating func run() throws {
        print("Input: '\(self.file)'")
        print("--- PART 1 ---")
        let cards = parseFile(filename: self.file)
        print("Total Cards: \(cards.count)")
        let points = part1(cards: cards)
        print("Sum: \(points)")
        print("--------------")

        print("--- PART 2 ---")
        let numCards = part2(cards: cards, verbose: v)
        print("Total produced: \(numCards)")
        print("--------------")
    }

    func part1(cards: [Card]) -> Int {
        var pts = 0
        for card in cards {
            pts += card.calculatePoints()
        }
        return pts
    }

    func part2(cards: [Card], verbose: Bool) -> Int {
        /* 
            * Every card can __only__ produce cards that come after it (and you can't fall off the list producing cards)
            * As such, we can count the total number of cards produced by induction:
                * Base case: Let our array of cards produced C be [1] (just card N alone, as it can produce nothing)
                * Inductive case (card i < N):
                    * Let M be the number of matches.
                    * Sum together the first M items in C
                    * Add this sum to the beginning of C, as it takes card i's place
            * At the end, we know that we queue up cards 1...N for counting, so we can just sum array C for our final number
        */
        var production = [Int]()
        for x in 1...cards.count {
            let i = cards.count - x
            let card = cards[i]
            var numProduced = 1 // 1 because it starts with its own existence
            let matches = card.countMatches()
            if matches > 0 {
                for j in 0...matches-1 {
                    numProduced += production[j]
                }
            }
            if verbose {
                print("Card \(card.id): \(numProduced) cards")
            }
            production.insert(numProduced, at: 0)
        }
        return production.reduce(0, +)
    }



    func parseFile(filename: String) -> [Card]{
        let input: String
        do {
            input = try String(contentsOfFile: filename, encoding: .utf8) // Read file
        } catch {
            print("FILENAME ERROR: Cannot find file '\(filename)'")
            quick_exit(0)
        }
        
        let lines = input.components(separatedBy: CharacterSet.newlines)
        var cards: [Card] = []

        for line in lines {
            if (!line.contains(":")) {continue}

            let parts = line.components(separatedBy: ":")
            
            let tempName = parts[0].components(separatedBy: " ")
            let cardName = Int(tempName[tempName.count - 1]) ?? -1 // In case of nil, make -1
            let numberPart = parts[1]
            
            let numberSets = numberPart.components(separatedBy: "|")

            let winning_nums = numberSets[0].components(separatedBy: " ").compactMap { Int($0) }
            var win_dict = [Int:Bool]()
            for n in winning_nums {win_dict[n] = true}
            let card_nums = numberSets[1].components(separatedBy: " ").compactMap { Int($0) }

            let card = Card(id: cardName, winners: win_dict, numbers: card_nums)
            cards.append(card)
        }
        return cards
    }
}
