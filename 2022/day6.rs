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
	let mut four = 0;
	let mut fourteen = 0;
	let mut masks: [u32; 4096] = [0; 4096];
	for i in 0..4096 {
		masks[i] = 1 << (s[i]-b'a');
	}
	let mut masks2: [u32; 4096] = masks.clone();
	for i in 1..4096 {
		masks2[i] |= masks[i-1];
	}
	for i in 4..4096 {
		// let mut mask = masks[i];
		// for j in 1..4 {mask |= masks[i-j];}
		let mut mask = masks2[i];
		for j in 1..2 {mask |= masks2[i-j*2];}
		if mask.count_ones() == 4 {
			four = i;
			break;
		}
	}
	for i in (four+9)..4096 {
		// let mut mask = masks[i];
		// for j in 1..14 {mask |= masks[i-j];}
		let mut mask = masks2[i];
		for j in 1..7 {mask |= masks2[i-j*2];}  // (2..14).step_by(2) doesn't unroll, LLVM is garbage
		if mask.count_ones() == 14 {
			fourteen = i;
			break;
		}
	}
	return (four+1, fourteen+1);
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
