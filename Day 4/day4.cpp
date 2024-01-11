#include <iostream>
#include <vector>
#include <string>
#include <list>
#include <fstream>
#include <regex>
#include <queue>
#include <tuple>

using namespace std; // Standard Library

class Day4 {
    public:
        vector<string> lines;
        vector<vector<int>> cards;
        vector<vector<int>> winningNumbers;
        // For regex parsing:
        vector<vector<string>> card_regexes;
        vector<string> winningStrings;

        // Constructors:
        Day4() { cout << "-----\nAdvent of Code, Day 4!\n-----" << endl; }
        ~Day4() { cout << "-----\nAu revoir!\n-----" << endl; }

        // Read the input file into a vector of strings, where each string is a line in the file
        vector<string> readFile(string fileName) {
            ifstream file(fileName);
            string line;
            int cardStart;
            int winStart;
            vector<string> cardStrings;

            while (getline(file, line)) {
                lines.push_back(line);
                // Split the line into the card and the winning number:
                cardStart = line.find(":");
                winStart = line.find('|');
                cardStrings.push_back(line.substr(cardStart+1, winStart-cardStart));
                winningStrings.push_back(line.substr(winStart+1, line.length()));
            } 
            // use regex to parse the ints from the strings:
            regex cardRegex("[0-9]+");
            for (int i = 0; i < lines.size(); i++) {
                // Iterators:
                sregex_iterator cardIt(cardStrings[i].begin(), cardStrings[i].end(), cardRegex);
                sregex_iterator winningIt(winningStrings[i].begin(), winningStrings[i].end(), cardRegex);
                // Add the cards to the cards vector:  
                cards.push_back(vector<int>());
                card_regexes.push_back(vector<string>());
                while (cardIt != sregex_iterator()) {
                    card_regexes[i].push_back(cardIt->str());
                    cards[i].push_back(stoi(cardIt->str()));
                    cardIt++;
                }
                sort(cards[i].begin(), cards[i].end());
                // Add the winning numbers to the winningNumbers vector:
                winningNumbers.push_back(vector<int>());
                while (winningIt != sregex_iterator()) {
                    winningNumbers[i].push_back(stoi(winningIt->str()));
                    winningIt++;
                }
                sort(winningNumbers[i].begin(), winningNumbers[i].end());           
            }
            return lines;
        }

        vector<string> checkAllWinsInLine(vector<string> card_line, string winning_line) {
            int total = 1;
            string card_regex_string = "\\b" + card_line[0] + "\\b";
            for (int i = 1; i < card_line.size(); i++) {
                card_regex_string.append("|\\b" + card_line[i] + "\\b"); // NOT WORKING CURRENTLY
            }
            regex cardRegex(card_regex_string);
            sregex_iterator winningIt(winning_line.begin(), winning_line.end(), cardRegex);
            vector<string> winningCards;
            while (winningIt != sregex_iterator()) {
                winningCards.push_back(winningIt->str());
                winningIt++;
            }

            return winningCards;
        }
        
        int checkAllWins(vector<vector<string>> card_regexes, vector<string> winning_line) {
            int total = 0;
            int subtotal;
            for (int i = 0; i < card_regexes.size(); i++) {
                subtotal = 2;
                vector<string> winningCards = checkAllWinsInLine(card_regexes[i], winning_line[i]);
                subtotal = max(pow(subtotal, winningCards.size()-1), 0);
                total += subtotal;
            }
            return total;
        }

        int max(int a, int b) { 
            int x = (a > b) ? a : b; 
            return x;
        }

        int partTwo(vector<vector<string>> card_regexes, vector<string> winning_lines) {
            // Preprocess all the lines for winners:
            int totalSeen = 0; // Do not update until we use the queue!
            vector<tuple<int, int>> indexAndWinners; // each tuple is (index, number of winners)
            for (int i = 0; i < card_regexes.size(); i++) {
                vector<string> winningCards = checkAllWinsInLine(card_regexes[i], winning_lines[i]);
                indexAndWinners.push_back(make_tuple(i, winningCards.size()));
            }

            queue <tuple<int, int>> q;
            for (int i = 0; i < indexAndWinners.size(); i++) {
                q.push(indexAndWinners[i]);
            }
            int total_length = indexAndWinners.size();
            while (!q.empty()) {
                // Get the first tuple in the queue:
                tuple<int, int> curr = q.front();
                q.pop();
                // unpack into index and winners:
                int index = get<0>(curr);
                int winners = get<1>(curr);
                // For however many winners there are (don't fall off!)
                for (int i = 1; i <= winners; i++) { 
                    // Push the next tuple into the queue:
                    if (i + index < total_length) {
                        q.push(indexAndWinners[index+i]);
                    }
                }
                // Update the total:
                totalSeen += 1;
            }
            return totalSeen;
        }
};

int main(string args[]) {
    string filename = "input.txt";
    Day4 day4 = Day4();
    day4.lines = day4.readFile(filename);
    // Part 1:
    int total = day4.checkAllWins(day4.card_regexes, day4.winningStrings);
    cout << "Part 1 | Total: " << total << endl;
    // Part 2:
    int total2 = day4.partTwo(day4.card_regexes, day4.winningStrings);
    cout << "Part 2 | Total: " << total2 << endl;
    return 0;
}