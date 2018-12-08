#include <fstream>
#include <iostream>
#include <vector>

constexpr char const* INPUT = "input.txt";

int main() {
	std::ifstream input(INPUT);
	std::string polymer;
	input >> polymer;
	std::vector<char> reacted;

	for (auto b = polymer.begin(); b < polymer.end(); ++b)
		if (reacted.size() == 0 || (reacted.back() ^ *b) != 32)
			reacted.push_back(*b);
		else 
			reacted.pop_back();

	std::cout << reacted.size() << std::endl;
	auto minsize = reacted.size();
	for (char ch = 'A'; ch <= 'Z'; ++ch) {
		std::string polymer(reacted.begin(), reacted.end());
		std::vector<char> new_reacted;

		for (auto b = polymer.begin(); b < polymer.end(); ++b) {
			if (*b == ch || (*b == (ch | 32)))
				continue;

			if (new_reacted.size() == 0 || (new_reacted.back() ^ *b) != 32)
				new_reacted.push_back(*b);
			else 
				new_reacted.pop_back();
		}

		std::cout << ch << ": " << new_reacted.size() << "\n";;
		minsize = std::min(minsize, new_reacted.size());
	}

	std::cout << minsize << std::endl;
}
