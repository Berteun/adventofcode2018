#include <array>
#include <iostream>

int grid_sum(std::array<std::array<int, 300>, 300> const& grid, int sq, int x, int y) {
	int s = 0;
	for (int cy = y ; cy < y + sq; ++cy)
		for (int cx = x ; cx < x + sq; ++cx)
			s += grid[cy][cx];
	return s;
}

int main() {
	std::array<std::array<int, 300>, 300> grid;
	const int serial = 2187;

	for (int y = 0; y < 300; ++y)
		for (int x = 0; x < 300; ++x)
			grid[y][x] = (((((x + 10) * y + serial)) * (x + 10) % 1000)/ 100) - 5;

	int sq_size = -1;
	int bx = -1;
	int by = -1;
	int m = -1;
	for (int y = 0; y < 299; ++y)
		for (int x = 0; x < 299; ++x) 
			for (int sq = 1; sq < std::min(300-y,300-x); ++sq) {
				int s = grid_sum(grid, sq, x, y);
				if (s > m) {
					m = s;
					sq_size = sq;
					bx = x;
					by = y;
				}
			}

	std::cout << bx << "," << by << "," << sq_size << "\n";
}
