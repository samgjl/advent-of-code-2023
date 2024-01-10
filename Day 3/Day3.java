import java.io.File;
import java.util.ArrayList;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Scanner;
import java.io.FileNotFoundException;

public class Day3 {
    class ParseNode {
        String data;
        boolean isValid;
        int[] position = {0, 0};

        private boolean checkNode(ArrayList<String> graph) {
            int row = position[0];
            int col = position[1];
            int len = data.length();
            // Check the immediate vicinity of the nodes:
            for (int i = row-1; i <= row+1; i++) {
                // Don't fall off:
                if (i < 0 || i >= graph.size()) continue;
                String line = graph.get(i);
                for (int j = col-1; j <= col+len; j++) {
                    // Don't fall off:
                    if (j < 0 || j >= line.length()) continue;
                    char c = line.charAt(j);
                    if (c != '.' && !Character.isDigit(c)) {
                        isValid = true;
                        return true;
                    }
                }
            }
            isValid = false;
            return false;
        }
    }
    class Gear {
        int[] position;
        ArrayList<Integer> neighbors;
        boolean isValid;

        public Gear() {
            position = new int[2];
            neighbors = new ArrayList<Integer>();
            isValid = false;
        }

        private boolean checkValidity() {
            if (neighbors.size() != 2) {
                isValid = false;
                return false;
            } else {
                isValid = true;
                return true;
            }
        }
        
        private ArrayList<Integer> findNeighbors(ArrayList<ParseNode> nodes) {
            neighbors = new ArrayList<Integer>();
            for (int i = 0; i < nodes.size(); i++) {
                ParseNode node = nodes.get(i);
                // check if the positional range of the number is within the range of the gear:
                int row = node.position[0];
                int col = node.position[1];
                int len = node.data.length();
                if (row > position[0]+1 || row < position[0]-1) continue; // Row out of bounds
                // MIGHT BE (col+len > position[1] + 1)
                if ((col > position[1]+1) || (col+len < position[1])) continue; // Col out of bounds
                // We must be in position:
                neighbors.add(Integer.parseInt(node.data));          
            }
            checkValidity();
            System.out.println("Node (" + position[0]+","+position[1] + ") | Neighbors: " + neighbors + " | Valid: " + isValid);      
            return neighbors;
        }
        
        private int getRatio() {
            if (!isValid) return 0;
            return neighbors.get(0) * neighbors.get(1);            
        }
    }

    private ArrayList<String> graph;
    private ArrayList<ParseNode> nodes;
    private ArrayList<Gear> gears;

    public Day3(String filename) {
        if (filename != null) {
            graph = fileToGraph(filename);
            nodes = new ArrayList<ParseNode>();
            gears = new ArrayList<Gear>();
        }
    }

    public static ArrayList<String> fileToGraph(String filename) {
        ArrayList<String> array = new ArrayList<String>();
        try {
            // Scan through the file:
            File file = new File(filename);
            Scanner scanner = new Scanner(file);
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                array.add(line);
            }
            scanner.close();
            return array;
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
            return null;
        }
    }

    public ArrayList<ParseNode> graphToNodes(ArrayList<String> lines) {
        ArrayList<ParseNode> nodes = new ArrayList<ParseNode>();
        Day3 day3 = new Day3(null); // empty instance of Day3
        Pattern nodePattern = Pattern.compile("([0-9]+)");
        Pattern gearPattern = Pattern.compile("([*])");


        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            // Get all numbers in the line, including the index of the first digit in each number:
            Matcher nodeMatcher = nodePattern.matcher(line);
            while (nodeMatcher.find()) {
                ParseNode node = day3.new ParseNode();
                node.data = nodeMatcher.group();
                node.isValid = false; // Temp value
                node.position[0] = i; node.position[1] = nodeMatcher.start();
                nodes.add(node);
            }
            // Get all gears in the line:
            Matcher gearMatcher = gearPattern.matcher(line);
            while (gearMatcher.find()) {
                Gear gear = day3.new Gear();
                gear.position[0] = i; gear.position[1] = gearMatcher.start();
                gears.add(gear);
            }
        }
        return nodes;
    }

    public ArrayList<ParseNode> checkNodes(ArrayList<ParseNode> nodes, ArrayList<String> graph) {
        for (int i = 0; i < nodes.size(); i++) {
            ParseNode node = nodes.get(i);
            node.checkNode(graph);
        }
        return nodes;
    }

    public ArrayList<Gear> checkGears(ArrayList<Gear> gears, ArrayList<ParseNode> nodes) {
        for (int i = 0; i < gears.size(); i++) {
            Gear gear = gears.get(i);
            gear.findNeighbors(nodes);
        }
        return gears;
    }

    public int sumValidNodes(ArrayList<ParseNode> nodes) {
        int total = 0;
        for (int i = 0; i < nodes.size(); i++) {
            ParseNode node = nodes.get(i);
            if (node.isValid) {
                total += Integer.parseInt(node.data);
            }
        }
        return total;
    }

    public int sumRatios(ArrayList<Gear> gears) {
        int total = 0;
        for (int i = 0; i < gears.size(); i++) {
            Gear gear = gears.get(i);
            total = total + gear.getRatio();
        }
        return total;
    }

    /* Prints a 2D Array (debugging purposes) */
    public static void print2DArray(ArrayList<String> array) {
        for (int i = 0; i < array.size(); i++) {
            System.out.println(array.get(i));
        }
    }

    public static void main(String[] args) {
        String filename;
        if (args.length > 0) {
            filename = args[0];
        } else {
            filename = "input2.txt";
        }
        Day3 day3 = new Day3(filename);
        day3.nodes = day3.graphToNodes(day3.graph);
        day3.checkNodes(day3.nodes, day3.graph);
        day3.checkGears(day3.gears, day3.nodes);
        System.out.println("Sum of all valid nodes: " + day3.sumValidNodes(day3.nodes));
        System.out.println("Sum of all ratios: " + day3.sumRatios(day3.gears));
    }
}