#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

void print_v(std::vector<int> const& recipes, int elf1, int elf2) {
	for (auto i = 0u; i < recipes.size(); ++i) {
		if (i == elf1) 
			std::cout << "(";
		else if (i == elf2)
			std::cout << "[";
		else
			std::cout << " ";
		std::cout << recipes[i];
		if (i == elf1) 
			std::cout << ")";
		else if (i == elf2)
			std::cout << "]";
		else
			std::cout << " ";
	}
	std::cout << "\n";
}


std::vector<int> make_pattern(int pattern) {
	std::vector<int> result;
	while (pattern > 0) {
		result.push_back(pattern % 10);
		pattern /= 10;	
	}
	std::reverse(result.begin(), result.end());
	return result;
}

int run(const int stop_pattern) {
	std::vector<int> recipes = {{3, 7}};
	int elf1 = 0, elf2 = 1;
	
	auto pattern = make_pattern(stop_pattern);
	while (true) {
		//print_v(recipes, elf1, elf2);
		int sum = recipes[elf1] + recipes[elf2];
		if (sum > 9) {
			recipes.push_back(sum / 10);
			if (recipes.size() >= pattern.size() && std::equal(pattern.begin(), pattern.end(), recipes.end() - pattern.size(), recipes.end()))
				break;
		} 
		recipes.push_back(sum % 10);
		if (recipes.size() >= pattern.size() && std::equal(pattern.begin(), pattern.end(), recipes.end() - pattern.size(), recipes.end()))
			break;
		elf1 = (elf1 + recipes[elf1] + 1) % recipes.size();
		elf2 = (elf2 + recipes[elf2] + 1) % recipes.size();
	}

	return recipes.size() - pattern.size();
}

int main()  {
	assert(run(51589) == 9);
	assert(run(92510) == 18);
	assert(run(59414) == 2018);
	std::cout << run(440231) << "\n";
}
