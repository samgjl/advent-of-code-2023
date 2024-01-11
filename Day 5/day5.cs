using System.Collections.Generic; 


public class Day5 {
    // Public variables
    string[] lines;
    public int[] seeds;
    /* Structure:
        {
            "X-to-Y": {
                (start, end): target
            }
            ...
        }
    */
    public Dictionary<string, Dictionary<>> dictionary = new Dictionary();
    // Private variables
    
    // Constructor
    public Day5(string path) {
        lines = System.IO.File.ReadAllLines(path);

    }

}