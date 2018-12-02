#include <array>
#include <fstream>
#include <iostream>
#include <vector>

constexpr char const* INPUT = "input.txt";

int main() {
	std::ifstream input(INPUT);
	std::string box_id;
	std::vector<std::string> box_ids;

	while(input >> box_id)
		box_ids.push_back(box_id);

	unsigned i = 0;
	unsigned j = 0;
	for (i = 0u; i < box_ids.size(); ++i)
		for (j = i + 1; j < box_ids.size(); ++j) {
			auto const& s1 = box_ids[i];
			auto const& s2 = box_ids[j];			
			int diff = 0;
			for (auto k = 0u; k < s1.size() && diff < 2; ++k)
				if (s1[k] != s2[k])
					++diff;
			if (diff == 1)
				goto done;
		}
done:
	for (auto k = 0u; k < box_ids[i].size(); ++k)
		if (box_ids[i][k] == box_ids[j][k])
			std::cout << box_ids[i][k];
	std::cout << "\n";
}
