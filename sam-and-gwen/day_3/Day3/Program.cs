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

            public List<(int, int)> FindAdjacentGears(List<List<char>> schema) {
                List<(int, int)> gears = new List<(int, int)>();
                for (int i = -1; i <= 1; i++) {
                    if (pos.row + i < 0 || pos.row + i >= schema.Count) continue;
                    for (int j = -1; j <= Length; j++) {
                        if (pos.col + j < 0 || pos.col + j >= schema[pos.row+i].Count) continue;
                        else if (schema[pos.row+i][pos.col+j] == '*') {
                            gears.Add((pos.row+i, pos.col+j));
                        }
                    }
                }
                return gears;
            }
        }

        static void Main(string[] args)
        {
            Console.WriteLine("--- Part 1 ---");
            List<List<char>> schema = ReadInput("sample.txt");
            List<Number> numbers = GetValidNumbers(schema);
            
            int sum1 = 0;
            foreach (Number n in numbers){
                 sum1 += n.num;
            }

            Console.WriteLine("Total part numbers: " + numbers.Count.ToString());
            Console.WriteLine("Sum: " + sum1.ToString());
            Console.WriteLine("--------------");
            /* Part 2:
                1. Find all asterisks, output a map M of {<row, col> : [adjacent numbers]} ✓
                2. For each number N :
                    2.a) get a list of N's adjacent gears: G = [(1, 2), (2, 3), ...] ✓
                    2.b) For each gear G_i in G:
                        2.c) Append the number to G_i's dictionary value
                3. sum S = 0. This is our final output.
                4. For each gear key M_i in M:
                    4.a) If the length of its mapped list == 2, multiply them together and add them to S.
                5. Output S.
            */
            Console.WriteLine("--- Part 2 ---");
            SortedDictionary<(int, int), List<Number>> gears = FindAllGears(schema);

            foreach (Number num in numbers) {
                List<(int, int)> adjacents = num.FindAdjacentGears(schema);
                foreach ((int,int) gear in adjacents){
                    gears[gear].Add(num);
                }
            }

            int gearsFound = 0;
            int sum2 = 0;
            foreach ((int,int) gear in gears.Keys.ToArray()) {
                if (gears[gear].Count == 2){
                    sum2 += (gears[gear][0].num * gears[gear][1].num);
                    gearsFound++;
                }
            }
            Console.WriteLine("Gears found: " + gearsFound.ToString());
            Console.WriteLine("Sum: " + sum2.ToString());
            Console.WriteLine("--------------");
        }

        private static List<Number> GetValidNumbers(List<List<char>> template) {
            List<List<char>> schema = Copy2DArray(template);
            List<Number> numbers = new List<Number>();
            for (int i = 0; i < schema.Count; i++)
            {
                for (int j = 0; j < schema[0].Count; j++)
                {
                    if (char.IsDigit(schema[i][j]))
                    {
                        string num = schema[i][j].ToString();
                        // Going left:
                        int col = j;
                        for (int l = 1; j-l >= 0 && char.IsDigit(schema[i][j-l]); l++) {
                            col = j-l;
                            num = schema[i][j-l] + num; // Add to the left of the num
                            schema[i][j-l] = '.';
                        }
                        // Going right:
                        for (int r = 1; j+r < schema[i].Count && char.IsDigit(schema[i][j+r]); r++) {
                            num += schema[i][j+r];
                            schema[i][j+r] = '.';
                        }

                        Number number = new Number(int.Parse(num), (i, col));
                        if (number.IsValid(schema)) {
                            numbers.Add(number);
                        }

                    }
                }
            }
            return numbers;
        }

        private static List<List<char>> Copy2DArray(List<List<char>> schema) {
            List<List<char>> copy = new List<List<Char>>();
            for (int i = 0; i < schema.Count; i++) {
                copy.Add(new List<char>());
                for (int j = 0; j < schema[0].Count; j++) {
                    copy[i].Add(schema[i][j]);
                }
            }
            return copy;
        }


        private static SortedDictionary<(int, int), List<Number>> FindAllGears(List<List<char>> schema) {
            SortedDictionary<(int, int), List<Number>> gears = new SortedDictionary<(int, int), List<Number>>();
            for (int i = 0; i < schema.Count; i++) {
                for (int j = 0; j < schema[0].Count; j++) {
                    if (schema[i][j] == '*') {
                        gears.Add((i, j), new List<Number>());
                    }
                }
            }
            return gears;
        }

        private static List<List<char>> ReadInput(string filename)
        {
            IEnumerable<string> text = File.ReadLines(filename);
            List<List<char>> schema = new List<List<char>>();
            Console.Write("Special characters: ");
            List<char> special = new List<char>();
            foreach (string line in text)
            {
                List<char> newLine = new List<char>();
                for (int i = 0; i < line.Length; i++)
                {
                    if (line[i] != '.' && !char.IsDigit(line[i]) && !special.Contains(line[i])) {
                        Console.Write(line[i]);
                        special.Add(line[i]);
                    }
                    newLine.Add(line[i]);
                }
                schema.Add(newLine);
            }
            Console.WriteLine();
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
            string special_chars = "@*$&/=-+#%";
            foreach (var item in special_chars){
                if (input == item) {
                    return true;
                }
            }
            return false;
        }
    }
}