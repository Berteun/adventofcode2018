#include <array>
#include <cmath>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <tuple>
#include <vector>


const long depth = 4848;
const long targetX = 15;
const long targetY = 700;
const long bounds = 40;

/*
const long depth = 510;
const long targetX = 10;
const long targetY = 10;
*/

std::array<std::array<long, targetX + bounds>, targetY + bounds> geologic;
std::array<std::array<long, targetX + bounds>, targetY + bounds> erosion;

enum class Type {
	rocky = 0,
	wet,
	narrow,
};

std::array<std::array<Type, targetX + bounds>, targetY + bounds> type;

enum class Gear {
	neither = 0,
	torch,
	climbing, 
};

struct Coor {
	long x;
	long y;
	Gear g;
};

bool operator<(Coor a, Coor b) {
	return std::tie(a.x, a.y, a.g) < std::tie(b.x, b.y, b.g);
}

bool operator==(Coor a, Coor b) {
	return std::tie(a.x, a.y, a.g) == std::tie(b.x, b.y, b.g);
}


long D(Coor a, Coor b) {
	return (a.g == b.g) ? 1 : 7;
}

std::map<Coor, std::vector<Coor>> graph;

void fill_array() {
	for (auto y = 0; y < geologic.size(); ++y) {
		for (auto x = 0; x < geologic[y].size(); ++x) {
			if (x == 0 && y == 0)
				geologic[y][x] = 0;	
			else if (x == targetX && y == targetY)
				geologic[y][x] = 0;
			else if (y == 0)
				geologic[y][x] = (x * 16807);
			else if (x == 0)
				geologic[y][x] = (y * 48271);
			else
				geologic[y][x] = erosion[y-1][x] * erosion[y][x-1];

			erosion[y][x] = (geologic[y][x] + depth) % 20183;
			type[y][x] = Type(erosion[y][x] % 3);
		}

	}
}

long risk_level() {
	long s = 0;
	for (auto y = 0; y <= targetY; ++y)
		for (auto x = 0; x <= targetX; ++x)
			s += long(type[y][x]);
	return s; 
}
void print_levels() {
	for (auto y = 0; y <= targetY; ++y) {
		for (auto x = 0; x <= targetX; ++x) {
			std::cout << ((type[y][x] == Type::rocky) ? "." : (type[y][x] == Type::wet) ? "=" : "|");
		}
		std::cout << "\n";
	}
}

//In rocky regions,  you can use the climbing gear or the torch.
//In wet regions,    you can use the climbing gear or neither tool
//In narrow regions, you can use the torch         or neither tool

void make_graph() {
	for (auto y = 0; y < geologic.size(); ++y) {
		for (auto x = 0; x < geologic[y].size(); ++x) {
			for (auto g = Gear::neither; g <= Gear::climbing; g = Gear(int(g)+1)) {
				Coor c = {x, y, g};
				if (int(type[y][x]) == int(g))
					continue;
				for (long dy = -1; dy <= 1; ++dy) {
					for (long dx = -1; dx <= 1; ++dx) {
						if (abs(dx) + abs(dy) == 1) {
							Coor nb = {x + dx, y + dy, g};
							if (nb.y < 0 || nb.y >= geologic.size() || nb.x < 0 || nb.x >= geologic[y].size())
								continue;
							if (int(type[nb.y][nb.x]) == int(g))
								continue;
							graph[c].push_back(nb);
						}
					}
				}

				for (auto dg = Gear::neither; dg <= Gear::climbing; dg = Gear(int(dg)+1)) {
					if (g == dg || int(type[y][x]) == int(dg))
						continue;
					graph[c].emplace_back(Coor{x, y, dg});
				}

			}
		}
	}
}

using Dist = std::tuple<long, Coor>;

long shortest_route() {
	Coor target = {targetX, targetY, Gear::torch};
	Coor source = {0, 0, Gear::torch};
	std::priority_queue<Dist, std::vector<Dist>, std::greater<>> Q;
	std::set<Coor> seen;
	std::map<Coor,long> finald;
	std::map<Coor,Coor> prev;

	Q.emplace(std::make_tuple(0, source));

	while (!Q.empty()) {
		auto [d, c] = Q.top();
		Q.pop();

		if (auto [_, inserted] = seen.insert(c); !inserted)
			continue;

		if (c == target) {
			break;
		}

		for (auto nb : graph[c]) {
			long nd = d + D(c, nb);
			if (finald.find(nb) == finald.end() || nd < finald.at(nb)) {
				finald[nb] = nd;
				prev[nb] = c;
				Q.emplace(std::make_tuple(nd, nb));
			}
		}
	}

	return finald[target];
}

int main() {
	fill_array();
	std::cout << risk_level() << "\n";
	//print_levels();
	make_graph();
	std::cout << shortest_route() << "\n";
}
