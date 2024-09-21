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

int main(int argc, char *argv[])
{
    // if (argc < 2)
    // {
    //     cerr << "Please enter a file." << endl;
    //     return -1;
    // }
    /* Algorithm:
        1. Let total = 0
        2. For each line:
            2.a) Parse the integers from the line
            2.b) Concatenate ints together to make one number
            2.c) total += concatenated ints
        3. return total
    */

    ifstream input_file("sample.txt");
    string line;
    int total = 0;
    if (input_file.is_open()) {
        cerr << "File not found" << endl;
        return 0;
    }
    while (getline(input_file, line))
    {
        cout << line << endl;
        string numbers = "";
        for (int i = 0; i < line.length(); i++)
        {
            if (isdigit(line[i]))
            {
                numbers.push_back(line[i]);
            }
        }
        if (numbers.length() >= 2)
        {
            string sub = "";
            sub.push_back(numbers[0]);
            sub.push_back(numbers[numbers.length() - 1]);
            total += stoi(sub);
        }
        else
        {
            // parse into int, add to total
            total += stoi(numbers);
        }
    }
    input_file.close();

    cout << total << endl;    
}