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


long run(const int stop_number) {
	std::vector<int> recipes = {{3, 7}};
	int elf1 = 0, elf2 = 1;
	
	while (recipes.size() < stop_number + 10) {
		//print_v(recipes, elf1, elf2);
		int sum = recipes[elf1] + recipes[elf2];
		if (sum > 9)
			recipes.push_back(sum / 10);
		recipes.push_back(sum % 10);
		elf1 = (elf1 + recipes[elf1] + 1) % recipes.size();
		elf2 = (elf2 + recipes[elf2] + 1) % recipes.size();
	}

	long n = 0;
	for (int i = 0; i < 10; ++i) {
		n *= 10;
		n += recipes[stop_number + i];
	}
	return n;
}

int main()  {
	assert(run(18) == 9251071085);
	std::cout << run(440231) << "\n";
}
