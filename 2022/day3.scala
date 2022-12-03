import scala.io.Source

extension (s: String) def splitHalf: (String, String) = (s.substring(0, s.length()/2), s.substring(s.length()/2))

def priorityScore(c: Char): Int = c match
	case c if 'a' to 'z' contains c => (c - 'a' + 1)
	case c if 'A' to 'Z' contains c => (c - 'A' + 27)
	case _ => 0


@main def main() =
	val inputLines = Source.fromFile("input/3").getLines.toArray  // Can't leave it lazy as Part 1 will consume it

	// Part 1 - find items common between first half and second half of each line
	println(inputLines.map(line =>
		val (knapsack1, knapsack2) = line.splitHalf
		priorityScore((knapsack1.toSet & knapsack2.toSet).head)
	).sum)

	// Part 2 - find items common between lines in groups of 3 lines
	println(inputLines.grouped(3).map(group =>
		priorityScore(group.map(_.toSet).reduce(_&_).head)
	).sum)
