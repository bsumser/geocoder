#include <iostream>
#include <string>
#include <cpprest/http_client.h>
#include <cpprest/filestream.h>

using namespace std;

void helpArgs();
void loadFile();
void loadCoord(int latStart, int longStart, int latFinish, int longFinish);

int main(int argc, char *argv[])
{
    cout << "starting main loop, arguments are: ";
    for (int i = 0; i < argc; ++i)
        cout << argv[i] << endl;
    switch(argc) {
        case 1:
            cout << "You have entered 0 arguments" << endl;
            break;
        case 2:
            cout << "You have entered 1 argument: "<< argv[1] << " displaying help options"<< endl;
            helpArgs();
            break;
        case 3:
            cout << "You have entered 2 argument: "<< argv[1] << " " << argv[2] << endl;
            if (string(argv[1]) == "-f")
                loadFile();
            break;
        case 4:
            cout << "You have entered 3 argument: "<< argv[1] << " " << argv[2] << " " << argv[3] << endl;
            if (string(argv[1]) == "-c")
                loadCoord(1,1,1,1);
            break;
        default:
            cout << "default case hit, unrecognized flags input" << endl;
    }
    return 0;
}

void helpArgs() {
    cout << "run with '-help' to list available options" << endl;
    cout << "run with '-c -lat,long -lat,long' to process path between coordinates (first coordinate being the start)" << endl;
    cout << "run with '-f /path/to/file' to load in coordinates from a text file" << endl;
}

void loadFile() {
    cout << "you have chosen to load coordinates from a file with path ''" << endl;
}

void loadCoord(int latStart, int longStart, int latFinish, int longFinish) {
    cout << "you have entered coordinates via command line of: " << latStart << "," << longStart << " " << latFinish << "," << longFinish << endl;
}