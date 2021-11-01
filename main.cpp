#include "video.h"

#include <fstream>
#include <utility>
#include <vector>
#include <list>


// ./a.out brandName1 brandName2 brandName3 file.csv

int readCSV(char* fileName){
    std::ifstream csv(fileName);

    // check argc == 3
    if(csv.is_open() == false){
        std::cerr << "ERROR: Cannot open" << fileName << "." << std::endl;
        return 1;
    }

    // read loop
    while(csv.good()){

    }

    return 0;
}


int main( int argc, char* argv[]){

    // check argc == 3
    if(argc < 3){
        std::cerr << "ERROR : There should be at least 3 command line arguments." << std::endl;
        return 1;
    }

    // create brand objects for each

    // process csv
    readCSV(argv[2]);

    // read csv

    return 0;
}