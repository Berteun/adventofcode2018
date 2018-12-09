#include <fstream>
#include <iostream>
#include <vector>

constexpr char const* INPUT = "input.txt";

std::vector<char> react(std::string const& polymer) {
	std::vector<char> reacted;
	for (auto b = polymer.begin(); b < polymer.end(); ++b)
		if (reacted.size() == 0 || (reacted.back() ^ *b) != 32)
			reacted.push_back(*b);
		else 
			reacted.pop_back();
	return reacted;
}

int main() {
	std::ifstream input(INPUT);
	std::string polymer;

	input >> polymer;
	auto reacted = react(polymer);
	std::cout << reacted.size() << std::endl;

	auto minsize = reacted.size();
	for (char ch = 'a'; ch <= 'z'; ++ch) {
		std::string polymer;
		std::copy_if(reacted.begin(), reacted.end(), std::back_inserter(polymer),
			[ch](auto p) { return (p | 32) != ch; });

		minsize = std::min(minsize, react(polymer).size());
	}
	std::cout << minsize << std::endl;
}
