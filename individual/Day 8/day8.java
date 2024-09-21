import java.util.HashMap;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class day8 {
    HashMap<String, String[]> tree; 
    String root = "AAA";
    ArrayList<String> part2Array = new ArrayList<String>();
    String directions;   

    public HashMap<String, String[]> buildBinaryTree(String filename) {
        tree = new HashMap<String, String[]>();
        try {
            File file = new File(filename);
            Scanner scanner = new Scanner(file);
            Pattern pattern = Pattern.compile("([A-Z]|[0-9])([A-Z]|[0-9])([A-Z]|[0-9])");
            directions = scanner.nextLine().strip();

            while (scanner.hasNextLine()) {
                String line = scanner.nextLine().trim();
                if (line == "") continue; // skip "\n"
                // Get the parent and children:
                Matcher matcher = pattern.matcher(line);
                String[] split = new String[3];
                for (int i = 0; matcher.find(); i++) {
                    split[i] = matcher.group();
                }
                // Assign the parent and children to the tree:
                String parent = split[0];
                String[] children = {split[1], split[2]};
                tree.put(parent, children);
                if (parent.charAt(2) == 'A') {
                    part2Array.add(parent);
                }
            }
            scanner.close();
        } catch (Exception e) {
            System.out.println("Error: " + e);
        }
        return tree;
    }

    /* QUESTION: Begin with the first node or with AAA ?
     * * Tentative answer: AAA
      */
    private int findZZZ(HashMap<String, String[]> tree, String root) {
        int numSeen = 0;
        int index = 0;
        String current = root;
        while (!current.equals("ZZZ")) {
            String[] children = tree.get(current);
            if (directions.charAt(index) == 'L') current = children[0];
            else if (directions.charAt(index) == 'R') current = children[1];
            else System.out.println("Error: directionIndex is not L or R");
            index = (index + 1) % directions.length();
            numSeen++;
        }
        return numSeen;
    }
    public int part1(HashMap<String, String[]> tree, String root) {
        return findZZZ(tree, root);
    }

    private long findZZZAsGhost(HashMap<String, String[]> tree) {
        int size = part2Array.size();
        long lcm;
        int[] distances = new int[size];
        for (int i = 0; i < size; i++) {
            distances[i] = subZZZGhost(tree, part2Array.get(i));
        }
        lcm = lcm_of_array_elements(distances);      
        return lcm;
    }

    private long lcm_of_array_elements(int[] element_array){
        long lcm_of_array_elements = 1;
        int divisor = 2;
        while (true) {
            int counter = 0;
            boolean divisible = false;
            for (int i = 0; i < element_array.length; i++) {
                if (element_array[i] == 0) {
                    return 0;
                }
                else if (element_array[i] < 0) {
                    element_array[i] = element_array[i] * (-1);
                }
                if (element_array[i] == 1) {
                    counter++;
                }
                if (element_array[i] % divisor == 0) {
                    divisible = true;
                    element_array[i] = element_array[i] / divisor;
                }
            }
            if (divisible) {
                lcm_of_array_elements = lcm_of_array_elements * divisor;
            }
            else {
                divisor++;
            }
            if (counter == element_array.length) {
                return lcm_of_array_elements;
            }
        }
    }

    private int subZZZGhost(HashMap<String, String[]> tree, String root) {
        int numSeen = 0;
        int index = 0;
        String current = root;
        while (current.charAt(2) !='Z') {
            String[] children = tree.get(current);
            if (directions.charAt(index) == 'L') current = children[0];
            else if (directions.charAt(index) == 'R') current = children[1];
            else System.out.println("Error: directionIndex is not L or R");
            index = (index + 1) % directions.length();
            numSeen++;
        }
        return numSeen;
    }

    public long part2(HashMap<String, String[]> tree) {
        return findZZZAsGhost(tree);
    }

    public static void main(String[] args) {
        String filename = "input2.txt";
        if (args.length > 0) {
            filename = args[0];
        }
        day8 day8 = new day8();
        HashMap<String, String[]> tree = day8.buildBinaryTree(filename);
        System.out.println("Part 1: " + day8.part1(tree, day8.root));
        System.out.println("Part 2: " + day8.part2(tree));
    }
}
