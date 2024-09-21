/*
NEEDS:
    * file io
    * string handling
*/
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;
vector<string> converter = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

int main(int argc, char *argv[])
{

    ifstream input_file("sample.txt", ios::in);
    string line;
    int total = 0;
    if (!input_file.is_open())
    {
        cerr << "File not found" << endl;
        return 0;
    }
    while (getline(input_file, line))
    {
        cout << line << " | ";
        string numbers = "";
        for (int i = 0; i < line.length(); i++)
        {
            // TODO: Part 2 rewrite
            // TODO: Do we read exclusively L->R or do we do a two pointer approach?
            if (isdigit(line[i]))
            {
                numbers.push_back(line[i]);
            } else if (false) {

            }
        }
        int subtotal = 0;
        if (numbers.length() >= 2)
        {
            string sub = "";
            sub.push_back(numbers[0]);
            sub.push_back(numbers[numbers.length() - 1]);
            subtotal = stoi(sub);
        }
        else if (numbers.length() == 1)
        {
            subtotal = stoi(numbers + numbers);
        }
        cout << subtotal << endl;
        total += subtotal;
    }
    input_file.close();

    cout << "Total: " << total << endl;

}