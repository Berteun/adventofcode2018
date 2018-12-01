#include <fstream>
#include <iostream>

constexpr char const* INPUT = "input.txt";

int main() {
	std::ifstream input(INPUT);
	int freq_change;
	int sum = 0;
	while (input >> freq_change) {
		sum += freq_change;
	}
	std::cout << sum << "\n";
}
