// AdventOfCode 2021, day 1

// compile with : gcc step_1.cpp
// run with     : ./a.out

#include "../utils.h"   // include some functions and more important some includes...


int count_increases(const std::vector<int>& ints) {

    int cnt = 0;
    int n = ints.size();

    for (int i=0; i < n-1; i++) {
    	if (ints[i+1] > ints[i]) {
	    cnt++;
	}
    }
    return cnt;
}


int main(int argc, char* argv[]) {

    // step 1
    std::vector<int> depths = ints_from_file("input.txt");
    std::cout << "day 1, step 1 solution : " << count_increases(depths) << std::endl;

    // step 2
    std::vector<int> windowed;
    int n = depths.size();
    for (int i=0; i < n-2; i++) {
        windowed.push_back(depths[i] + depths[i+1] + depths[i+2]);
    }
    std::cout << "day 1, step 2 solution : " << count_increases(windowed) << std::endl;

    return EXIT_SUCCESS;
}

