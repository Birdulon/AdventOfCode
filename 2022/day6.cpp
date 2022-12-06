#include <cinttypes>
#include <fstream>
#include <iostream>
#include <vector>

bool substring_unique_copyless(std::vector<uint8_t> *s, size_t right, size_t length) {
	for (size_t i = (right-length); i<right; i++) {
		uint8_t c = (*s)[i];  //s[i];
		for (size_t j = (i+1); j<right; j++) {
			if ((*s)[j] == c) {
				return false;
			}
		}
	}
	return true;
}

size_t find_first_unique_run(std::vector<uint8_t> *s, size_t num, size_t skip) {
	for (size_t right = skip; right<s->size(); right++) {
		if (substring_unique_copyless(s, right, num)) {
			return right;
		}
	}
	return 0;
}

void run_once(std::vector<uint8_t> *s) {
	size_t four = find_first_unique_run(s, 4, 4);
	size_t fourteen = find_first_unique_run(s, 14, four);
	std::cout << "Part 1: " << four << '\n';
	std::cout << "Part 2: " << fourteen << '\n';
}

void run_many(std::vector<uint8_t> *s, size_t iterations) {
	size_t four = 0;
	size_t fourteen = 0;
	for (size_t i = 0; i<iterations; i++) {
		four = find_first_unique_run(s, 4, 4);
		fourteen = find_first_unique_run(s, 14, four);
	}
	std::cout << "Part 1: " << four << '\n';
	std::cout << "Part 2: " << fourteen << '\n';
	std::cout << "Completed " << iterations << " iterations\n";
}

int main() {
	std::ifstream input_file("input/6", std::ios::binary | std::ios::ate);
	const std::streamoff eof_position = static_cast<std::streamoff>(input_file.tellg());
	std::vector<uint8_t> input = std::vector<uint8_t>(eof_position);
	input_file.seekg(0, std::ios::beg);
	input_file.read(reinterpret_cast<char*>(input.data()), eof_position);

	// run_once(&input);
	run_many(&input, 1000000);
}
