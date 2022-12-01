import scala.collection.mutable.ArrayBuffer
import scala.io.Source

@main def main() =
	val elfRations = Source.fromFile("day1-input").mkString.split("\n\n").map(_.split("\n").map(_.toInt))
	val sortedElfCalories = elfRations.map(_.sum).sorted

	// Part 1 solution: Total calories held by elf with the most total calories
	println(s"${sortedElfCalories.last}")
	// Part 2 solution: Total calories held by the top 3 elves
	println(s"${sortedElfCalories.takeRight(3).sum}")
