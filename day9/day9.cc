#include <deque>
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


void print_progress(int cur_round, int players, std::deque<int> const& marbles) {
	std::cout << "[" << cur_round << "/" << (cur_round % players) << "] [" ;
	for (auto m : marbles) {
		std::cout << m << ", ";
	}
	std::cout << "]\n";
}

void rotate_left(std::deque<int>& marbles, int n) {
	while (n--) {
		marbles.push_back(marbles.front());
		marbles.pop_front();
	}
}

void rotate_right(std::deque<int>& marbles, int n) {
	while (n--) {
		marbles.push_front(marbles.back());
		marbles.pop_back();
	}
}

long play_game(int players, int rounds) {
	std::map<int,long> scores;
	std::deque<int> marbles = {0};

	for (int cur_round = 1; cur_round <= rounds; ++cur_round) {
		if (cur_round % 23) {
			rotate_left(marbles, 2);
			marbles.push_front(cur_round);
		} else {
			rotate_right(marbles, 7);
			scores[cur_round % players] += cur_round + marbles.front();
			marbles.pop_front();
		}

		//print_progress(cur_round, players, marbles);
	}

	return std::max_element(scores.begin(), scores.end(),
		[](auto p, auto q) { return p.second < q.second; })->second;
}

int main() {
	int players, rounds;
	std::tie(players, rounds) = read_input();
	std::cout << play_game(players, rounds) << "\n";
	std::cout << play_game(players, rounds*100) << "\n";
}
