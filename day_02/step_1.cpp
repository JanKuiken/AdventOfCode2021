// AdventOfCode 2021, day 2

// compile with : gcc step_1.cpp
// run with     : ./a.out

#include "../utils.h"   // include some functions and more important some includes...
                        // ... and typedef's

int main(int argc, char* argv[]) {

    // step 1
    std::vector<str_int_pair> commands = str_int_pairs_from_file("input.txt");

    // start position
    int hpos  = 0;
    int depth = 0;

    for (auto c : commands) {
        std::string direction = c.first;
	int X = c.second;
        if (direction == "forward") hpos  += X;
        if (direction == "down"   ) depth += X;
        if (direction == "up"     ) depth -= X;
    }
    std::cout << "=== step 1 ====" << std::endl;
    std::cout << "hpos   :  " << hpos         << std::endl;
    std::cout << "depth  :  " << depth        << std::endl;
    std::cout << "answer :  " << hpos * depth << std::endl;

    // step 2

    // start position
    hpos  = 0;
    depth = 0;
    int aim   = 0;

    for (auto c : commands) {
        std::string direction = c.first;
	int X = c.second;
        if (direction == "forward") { hpos  += X; depth += aim * X; }
        if (direction == "down"   ) aim += X;
        if (direction == "up"     ) aim -= X;
    }
    std::cout << "=== step 2 ====" << std::endl;
    std::cout << "hpos   :  " << hpos         << std::endl;
    std::cout << "depth  :  " << depth        << std::endl;
    std::cout << "answer :  " << hpos * depth << std::endl;

    return EXIT_SUCCESS;
}

