using System.IO;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

public class Day6 {
    // Public variables    
    List<(int, int)> races = new List<(int, int)>(); // (time, distance to beat)
    
    public List<(int, int)> part1Parse(string filename) {
        // 2D list of ints:
        List<List<int>> list2D = new List<List<int>>();
        // Open the file:
        using (StreamReader stream = new StreamReader(filename)) {
            while (!stream.EndOfStream) {
                string line = stream.ReadLine();
                // Split the line:
                string[] split = line.Split(' ');
                // Add the line to the list:
                list2D.Add(new List<int>());
                for (int i = 1; i < split.Length; i++) {
                    string s = split[i];
                    if (s != ""){
                        list2D[list2D.Count - 1].Add(int.Parse(s));
                    }
                }
            }
        }
        // Convert 2D list into tuple of races:
        for (int col = 0; col < list2D[0].Count; col++) {
            (int, int) race = (list2D[0][col], list2D[1][col]);
            this.races.Add(race);
        }
        return this.races;
    }

    public (long, long) part2Parse(string filename) {
        long time = 0; long distance = 0;
        using (StreamReader stream = new StreamReader(filename)) {
            // Line 1:
            string line = stream.ReadLine();
            line = line.Replace("Time:", "").Replace(" ", "");
            time = long.Parse(line);
            line = stream.ReadLine();
            line = line.Replace("Distance:", "").Replace(" ", "");
            distance = long.Parse(line);
        }
        return (time, distance);
    }

    public void printTuples(List<(int, int)> list) {
        foreach ((int, int) tuple in list) {
            Console.WriteLine(tuple);
        }
    }

    public int part1() {
        int total = bruteForce(this.races[0]);
        for (int r = 1; r < this.races.Count; r++)total = total * bruteForce(this.races[r]);
        return total;
    }
    public long part2() {
        (long, long) race = part2Parse("input.txt");
        return bruteForce2(race);
    }

    public int bruteForce((int, int) race) {
        int time = race.Item1; int distance = race.Item2;
        int firstNum = 0; int lastNum = 0;

        for (int i = 0; i <= time; i++) {
            if (i * (time - i) > distance) {
                firstNum = i;
                break;
            }
        }
        for (int i = time; i >= 0; i--) {
            if (i * (time - i) > distance) {
                lastNum = i;
                break;
            }
        }
        return lastNum - firstNum + 1;
    }

    public long bruteForce2((long, long) race) {
        long time = race.Item1; long distance = race.Item2;
        long firstNum = 0; long lastNum = 0;

        for (long i = 0; i <= time; i++) {
            if (i * (time - i) > distance) {
                firstNum = i;
                break;
            }
        }
        for (long i = time; i >= 0; i--) {
            if (i * (time - i) > distance) {
                lastNum = i;
                break;
            }
        }
        return lastNum - firstNum + 1;
    }
}