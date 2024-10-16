import java.io.File
class Hand(val cards: String) {
    val cardsList = cards.split('')

    fun compare(): Int{
        
    }

    fun getType(): String{
        
    }

}

class Solution {
    fun main() {
        val rounds = parseFile("sample.txt");

    }
    fun parseFile(filename: String): List<Pair<Hand,Int>>{
        val lines = File(filename).readLines()
        val rounds = MutableListOf<Pair<Hand,Int>>()
        
        for (line in lines) {
            val hand = line.split(" ")[0]
            val bid = line.split(" ")[1].toInt()

            val handObj = Hand(hand)
            rounds.add(Pair(handObj, bid))
        }
        return rounds
    }
}