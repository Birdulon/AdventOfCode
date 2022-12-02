import scala.io.Source
import scala.math.floorMod

enum RPS(val score: Int):
	case Rock     extends RPS(1)
	case Paper    extends RPS(2)
	case Scissors extends RPS(3)

	def <=>(other: RPS) =
		(other.score - score) match
			case -2 | 1 => -1
			case -1 | 2 =>  1
			case _      =>  0

	def >(other: RPS) = <=>(other) > 0
	def <(other: RPS) = <=>(other) < 0
	def ==(other: RPS) = <=>(other) == 0

	def +(amount: Int) = RPS.fromOrdinal(floorMod(this.ordinal + amount, 3))
	def -(amount: Int) = RPS.fromOrdinal(floorMod(this.ordinal - amount, 3))

def resultScore(a: RPS, b: RPS) = a <=> b match
	case -1 => 0
	case 1 => 6
	case _ => 3

val moveMap = Map("A"->RPS.Rock, "B"->RPS.Paper, "C"->RPS.Scissors, "X"->RPS.Rock, "Y"->RPS.Paper, "Z"->RPS.Scissors)

@main def main() =
	val strategyGuide = Source.fromFile("day2-input").getLines.map(_.split(" ")).toArray  // Can't leave it lazy as Part 1 will consume it
	// val strategyGuide = Source.fromString("A Y\nB X\nC Z\n").getLines.map(_.split(" ")).toArray

	// Part 1 - evaluate all moves in the guide using moveMap and tally score
	var score = 0
	for movePair <- strategyGuide do
		val opponentMove = moveMap(movePair(0))
		val ourMove = moveMap(movePair(1))
		score += resultScore(ourMove, opponentMove) + ourMove.score
	println(score)

	// Part 2 - X->lose, Y->draw, Z->win
	score = 0
	for movePair <- strategyGuide do
		val opponentMove = moveMap(movePair(0))
		val ourMove = movePair(1) match
			case "X" => opponentMove - 1
			case "Y" => opponentMove
			case "Z" => opponentMove + 1
		score += resultScore(ourMove, opponentMove) + ourMove.score
	println(score)