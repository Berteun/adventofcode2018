#include <fstream>
#include <iostream>
#include <vector>
#include <unordered_set>

constexpr char const* INPUT = "input.txt";

std::vector<int> inputs;

int main() {
	std::ifstream input(INPUT);
	int freq_change;
	while (input >> freq_change)
		inputs.push_back(freq_change);
	
	int index = 0;
	int cur_frequency = 0;
	std::unordered_set<int> seen;
	while (true) {
		cur_frequency += inputs[index++];			
		if (auto [_, inserted] = seen.insert(cur_frequency); !inserted) {
			std::cout << cur_frequency << "\n";
			break;
		}
		index %= inputs.size();
	}
}
