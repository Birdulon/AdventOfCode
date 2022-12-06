import java.nio.file.Files
import java.nio.file.Paths
import scala.util.control.NonLocalReturns.*

def first_unique_run_for(line: String, num: Int, skip: Int = 0): Int = returning {
	for i <- num.max(skip) until line.length do
		if line.substring(i-num, i).toCharArray.distinct.size == num then
			throwReturn(i)
	throwReturn(-1)
}

def first_unique_run_while(line: String, num: Int, skip: Int = 0): Int =
	var i = num.max(skip)
	while i < line.length do
		if line.substring(i-num, i).toCharArray.distinct.size == num then
			return i
		i += 1
	return -1

@main def main() =
	val line = Files.readString(Paths.get("input/6")).strip
	// do_once(line)
	perf_test(line, 100000)

def do_once(line: String) =
	val four = first_unique_run_for(line, 4)
	val fourteen = first_unique_run_for(line, 14, four)
	println(four)
	println(fourteen)

def perf_test(line: String, n: Int) =
	var four = -1
	var fourteen = -1
	for i <- 1 to n do
		four = first_unique_run_for(line, 4)
		fourteen = first_unique_run_for(line, 14, four)
	println(four)
	println(fourteen)