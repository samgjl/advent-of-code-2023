#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

int main(int argc, char *argv[])
{
    string converter[] = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

    ifstream input_file("input.txt", ios::in);
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
            if (isdigit(line[i]))
            {
                numbers.push_back(line[i]);
            }
            else
            {
                int start = i;
                int num = -1;
                for (int j = 0; start + j < line.length(); j++)
                {
                    string *it = find(begin(converter), end(converter), line.substr(start, j + 1));
                    if (it != end(converter))
                    {
                        num = it - begin(converter);
                    }
                }
                if (num != -1)
                {
                    numbers += to_string(num);
                }
            }
        }
        int subtotal = 0;
        if (numbers.length() >= 2)
        {
            string sub = "";
            sub.push_back(numbers[0]);
            sub.push_back(numbers[numbers.length() - 1]);
            // cout << numbers << endl;
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