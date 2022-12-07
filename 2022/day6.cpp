#include <bit>
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


std::pair<size_t, size_t> find_first_unique_runs(std::vector<uint8_t> *s) {
	const size_t BATCH_SIZE = 8;
	const size_t BATCH_NUM = 4096/BATCH_SIZE;
	size_t four = 0;
	size_t fourteen = 0;
	uint32_t masks[4096];
	uint32_t scratch_masks[BATCH_SIZE];
	uint8_t scratch_masks_bits[BATCH_SIZE];
	for (int i=0; i<4096; i++) {
		masks[i] = 1 << ((*s)[i]-'a');
	}
	// Turn masks into masks2. Indices are now +1.
	for (int i=0; i<4095; i++) {
		masks[i] |= masks[i+1];
	}
	for (int batch=1; batch<BATCH_NUM; batch++) {
		for (int i=0; i<BATCH_SIZE; i++) {
			int idx = batch*BATCH_SIZE + i;
			scratch_masks[i] = masks[idx] | masks[idx-2];
			scratch_masks_bits[i] = std::popcount(scratch_masks[i]);
		}
		for (int i=0; i<BATCH_SIZE; i++) {
			if (scratch_masks_bits[i] == 4) {
				four = batch*BATCH_SIZE + i;
				goto four_found;
			}
		}
	}
four_found:
	// Turn masks2 into masks4. Indices are now +3.
	for (int i=four; i<4093; i++) {
		masks[i] |= masks[i+2];
	}
	// Turn masks4 into masks8. Indices are now +7.
	for (int i=fourteen; i<4089; i++) {
		masks[i] |= masks[i+4];
	}
	for (int batch=(four/BATCH_SIZE); batch<BATCH_NUM; batch++) {
		for (int i=0; i<BATCH_SIZE; i++) {
			int idx = batch*BATCH_SIZE + i;
			scratch_masks[i] = masks[idx] | masks[idx-6];
			scratch_masks_bits[i] = std::popcount(scratch_masks[i]);
		}
		for (int i=0; i<BATCH_SIZE; i++) {
			if (scratch_masks_bits[i] == 14) {
				fourteen = batch*BATCH_SIZE + i;
				goto fourteen_found;
			}
		}
	}
fourteen_found:
	return std::pair<size_t, size_t>(four+2, fourteen+8);
}

void run_once(std::vector<uint8_t> *s) {
	size_t four = find_first_unique_run(s, 4, 4);
	size_t fourteen = find_first_unique_run(s, 14, four);
	std::cout << "Part 1: " << four << '\n';
	std::cout << "Part 2: " << fourteen << '\n';
}

void run_many(std::vector<uint8_t> *s, size_t iterations) {
	size_t volatile four = 0;  // Don't you dare optimize out the iterations!
	size_t volatile fourteen = 0;
	std::cout << "Running " << iterations << " iterations:\n";
	for (size_t i = 0; i<iterations; i++) {
		// four = find_first_unique_run(s, 4, 4);
		// fourteen = find_first_unique_run(s, 14, four);
		std::pair<size_t, size_t> result = find_first_unique_runs(s);
		four = result.first;
		fourteen = result.second;
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
	run_many(&input, 10000000);
}
