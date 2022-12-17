val fileSizePattern = raw"(\d+) ([\w.]+)".r
val cdPattern = "\\$ cd ([\\/\\w.]+)".r  // raw string interpolation doesn't like \$
val rootPattern = raw"\/(.*)".r

def cd(cwd: String, to: String): String = to match
	case rootPattern(absPath) => absPath  // Absolute path
	case ".." => 
		val i = cwd.lastIndexOf('/')
		if i < 0 then cwd else cwd.substring(0, i)  // Up one subfolder
	case _ => s"$cwd/$to"

@main def main() =
	val inputLines = scala.io.Source.fromFile("input/07").getLines

	var cwd = ""  // We append the / at time of use
	val folders = scala.collection.mutable.HashSet[String](cwd)
	val fileSizes = scala.collection.mutable.HashMap[String, Int]()
	for line <- inputLines do
		line match
			case cdPattern(dir) =>
				cwd = cd(cwd, dir)
				folders += cwd
			case fileSizePattern(sizeStr, filename) =>
				fileSizes += (s"$cwd/$filename" -> sizeStr.toInt)
			case _ => {}  // "$ ls", "dir ..."
	// Very inefficient way of calculating folder sizes, but cute enough
	val folderSizes = folders.map(f => (f, fileSizes.filter((k,v) => k startsWith s"$f/").values.sum)).toMap

	println(s"Part 1: ${folderSizes.values.filter(v => v <= 100_000).sum}")

	val totalCapacity = 70_000_000
	val desiredRemaining = 30_000_000
	val currentRemaining = totalCapacity - folderSizes("")
	val sizeToDelete = desiredRemaining - currentRemaining
	println(s"Part 2: ${folderSizes.values.filter(v => v > sizeToDelete).min}")
