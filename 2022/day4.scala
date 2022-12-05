import scala.io.Source

val numberPattern = raw"((?:(?<!\d)-)?\d+)".r

@main def main() =
	val rangePairs: Array[(Range, Range)] = Source.fromFile("input/4").getLines
		.map(line => numberPattern.findAllIn(line).map(_.toInt).toArray)
		.map(n => ((n(0) to n(1)), (n(2) to n(3))))
		.toArray  // Can't leave it lazy as Part 1 will consume it

	val subsets = rangePairs.map((a,b) => if (a.containsSlice(b) | b.containsSlice(a)) 1 else 0).sum
	println(s"Part 1: $subsets elves have no unique work in their pairing")

	val overlaps = rangePairs.map((a,b) => if (a.intersect(b).isEmpty) 0 else 1).sum
	println(s"Part 2: $overlaps elf pairs have overlapping work in their pairing")
