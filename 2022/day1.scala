import scala.collection.mutable.ArrayBuffer
import scala.io.Source

val filename = "input/1"


class Elf:
	var foodCalories = List[Int]()
	var totalCalories = 0

	def calculateTotalCalories(): Int =
		totalCalories = foodCalories.sum
		totalCalories


@main def main() =
	val elves = ArrayBuffer[Elf](Elf())
	for (line <- Source.fromFile(filename).getLines)
		if line.isEmpty then
			elves.last.calculateTotalCalories()
			elves.addOne(Elf())
		else
			elves.last.foodCalories = line.toInt :: elves.last.foodCalories
	elves.last.calculateTotalCalories()

	// Part 1 solution: Total calories held by elf with the most total calories
	println(s"${elves.map(elf => elf.totalCalories).max}")
	// Part 2 solution: Total calories held by the top 3 elves
	println(s"${elves.map(elf => elf.totalCalories).sorted.takeRight(3).sum}")
