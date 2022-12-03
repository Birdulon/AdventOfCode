import scala.io.Source
import scala.math.floorMod

extension (i: Int) def %%(modulus: Int) = floorMod(i, modulus)

enum RPS(val score: Int):
	case Rock     extends RPS(1)
	case Paper    extends RPS(2)
	case Scissors extends RPS(3)

	def +(amount: Int) = RPS.fromOrdinal((ordinal + amount) %% 3)
	def -(amount: Int) = RPS.fromOrdinal((ordinal - amount) %% 3)
	def -(other: RPS) = score - other.score

	def vs(other: RPS) = (this - other) %% 3 match
		case 1 => 6
		case 2 => 0
		case _ => 3

val moveMap = Map("A"->RPS.Rock, "B"->RPS.Paper, "C"->RPS.Scissors, "X"->RPS.Rock, "Y"->RPS.Paper, "Z"->RPS.Scissors)

@main def main() =
	val strategyGuide = Source.fromFile("input/2").getLines.map(_.split(" ")).toArray  // Can't leave it lazy as Part 1 will consume it
	// val strategyGuide = Source.fromString("A Y\nB X\nC Z\n").getLines.map(_.split(" ")).toArray

	// Part 1 - evaluate all moves in the guide using moveMap and tally score
	println(strategyGuide.map(movePair=>
		val theirMove = moveMap(movePair(0))
		val ourMove = moveMap(movePair(1))
		ourMove.score + (ourMove vs theirMove)
	).sum)

	// Part 2 - X->lose, Y->draw, Z->win
	println(strategyGuide.map(movePair=>
		val theirMove = moveMap(movePair(0))
		val ourMove = movePair(1) match
			case "X" => theirMove - 1
			case "Y" => theirMove
			case "Z" => theirMove + 1
		ourMove.score + (ourMove vs theirMove)
	).sum)