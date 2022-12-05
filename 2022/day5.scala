import java.nio.file.Files
import java.nio.file.Paths
import scala.collection.mutable.ArrayDeque

type Stack[A] = ArrayDeque[A]
val Stack = ArrayDeque

val numberPattern = raw"((?:(?<!\d)-)?\d+)".r

extension (s: String) def partition(sep: String = "\n\n"): (String, String) =
	val ss = s.split(sep, 2)
	(ss(0), ss(1))

extension (s: String) def partition2(sep: String = "\n\n", sep2 : String = "\n"): (Array[String], Array[String]) =
	val ss = s.split(sep, 2)
	(ss(0).split(sep2), ss(1).split(sep2))

extension (aos: Seq[String]) def transpose(reverseX: Boolean = false, reverseY: Boolean = false): Seq[String] =
	val mapping: Function[Int, String] = if reverseY
		then (i => aos.reverse.map(_.substring(i,i+1)).reduceLeft(_+_))
		else (i => aos.map(_.substring(i,i+1)).reduceLeft(_+_))
	if reverseX
		then (0 until aos(0).length).reverse.map(mapping)
		else (0 until aos(0).length).map(mapping)

def getStacksString(stacks: Map[Int, Stack[Char]]): String = stacks.keys.toBuffer.sorted.map(stacks(_).last.toString).reduceLeft(_+_)

@main def main() =
	val (input_stacks, input_orders) = Files.readString(Paths.get("input/5")).partition2()
	val stacks_s = input_stacks
		.transpose(reverseY = true)
		.map(_.replaceAll(raw"[\[\]]", " ").strip)
		.filter(_.length > 0)
		.map(s => (s.substring(0,1).toInt, s.substring(1))).toMap
	val orders = input_orders.map(numberPattern.findAllIn(_).map(_.toInt).toArray).toArray  // Can't leave lazy or Part 1 will consume it all

	var stacks: Map[Int, Stack[Char]] = stacks_s.map((k,v) => (k, v.toCharArray.to(Stack))).toMap
	for order <- orders do
		val (amount, source, dest) = (order(0), stacks(order(1)), stacks(order(2)))
		for _ <- 1 to amount do
			dest.append(source.removeLast())
	println(s"Part 1: ${getStacksString(stacks)}")

	stacks = stacks_s.map((k,v) => (k, v.toCharArray.to(Stack))).toMap
	for order <- orders do
		val (amount, source, dest) = (order(0), stacks(order(1)), stacks(order(2)))
		dest.appendAll(source.takeRight(amount))
		source.dropRightInPlace(amount)
	println(s"Part 2: ${getStacksString(stacks)}")
