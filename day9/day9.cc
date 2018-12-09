#include <list>
#include <fstream>
#include <iostream>
#include <map>
#include <tuple>

constexpr char const* INPUT = "input.txt";

std::tuple<int, int> read_input() {
	int players, rounds;
	std::string _s;
	std::ifstream input(INPUT);
	input >> players >> _s >> _s >> _s >> _s >> _s >> rounds;
	return std::make_tuple(players, rounds);
}


void print_progress(int cur_round, int players, std::list<int>::const_iterator current, std::list<int> const& marbles) {
	std::cout << "[" << cur_round << "/" << (cur_round % players) << "] " 
		<< std::distance(marbles.begin(), current) << " (" << *current << ") [" ;
	std::string sep = "";
	for (auto m : marbles) {
		std::cout << sep << m;
		sep = ", ";
	}
	std::cout << "]\n";
}

long play_game(int players, int rounds) {
	std::map<int,long> scores;
	std::list<int> marbles = {0};
	auto current = marbles.begin();

	for (int cur_round = 1; cur_round <= rounds; ++cur_round) {
		if (cur_round % 23 == 0) {
			for (auto i = 0; i < 7; i++) {
				if (current == marbles.begin())
					current = marbles.end();
				--current;
			}
			scores[cur_round % players] += cur_round + *current;
			current = marbles.erase(current);
			if (current == marbles.end())
				current = marbles.begin();
		} else {
			for (auto i = 0; i < 2; i++) {
				++current;
				if (current == marbles.end())
					current = marbles.begin();
			}
			current = marbles.insert(current, cur_round);
		}

		//print_progress(cur_round, players, current, marbles);
	}
	long max_s = 0;
	for (auto [p,s] : scores)
		max_s = std::max(max_s, s);
	return max_s;
}

int main() {
	int players, rounds;
	std::tie(players, rounds) = read_input();
	std::cout << play_game(players, rounds) << "\n";
	std::cout << play_game(players, rounds*100) << "\n";
}

