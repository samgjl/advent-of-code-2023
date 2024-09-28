using System;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.IO;

namespace Solution
{
    class Program
    {
        private class Number
        {
            public readonly int num; // The number itself
            public readonly int Length; 
            public readonly (int row, int col) pos; // The position of the top-leftmost integer
            
            public Number(int num, (int, int) pos) {
                this.num = num;
                this.pos = pos;
                this.Length = GetLength();
            }

            private int GetLength() {
                string temp = num.ToString();
                int len = temp.Length;
                return len;
            }
            public int GetNum() {
                return num;
            }

            public bool IsValid(List<List<char>> schema) {
                for (int i = -1; i <= 1; i++) {
                    if (pos.row + i < 0 || pos.row + i >= schema.Count) continue;
                    for (int j = -1; j <= Length; j++) {
                        if (pos.col + j < 0 || pos.col + j >= schema[pos.row+i].Count) continue;
                        else if (IsSpecialCharacter(schema[pos.row+i][pos.col+j])) {
                            return true;
                        }
                    }
                }

                return false;
            }
        }

        static void Main(string[] args)
        {
            Console.WriteLine("--- Part 1 ---");
            List<List<char>> schema = ReadInput("input.txt");
            Print2DArr(schema);

            List<List<char>> copy = schema;
            List<Number> numbers = new List<Number>();
            
            for (int i = 0; i < schema.Count; i++)
            {
                for (int j = 0; j < schema[0].Count; j++)
                {
                    if (char.IsDigit(copy[i][j]))
                    {
                        string num = copy[i][j].ToString();
                        // Going left:
                        int col = j;
                        for (int l = 1; j-l >= 0 && char.IsDigit(copy[i][j-l]); l++) {
                            col = j-l;
                            num = copy[i][j-l] + num; // Add to the left of the num
                            copy[i][j-l] = '.';
                        }
                        // Going right:
                        for (int r = 1; j+r < copy[i].Count && char.IsDigit(copy[i][j+r]); r++) {
                            num += copy[i][j+r];
                            copy[i][j+r] = '.';
                        }

                        Number number = new Number(int.Parse(num), (i, col));
                        if (number.IsValid(schema)) {
                            numbers.Add(number);
                        }

                    }
                }
            }
            
            int sum = 0;
            foreach (Number n in numbers){
                 sum += n.num;
            }
            Console.WriteLine("Sum: " + sum.ToString());
        }

        private static List<List<char>> ReadInput(string filename)
        {
            IEnumerable<string> text = File.ReadLines(filename);
            List<List<char>> schema = new List<List<char>>();
            foreach (string line in text)
            {
                List<char> newLine = new List<char>();
                for (int i = 0; i < line.Length; i++)
                {
                    newLine.Add(line[i]);
                }
                schema.Add(newLine);
            }
            return schema;
        }

        public static void Print2DArr(List<List<char>> arr)
        {
            foreach (List<char> line in arr)
            {
                foreach (char c in line)
                {
                    Console.Write(c);
                }
                Console.WriteLine();
            }
        }
        public static bool IsSpecialCharacter(char input)
        {
            string special_chars = "#$@!*&+=";
            foreach (var item in special_chars){
                if (input == item) {
                    return true;
                }
            }
            return false;
        }
    }
}