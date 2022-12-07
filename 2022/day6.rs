#![allow(dead_code)]
use std::env;
use std::fs;
use std::time::Instant;

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

fn main() {
	let mut filename = "input/6";
	let mut iterations = 1_000_000;
	let args: Vec<String> = env::args().collect();
	match args.len() {
		3 => {filename = &args[1]; iterations = args[2].parse().expect(&("Invalid number for iterations: ".to_owned() + &args[2]))},
		2 => filename = &args[1],
		_ => (),
	};
	let s: Vec<u8> = fs::read(filename).expect("Input not found!");

	println!("Running {} iterations:", iterations);
	let t0 = Instant::now();
	let mut four = 0;
	let mut fourteen = 0;
	for _ in 0..iterations {
		// four = find_first_unique_run(&s, 4, 0);
		// fourteen = find_first_unique_run(&s, 14, four);
		(four, fourteen) = find_first_unique_runs(&s);
	}
	let duration = t0.elapsed();
	let per_iteration = duration / iterations;
	println!("Part 1: {}", four);
	println!("Part 2: {}", fourteen);
	println!("Completed {} iterations in {:.3}s (~{}ns each)", iterations, duration.as_secs_f32(), per_iteration.as_nanos());
}
