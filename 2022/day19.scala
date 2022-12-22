import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global
import scala.util.{Failure, Success}

val inputLines = scala.io.Source.fromFile("input/19").getLines.toArray
val sampleLines = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip.split('\n')
val numberPattern = raw"((?:(?<!\d)-)?\d+)".r

extension (i: Int) def ceilDiv(j: Int): Int = (i+j-1) / j

def blueprintQuality(line: String, tMax: Int=24): (Int, Int, Int) =
	val nums = numberPattern.findAllIn(line).map(_.toInt).toArray
	// Kill me
	val bp = nums(0)
	val cost_orebot_ore = nums(1)
	val cost_claybot_ore = nums(2)
	val cost_obsbot_ore = nums(3)
	val cost_obsbot_clay = nums(4)
	val cost_geodebot_ore = nums(5)
	val cost_geodebot_obs = nums(6)

	val max_cost_ore = cost_orebot_ore max cost_claybot_ore max cost_obsbot_ore max cost_geodebot_ore

	val maxPossibleInXMinutes = (0 to 32).toArray
	for i <- 1 to 32 do
		maxPossibleInXMinutes(i) = maxPossibleInXMinutes(i-1) + i

	def simStep(t: Int, numRobots: Array[Int], numRes: Array[Int], totalGeodes: Int=0, maxGeodes: Int=0): Int =
		var mostGeodes = totalGeodes max maxGeodes
		if t >= tMax then return mostGeodes
		if (totalGeodes + maxPossibleInXMinutes(tMax-t)) <= mostGeodes then return mostGeodes

		var (dt, tn) = (0, 0)
		// Try to make a Geode robot
		if numRobots(2) > 0 then
			dt = 1 max (((cost_geodebot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
			dt = dt max (((cost_geodebot_obs - numRes(2)) ceilDiv numRobots(2)) + 1)  // Must always spend at least 1 minute to build
			tn = t + dt
			if tn < tMax then
				val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
				nextRes(0) -= cost_geodebot_ore
				nextRes(2) -= cost_geodebot_obs
				mostGeodes = mostGeodes max simStep(tn, numRobots, nextRes, totalGeodes + (tMax-tn), mostGeodes)
		// Try to make an Obs robot
		if numRobots(1) > 0 && numRobots(2) < cost_geodebot_obs then
			dt = 1 max (((cost_obsbot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
			dt = dt max (((cost_obsbot_clay - numRes(1)) ceilDiv numRobots(1)) + 1)  // Must always spend at least 1 minute to build
			tn = t + dt
			if tn < (tMax-1) then  // any obsidian past that point is worthless
				val nextRobots = numRobots.toArray
				nextRobots(2) += 1
				val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
				nextRes(0) -= cost_obsbot_ore
				nextRes(1) -= cost_obsbot_clay
				mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes, totalGeodes, mostGeodes)
		// Try to make an Ore robot
		if numRobots(0) < max_cost_ore then
			dt = 1 max (((cost_orebot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
			tn = t + dt
			if tn < (tMax-1) then  // any ore past that point is worthless
				val nextRobots = numRobots.toArray
				nextRobots(0) += 1
				val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
				nextRes(0) -= cost_orebot_ore
				mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes, totalGeodes, mostGeodes)
		// Try to make a Clay robot
		if numRobots(1) < cost_obsbot_clay then
			dt = 1 max (((cost_claybot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
			tn = t + dt
			if tn < (tMax-2) then  // any clay past that point is worthless, needs to turn to obs
				val nextRobots = numRobots.toArray
				nextRobots(1) += 1
				val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
				nextRes(0) -= cost_claybot_ore
				mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes, totalGeodes, mostGeodes)
		return totalGeodes max mostGeodes

	val mostGeodes = simStep(0, Vector(1,0,0).toArray, Vector(0,0,0).toArray)
	val quality = mostGeodes * bp
	println(s"Blueprint $bp at $tMax minutes: most geodes $mostGeodes = quality score $quality")
	return (bp, mostGeodes, quality)

@main def main() =
	// val part1 = inputLines.map(blueprintQuality(_)(2)).sum
	// println(s"Part 1: total quality score: $part1")
	// val part2 = inputLines.take(3).map(blueprintQuality(_, 32)(1)).product
	// println(s"Part 2: $part2")
	val p2Futures = Future.sequence(inputLines.take(3).map(line => Future(blueprintQuality(line, 32)(1))))
	val p1Futures = Future.sequence(inputLines.map(line => Future(blueprintQuality(line)(2))))
	p1Futures.onComplete {
		case Success(results) => println(s"Part 1: total quality score: ${results.sum}")
		case Failure(e) => e.printStackTrace
	}
	p2Futures.onComplete {
		case Success(results) => println(s"Part 2: ${results.product}")
		case Failure(e) => e.printStackTrace
	}
	Thread.sleep(1000)
	// val part2 = p2Futures.product
	// println(s"Part 2: $part2")
