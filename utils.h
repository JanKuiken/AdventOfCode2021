//
// header-only utility functions for AdventOfCode 2021
//

#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>

#include <cstdlib>


// for day 1 and maybe others, read file, return vector of ints
std::vector<int> ints_from_file(std::string filename) {

    std::cout << "ints_from_file : " << filename << std::endl; 
    std::vector<int> retval;
    std::ifstream infile(filename);
    if (!infile.good()) {
        std::cout << "ints_from_file : could not read : " << filename << std::endl; 
        std::exit(EXIT_FAILURE);
    }
    int i;
    int cnt = 0;
    while (infile >> i) {
        retval.push_back(i);
	cnt++;
    }
    std::cout << "ints_from_file : read " << cnt << " integers" << std::endl; 
    return retval;
}


