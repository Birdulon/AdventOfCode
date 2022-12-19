val inputLines = scala.io.Source.fromFile("input/19").getLines.toArray
val sampleLines = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip.split('\n')
val numberPattern = raw"((?:(?<!\d)-)?\d+)".r

extension (i: Int) def ceilDiv(j: Int): Int = (i+j-1) / j

def blueprintQuality(line: String, tMax: Int=24): Int =
	val nums = numberPattern.findAllIn(line).map(_.toInt).toArray
	// println(nums.mkString(", "))
	// Kill me
	val bp = nums(0)
	val cost_orebot_ore = nums(1)
	val cost_claybot_ore = nums(2)
	val cost_obsbot_ore = nums(3)
	val cost_obsbot_clay = nums(4)
	val cost_geodebot_ore = nums(5)
	val cost_geodebot_obs = nums(6)

	def simStep(t: Int, numRobots: Array[Int], numRes: Array[Int]): Int =
		if t >= tMax then return numRes(3)
		var mostGeodes = 0
		var (dt, tn) = (0, 0)
		// // Try to make an Ore robot
		// dt = 1 max (((cost_orebot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
		// tn = t + dt
		// if tn <= tMax then
		// 	val nextRobots = Vector(numRobots(0)+1, numRobots(1), numRobots(2), numRobots(3))
		// 	val nextRes = Vector(numRes(0)+numRobots(0)*dt-cost_orebot_ore, numRes(1)+numRobots(1)*dt, numRes(2)+numRobots(2)*dt, numRes(3)+numRobots(3)*dt)
		// 	mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes)
		// Try to make an Ore robot
		dt = 1 max (((cost_orebot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
		tn = t + dt
		if tn <= tMax then
			val nextRobots = numRobots.toArray
			nextRobots(0) += 1
			val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
			nextRes(0) -= cost_orebot_ore
			mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes)
		// Try to make a Clay robot
		dt = 1 max (((cost_claybot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
		tn = t + dt
		if tn <= tMax then
			val nextRobots = numRobots.toArray
			nextRobots(1) += 1
			val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
			nextRes(0) -= cost_claybot_ore
			mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes)
		// Try to make an Obs robot
		if numRobots(1) > 0 then
			dt = 1 max (((cost_obsbot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
			dt = dt max (((cost_obsbot_clay - numRes(1)) ceilDiv numRobots(1)) + 1)  // Must always spend at least 1 minute to build
			tn = t + dt
			if tn <= tMax then
				val nextRobots = numRobots.toArray
				nextRobots(2) += 1
				val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
				nextRes(0) -= cost_obsbot_ore
				nextRes(1) -= cost_obsbot_clay
				mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes)
		// Try to make a Geode robot
		if numRobots(2) > 0 then
			dt = 1 max (((cost_geodebot_ore - numRes(0)) ceilDiv numRobots(0)) + 1)  // Must always spend at least 1 minute to build
			dt = dt max (((cost_geodebot_obs - numRes(2)) ceilDiv numRobots(2)) + 1)  // Must always spend at least 1 minute to build
			tn = t + dt
			if tn <= tMax then
				val nextRobots = numRobots.toArray
				nextRobots(3) += 1
				val nextRes = (numRes zip numRobots).map((b,f) => b + f*dt).toArray
				nextRes(0) -= cost_geodebot_ore
				nextRes(2) -= cost_geodebot_obs
				mostGeodes = mostGeodes max simStep(tn, nextRobots, nextRes)
		// Make nothing
		if mostGeodes == 0 then
			dt = tMax - t
			mostGeodes = numRes(3) + dt*numRobots(3)
		return mostGeodes

	val mostGeodes = simStep(0, Vector(1,0,0,0).toArray, Vector(0,0,0,0).toArray)
	val quality = mostGeodes * bp
	println(s"Blueprint $bp: most geodes $mostGeodes = quality score $quality")
	return quality

@main def main() =
	val part1 = inputLines.par.map(blueprintQuality(_)).sum
	println(s"Part 1: total quality score: $part1")
	val part2 = inputLines.take(3).par.map(blueprintQuality(_, 32)).sum
	println(s"Part 2: total quality score for 32min 3 blueprints: $part2")  // lmao you'll have to convert to the actual part2 answer yourself
	// blueprintQuality(sampleLines(1))
