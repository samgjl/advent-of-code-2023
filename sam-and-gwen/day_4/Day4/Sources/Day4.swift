// The Swift Programming Language
// https://docs.swift.org/swift-book
// 
// Swift Argument Parser
// https://swiftpackageindex.com/apple/swift-argument-parser/documentation

import ArgumentParser
import Foundation

class Card: CustomStringConvertible {
    var id: String
    var winners: [Int:Bool]
    var numbers: [Int]

    init(id: String, winners: [Int:Bool], numbers: [Int]) {
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
}

@main
struct Day4: ParsableCommand {
    @Option(help: "Specify the input")
    public var file: String = "sample.txt"

    mutating func run() throws {
        print("Input: '\(self.file)'")
        let cards = parseFile(filename: self.file)
        let winArr = part1(cards: cards)
        print("--- PART 1 ---\nTotal Cards: \(cards.count)\nSum: \(winArr.reduce(0, +))\n--------------")

        var queue = [Int]()
        
    }

    func part1(cards: [Card]) -> [Int] {
        var sum = 0
        var winArr = [Int]()
        for card in cards {
            winArr.append(card.calculatePoints())
        }
        return winArr
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
            
            let cardName = parts[0]
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
