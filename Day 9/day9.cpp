#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <regex>
#include <algorithm>
#include <map>
#include <numeric>

using namespace std;

class Day9 {
    public:
        vector<string> histories = vector<string>();
        vector<vector<int>> numbers = vector<vector<int>>();

        /* Constructors: */
        Day9(string filename = "None") {
            cout << "-----\nAdvent of Code, Day 9!\n-----" << endl;
            if (filename != "None") readFile(filename);
        }
        ~Day9() { cout << "-----\nAu revoir!\n-----" << endl; }

        /* Read input into 2D int vector and 1D string vector */
        vector<vector<int>> readFile(string filename) {
            cout << "Reading file: " << filename << endl;
            ifstream file(filename); string line;
            regex numberRegex("[+-][0-9]+|[0-9]+");
            while (getline(file, line)) {
                histories.push_back(line);
                // Parse the numbers from the line:
                vector<int> subNumbers = vector<int>();
                sregex_iterator numberIterator(line.begin(), line.end(), numberRegex);
                while (numberIterator != sregex_iterator()) {
                    subNumbers.push_back(stoi(numberIterator->str()));
                    numberIterator++;
                }
                numbers.push_back(subNumbers);
            }
            return numbers;
        }

        /* Part 1: predict all next values in the 2D vector, then sum them*/
        int part1(vector<vector<int>> numbers) {
            int total = 0;
            for (int i = 0; i < numbers.size(); i++) {
                int next = predictNext(numbers[i]);
                numbers[i].push_back(next);
                total += next;
            }
            return total;
        }

        /* For an int vector, predict the next value */
        int predictNext(vector<int> numbers) {
            vector<vector<int>> vec2D = vector<vector<int>>();
            vec2D.push_back(numbers);
            // Build downwards:
            int i = 0;
            while (!allZeroes(vec2D[i])) {
                vector<int> diffs = vector<int>();
                for (int j = 0; j < vec2D[i].size()-1; j++) {
                    diffs.push_back(vec2D[i][j+1] - vec2D[i][j]);
                }
                vec2D.push_back(diffs);
                i++;
            }
            // Build upwards:
            for (int i = vec2D.size()-1; i > 0; i--) {
                int next = vec2D[i][vec2D[i].size()-1] + vec2D[i-1][vec2D[i-1].size()-1];
                vec2D[i-1].push_back(next);
            }
            return vec2D[0][vec2D[0].size()-1];
        }
        /* Check if a vector is all zeroes */
        bool allZeroes(vector<int> vec) {
            for (int i = 0; i < vec.size(); i++) if (vec[i] != 0) return false;
            return true;
        }

        /* Part 2: */
        int part2(vector<vector<int>> numbers) {
            for (int i = 0; i < numbers.size(); i++) reverse(numbers[i].begin(), numbers[i].end()); // Reverse the numbers
            return part1(numbers); // Do part 1 again lmao:
        }
};

/* MAIN */
int main(int argc, char* argv[]) {
    // Basic setup:
    string filename = "input.txt";
    if (argc > 1) filename = argv[1];
    Day9 day9 = Day9(filename);
    // Solutions:
    cout << "--- Part 1 ---" << endl;
    cout << "Output: " << day9.part1(day9.numbers) << endl;
    cout << "--- Part 2 ---" << endl;
    cout << "Output: " << day9.part2(day9.numbers) << endl;
    return 0;
}