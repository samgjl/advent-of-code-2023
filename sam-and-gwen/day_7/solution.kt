import java.io.File
class Hand(val cards: String) {
    val cards = ""

}

class Solution {
    fun main() {
        parseFile("sample.txt");
    }
    fun parseFile(filename: String): List<Pair<Hand,Int>>{
        val lines = File(filename).readLines()
        val rounds = MutableListOf<Pair<Hand,Int>>()
        
        for (line in lines) {
            val hand = line.split(" ")[0]
            val bid = line.split(" ")[1].toInt()

            val handObj = Hand(hand)
            round.add(Pair(handObj, bid));
        }

    }
}