#include <array>
#include <fstream>
#include <iostream>

constexpr char const* INPUT = "input.txt";

int main() {
	std::ifstream input(INPUT);
	std::string box_id;
	int two_count = 0;
	int three_count = 0;
	while(input >> box_id) {
		std::array<int, 26> counts = {0};
		for (auto c : box_id)
			++counts[c - 'a'];
		bool has_two = false;
		bool has_three = false;
		for (auto n : counts) {
			if (n == 2)
				has_two = true;
			if (n == 3)
				has_three = true;
		}

		two_count += has_two;
		three_count += has_three;
	}
	std::cout << two_count * three_count << "\n";
}
