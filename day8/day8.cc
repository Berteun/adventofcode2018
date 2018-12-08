#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

constexpr char const* INPUT = "input.txt";

struct Tree {
	const std::vector<Tree> children_;
	const std::vector<int> metadata_;

	Tree(std::vector<Tree> children, std::vector<int> metadata) 
	: children_(std::move(children)) , metadata_(std::move(metadata))
	{}

	int eval_metadata() const {
		return std::accumulate(
			children_.begin(), children_.end(),
			std::accumulate(metadata_.begin(), metadata_.end(), 0),
			[](auto s, auto& c) { return s + c.eval_metadata(); });
	}

	int eval_tree() const {
		if (children_.size() == 0)
			return eval_metadata();
		return std::accumulate(metadata_.begin(), metadata_.end(), 0, 
			[&](auto s, auto i) { 
				return s + (i > 0 && i <= children_.size() 
					 ? children_[i - 1].eval_tree() 
					 : 0
				); 
			});
	}
};

Tree parse_tree(std::vector<int> const& numbers, int& idx) {
	auto n_child = numbers[idx++];
	auto n_metad = numbers[idx++];

	std::vector<Tree> children;
	for (auto i = 0; i < n_child; ++i)
		children.emplace_back(parse_tree(numbers, idx));

	idx += n_metad;
	return Tree(std::move(children), std::vector<int>(&numbers[idx - n_metad], &numbers[idx]));
}

std::vector<int> read_input() {
	std::ifstream input(INPUT);
	std::vector<int> numbers;
	int number;
	while(input >> number)
		numbers.push_back(number);
	return numbers;
}

int main() {
	auto numbers = read_input();
	int idx = 0;
	auto tree = parse_tree(numbers, idx);
	std::cout << tree.eval_metadata() << "\n";
	std::cout << tree.eval_tree() << "\n";
}
