
Day6 day6 = new Day6();
List<(int, int)> lines = day6.part1Parse("input.txt");
day6.printTuples(lines);
int p1 = day6.part1();
Console.WriteLine($"Part 1: {p1}");
long p2 = day6.part2();
Console.WriteLine($"Part 2: {p2}");
