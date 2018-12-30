#include <array>
#include <string>
#include <fstream>
#include <iostream>
#include <tuple>
#include <unordered_set>
#include <vector>

using registers = std::array<int, 6>;
using instr_p = void (*)(int A, int B, int C, registers&);

struct instruction {
	instr_p instr;
	std::string name;
	int A;
	int B;
	int C;
};

using instruction_list = std::vector<instruction>;

void addr(int A, int B, int C, registers& R) { R[C] = R[A] + R[B]; }
void addi(int A, int B, int C, registers& R) { R[C] = R[A] + B; }
void mulr(int A, int B, int C, registers& R) { R[C] = R[A] * R[B]; }
void muli(int A, int B, int C, registers& R) { R[C] = R[A] * B; }
void banr(int A, int B, int C, registers& R) { R[C] = R[A] & R[B]; }
void bani(int A, int B, int C, registers& R) { R[C] = R[A] & B; }
void borr(int A, int B, int C, registers& R) { R[C] = R[A] | R[B]; }
void bori(int A, int B, int C, registers& R) { R[C] = R[A] | B; }
void setr(int A, int  , int C, registers& R) { R[C] = R[A]; }
void seti(int A, int  , int C, registers& R) { R[C] = A; }
void gtir(int A, int B, int C, registers& R) { R[C] = int(A > R[B]); } 
void gtri(int A, int B, int C, registers& R) { R[C] = int(R[A] > B); }
void gtrr(int A, int B, int C, registers& R) { R[C] = int(R[A] > R[B]); }
void eqir(int A, int B, int C, registers& R) { R[C] = int(A == R[B]); }
void eqri(int A, int B, int C, registers& R) { R[C] = int(R[A] == B); }
void eqrr(int A, int B, int C, registers& R) { R[C] = int(R[A] == R[B]); }

std::tuple<int, instruction_list> read_input(std::string const& input) {
	std::fstream file(input);
	int ip_reg;
	std::string skip;
	file >> skip >> ip_reg;

	instruction instr;
	instruction_list program;
	while (file >> skip >> instr.A >> instr.B >> instr.C) {
		if (skip == "addr") {
			instr.instr = addr;
		} else if (skip == "addi") {
			instr.instr = addi;
		} else if (skip == "mulr") {
			instr.instr = mulr;
		} else if (skip == "muli") {
			instr.instr = muli;
		} else if (skip == "banr") {
			instr.instr = banr;
		} else if (skip == "bani") {
			instr.instr = bani;
		} else if (skip == "borr") {
			instr.instr = borr;
		} else if (skip == "bori") {
			instr.instr = bori;
		} else if (skip == "setr") {
			instr.instr = setr;
		} else if (skip == "seti") {
			instr.instr = seti;
		} else if (skip == "gtir") {
			instr.instr = gtir;
		} else if (skip == "gtri") {
			instr.instr = gtri;
		} else if (skip == "gtrr") {
			instr.instr = gtrr;
		} else if (skip == "eqir") {
			instr.instr = eqir;
		} else if (skip == "eqri") {
			instr.instr = eqri;
		} else if (skip == "eqrr") {
			instr.instr = eqrr;
		} else {
			throw std::runtime_error("fail");
		}
		instr.name = skip;
		program.push_back(instr);
	}
	return std::make_tuple(ip_reg, program);
}

long evaluate(int ip_reg, instruction_list& program, registers& R) {
	std::unordered_set<int> seen;
	int ip = R[ip_reg];
	bool first = true;
	int last = -1;
	long iterations = 0;
	while (++iterations) {
		R[ip_reg] = ip;
		auto& cur = program[ip];
		if (ip == 28) {
			if (std::exchange(first, false))
				std::cout << "Part 1: " << R[4] << "\n";
			if (auto [it, inserted] = seen.insert(R[4]); !inserted) {
				std::cout << "Part 2: " << last << "\n";
				break;						
			}
			last = R[4];
		}
		//std::cout << "ip=" << ip << " [" << R[0] << ", " << R[1] << ", "  << R[2] << ", "  << R[3] << ", "  << R[4] << ", "  << R[5] << "] " << cur.name << " " << cur.A << " " << cur.B << " " << cur.C;
		cur.instr(cur.A, cur.B, cur.C, R);
		ip = R[ip_reg] + 1;
		//std::cout << " [" << R[0] << ", " << R[1] << ", " << R[2] << ", " << R[3] << ", " << R[4] << ", " << R[5] << "]\n";
		if (ip >= program.size())
			break;
	}
	return iterations;
}

int main(int argc, char** argv) {
	std::string input = "input.txt";
	if (argc > 1)
		input = argv[1];	
	instruction_list program;
	int ip_reg;
	std::tie(ip_reg, program) = read_input(input);
	registers R = {{0,0,0,0,0,0}};
	auto it = evaluate(ip_reg, program, R);
	std::cout << "iterations: " << it << "\n";
}

