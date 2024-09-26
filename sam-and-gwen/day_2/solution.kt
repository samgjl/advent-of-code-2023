import java.io.File
val MAX_RED = 12;
val MAX_GREEN = 13;
val MAX_BLUE = 14;

class Round(r: Int, g: Int, b: Int) {
  val r = r;
  val g = g;
  val b = b;

  fun isPossible(): Boolean {
    if (this.r > MAX_RED || this.g > MAX_GREEN || this.b > MAX_BLUE) {
      return false;
    }
    return true;
  }

  override fun toString(): String {
    return " ${this.r} red, ${this.g} green, ${this.b} blue;"
  }
}

class Game(id: Int, rounds: List<Round>) {
  val id = id;
  val rounds = rounds;

  fun isPossible(): Boolean {
    for (round in rounds) {
      if (!round.isPossible()) {
        return false;
      }
    }
    return true;
  }

  fun max(): List<Int> {
    var r = 0; var g = 0; var b = 0;  
    for (round in rounds) {
      if (round.r > r) r = round.r;
      if (round.g > g) g = round.g;
      if (round.b > b) b = round.b;
    }
    return listOf(r, g, b)  
  }

  fun power(): Int {
    val maxes: List<Int> = this.max();
    return maxes[0] * maxes[1] * maxes[2];
  }

  override fun toString(): String {
    var output = "Game ${this.id} (${if (this.isPossible()) "possible" else "impossible"}):";
    for (round in rounds){
      output += round.toString();
    }
    return output;
  }
  
}

fun main() {
  part1("input.txt");
  part2("input.txt");
}

fun readFile(filename: String): List<Game> {
  // Read file into list of games
  val lines = File(filename).readLines();
  val games: MutableList<Game> = mutableListOf();
  // Create game object for each line
  for (i in lines.indices) {
    var game = lines[i].split(":")[1];
    var str_rounds = game.split(";");
    var rounds: MutableList<Round> = mutableListOf();
    // Create Round object for each round
    for (j in str_rounds.indices) {
      val colors = str_rounds[j].split(",");
      var r = 0; var g = 0; var b = 0;
      //  Parse each color:
      for (c in colors) {
        val match = c.split(" ");
        when (match[2]) {
          "red" -> r = match[1].toInt();
          "green" -> g = match[1].toInt();
          "blue" -> b = match[1].toInt();
          else -> println("Problem with color: ${match[2]}")
        }
      }

      rounds.add(Round(r,g,b));
    }
    
    games.add(Game(i+1, rounds))
  }
  
  return games;
}

fun part1(input: String) {
    println("--- PART 1 ---")
    val games = readFile(input);
    var sum = 0;
    for (game in games){
    //   println(game.toString());
      if (game.isPossible()) {
          sum += game.id;
      }
    }
    println("Sum1: $sum")
    println("--------------")
}

fun part2(input: String) {
    println("--- PART 2 ---")
    val games = readFile(input);
    var sum = 0;
    for (game in games){
        sum += game.power();
    }
    println("Sum2: $sum")
    println("--------------")
}