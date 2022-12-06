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
		four = find_first_unique_run(&s, 4, 0);
		fourteen = find_first_unique_run(&s, 14, four);
	}
	println!("Part 1: {}", four);
	println!("Part 2: {}", fourteen);
	println!("Completed {} iterations", iterations);
}

fn main() {
	let input: Vec<u8> = fs::read("input/6").expect("Input not found!");
	// run_once(&input);
	run_many(&input, 1_000_000);
}
