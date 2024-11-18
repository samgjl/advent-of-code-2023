// COMPILE WITH kotlinc solution.kt -include-runtime -d solution.jar
import java.io.File

class Hand(val cards: String) {
    val cardsList = cards.map { it }

    fun compare(): Int{
        return -1
    }

    fun getType(): String{
        val counts = cardsList.groupingBy { it }.eachCount()
        val countFreq = counts.values.groupingBy { it }.eachCount()

        return when {
            5 in counts.values -> "Five of a kind"
            4 in counts.values -> "Four of a kind"
            3 in counts.values && 2 in counts.values -> "Full house"
            3 in counts.values -> "Three of a kind"
            countFreq[2] == 2 -> "Two pair"
            2 in counts.values -> "One pair"
            else -> "High card"
        }
    }

}

fun main() {
    val rounds = parseFile("sample.txt")
    print(rounds[1].first.getType()) // testing
}

fun parseFile(filename: String): List<Pair<Hand,Int>>{
    val lines = File(filename).readLines()
    val rounds = mutableListOf<Pair<Hand,Int>>() //list of (hand, bid)
    
    for (line in lines) {
        val hand = line.split(" ")[0]
        val bid = line.split(" ")[1].toInt()

        val handObj = Hand(hand)
        rounds.add(Pair(handObj, bid))
    }
    return rounds
}
