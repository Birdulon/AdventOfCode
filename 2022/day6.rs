#![allow(dead_code)]
use std::fs;

type Int = usize;

fn substring_unique_copyless(s: &Vec<u8>, right: Int, length: Int) -> bool {
	for i in (right-length)..right {
		let c = s[i];
		for j in (i+1)..right {
			if s[j] == c {
				return false;
			}
		}
	}
	return true;
}

fn find_first_unique_run(s: &Vec<u8>, num: Int, skip: Int) -> Int {
	for right in num.max(skip)..s.len() {
		if substring_unique_copyless(s, right, num) {
			return right;
		}
	}
	return 0;
}

fn mask_to_string(mask: u32) -> String {
	let mut v: Vec<u8> = Vec::with_capacity(mask.count_ones() as usize);
	for i in 0..26 {
		if mask & (1<<i) != 0 {
			v.push(b'a'+i);
		}
	}
	return String::from_utf8(v).unwrap();
}

fn find_first_unique_runs(s: &Vec<u8>) -> (Int, Int) {
	const BATCH_SIZE: Int = 8;
	const BATCH_NUM: Int = 4096/BATCH_SIZE;
	let mut four: Int = 0;
	let mut fourteen: Int = 0;
	let mut masks: [u32; 4096] = [0; 4096];
	let mut scratch_masks: [u32; BATCH_SIZE] = [0; BATCH_SIZE];
	let mut scratch_masks_bits: [u8; BATCH_SIZE] = [0; BATCH_SIZE];
	for i in 0..4096 {
		masks[i] = 1 << (s[i]-b'a');
	}
	// Turn masks into masks2. Indices are now +1.
	for i in 0..(4096-1) {
		masks[i] |= masks[i+1];
	}
	'four_loop: for batch in 1..(BATCH_NUM) {
		for i in 0..BATCH_SIZE {
			let idx = batch*BATCH_SIZE + i;
			scratch_masks[i] = masks[idx] | masks[idx-2];
			scratch_masks_bits[i] = scratch_masks[i].count_ones() as u8;
		}
		for i in 0..BATCH_SIZE {
			if scratch_masks_bits[i] == 4 {
				four = batch*BATCH_SIZE + i;
				break 'four_loop;
			}
		}
	}
	// Turn masks2 into masks4. Indices are now +3.
	for i in four..(4096-3) {
		masks[i] |= masks[i+2];
	}
	// Turn masks4 into masks8. Indices are now +7.
	for i in four..(4096-7) {
		masks[i] |= masks[i+4];
	}
	'fourteen_loop: for batch in (four/BATCH_SIZE)..(BATCH_NUM) {
		for i in 0..BATCH_SIZE {
			let idx = batch*BATCH_SIZE + i;
			// scratch_masks[i] = masks[idx] | masks[idx-4] | masks[idx-8] | masks[idx-10];
			scratch_masks[i] = masks[idx] | masks[idx-6];
			scratch_masks_bits[i] = scratch_masks[i].count_ones() as u8;
		}
		for i in 0..BATCH_SIZE {
			if scratch_masks_bits[i] == 14 {
				fourteen = batch*BATCH_SIZE + i;
				break 'fourteen_loop;
			}
		}
	}
	return (four+2, fourteen+8);
}

fn run_once(s: &Vec<u8>) {
	let four = find_first_unique_run(&s, 4, 0);
	let fourteen = find_first_unique_run(&s, 14, four);
	println!("Part 1: {}", four);
	println!("Part 2: {}", fourteen);
}

fn run_many(s: &Vec<u8>, iterations: usize) {
	let mut four = 0;
	let mut fourteen = 0;
	for _ in 0..iterations {
		// four = find_first_unique_run(&s, 4, 0);
		// fourteen = find_first_unique_run(&s, 14, four);
		(four, fourteen) = find_first_unique_runs(&s);
	}
	println!("Part 1: {}", four);
	println!("Part 2: {}", fourteen);
	println!("Completed {} iterations", iterations);
}

fn main() {
	let input: Vec<u8> = fs::read("input/6").expect("Input not found!");
	println!("Input is {} long", input.len());
	// run_once(&input);
	run_many(&input, 1_000_000);
	// let (four, fourteen) = find_first_unique_runs(&input);
	// println!("Part 1: {}", four);
	// println!("Part 2: {}", fourteen);
}
