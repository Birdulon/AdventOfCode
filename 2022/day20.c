#include <stdio.h>
// #define INPUT_LENGTH 5000
#define INPUT_LENGTH 7
#define DEC_KEY 811589153

struct list_node {
	struct list_node* prev;
	struct list_node* next;
	long value;
};

void mix_right(struct list_node* node, long amount) {
	struct list_node* new_prev = node->next;
	// Pop from position
	node->prev->next = node->next;
	node->next->prev = node->prev;
	// Advance from original next to the new prev
	for (int i = 1; i < amount; i++) {
		new_prev = new_prev->next;
	}
	// Set node to have correct new links
	node->prev = new_prev;
	node->next = new_prev->next;
	// Insert after new prev
	new_prev->next = node;  // same as node->prev->next = node;
	node->next->prev = node;
}

void mix_left(struct list_node* node, long amount) {
	struct list_node* new_next = node->prev;
	// Pop from position
	node->prev->next = node->next;
	node->next->prev = node->prev;
	// Advance from original prev to the new next
	for (int i = 1; i < amount; i++) {
		new_next = new_next->prev;
	}
	// Set node to have correct new links
	node->next = new_next;
	node->prev = new_next->prev;
	// Insert after new prev
	new_next->prev = node;  // same as node->next->prev = node;
	node->prev->next = node;
}

void mix(struct list_node* node) {
	int forward_amount = node->value;
	int reverse_amount;
	const int mod = INPUT_LENGTH-1;
	if (forward_amount == 0) return;  // Do nothing for 0
	if (forward_amount > 0) {
		forward_amount = forward_amount % mod;
		reverse_amount = mod - forward_amount;
	} else {
		reverse_amount = -forward_amount % mod;
		forward_amount = mod - reverse_amount;
	}
	if (forward_amount < reverse_amount) {
		mix_right(node, forward_amount);
	} else {
		mix_left(node, reverse_amount);
	}
}

int main(int argc, char *argv[]) {
	struct list_node code[INPUT_LENGTH];
	struct list_node* zero;  // Keep track of this node for later
	long coord_x, coord_y, coord_z;
	// Initialize circular doubly-linked list links
	code[0].prev = &code[INPUT_LENGTH-1];
	code[0].next = &code[1];
	for (int i = 1; i < INPUT_LENGTH-1; i++) {
		code[i].prev = &code[i-1];
		code[i].next = &code[i+1];
	}
	code[INPUT_LENGTH-1].prev = &code[INPUT_LENGTH-2];
	code[INPUT_LENGTH-1].next = &code[0];

	// Init sample
	code[0].value = 1;
	code[1].value = 2;
	code[2].value = -3;
	code[3].value = 3;
	code[4].value = -2;
	code[5].value = 0;
	code[6].value = 4;
	zero = &code[5];

	// // Load input
	// FILE *fp = fopen("input/20", "r");
	// for (int i = 0; i < INPUT_LENGTH; i++) {
	// 	fscanf(fp, "%ld", &code[i].value);
	// 	if (code[i].value == 0) {
	// 		zero = &code[i];
	// 	}
	// }
	// fclose(fp);

	// Part 2 execution
	for (int i = 0; i < INPUT_LENGTH; i++) {
		code[i].value = code[i].value * DEC_KEY;
	}
	for (int pass = 0; pass < 10; pass++) {
		for (int i = 0; i < INPUT_LENGTH; i++) {
			mix(&code[i]);
		}
		printf("Resulting chain from mix %d: ", pass);
		for (int i = 0; i < 7; i++) {
			printf("%ld ", zero->value);
			zero = zero->next;
		}
		printf("\n");
	}
	// Get resulting coords
	for (int i = 0; i < 1000; i++) {zero = zero->next;}
	coord_x = zero->value;
	for (int i = 0; i < 1000; i++) {zero = zero->next;}
	coord_y = zero->value;
	for (int i = 0; i < 1000; i++) {zero = zero->next;}
	coord_z = zero->value;
	printf("Part 2: coords (%ld, %ld, %ld) give sum %ld\n", coord_x, coord_y, coord_z, coord_x+coord_y+coord_z);
	return 0;
}
