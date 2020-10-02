#include <iostream>
#include <string>
#include <vector>
#include <cpprest/http_client.h>
#include <cpprest/filestream.h>

using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace concurrency::streams;       // Asynchronous streams

void helpArgs();
void loadFile();
void getUserInputAddress(char *argv[]);
void htttpRequestBuilder(std::vector<std::string> address);     //Test request to google using cpprestsdk
void htttpRequestBuilder(std::vector<int> coord);     //Test request to google using cpprestsdk

int main(int argc, char *argv[])
{
    std::cout << "starting main loop, arguments are: ";
    for (int i = 0; i < argc; ++i)
        std::cout << argv[i] << std::endl;
    switch(argc) {
        case 1:
            std::cout << "You have entered 0 arguments" << std::endl;
            break;
        case 2:
            std::cout << "You have entered 1 argument: "<< argv[1] << " displaying help options"<< std::endl;
            helpArgs();
            break;
        case 3:
            std::cout << "You have entered 2 argument: "<< argv[1] << " " << argv[2] << std::endl;
            if (std::string(argv[1]) == "-f")
                loadFile();
            break;
        case 4:
            std::cout << "You have entered 3 argument: "<< argv[1] << " " << argv[2] << " " << argv[3] << std::endl;
            if (std::string(argv[1]) == "-c")
            getUserInputAddress(argv);
            break;
        default:
            std::cout << "default case hit, unrecognized flags input" << std::endl;
    }
    std::cout << "testing httpRequestBuilder" << std::endl;
    std::vector<std::string> address;
    address.push_back("9355 Burton Way");
    address.push_back("Beverly Hills");
    address.push_back("ca");
    address.push_back("90210");
    htttpRequestBuilder(address);
    return 0;
}

void helpArgs() {
    std::cout << "run with '-help' to list available options" << std::endl;
    std::cout << "run with '-c -lat,long -lat,long' to process path between coordinates (first coordinate being the start)" << std::endl;
    std::cout << "run with '-f /path/to/file' to load in coordinates from a text file" << std::endl;
}

void loadFile() {
    std::cout << "you have chosen to load coordinates from a file with path ''" << std::endl;
}

void getUserInputAddress(char *argv[]) {

}

void htttpRequestBuilder(std::vector<std::string> address) {     //Test request to google using cpprestsdk
    auto fileStream = std::make_shared<ostream>();

    //open the stream to the output file
    pplx::task<void> requestTask = fstream::open_ostream(U("data/result.html")).then([=](ostream outFile) {
        *fileStream = outFile;
        // Create http_client to send the request.
        http_client client(U("https://geoservices.tamu.edu/Services/Geocode/WebService/"));

        // Build request URI and start the request.
        uri_builder builder(U("/GeocoderService_V04_01.asmx"));
        builder.append_query(U("streetAddress"),U(address[0]));
        builder.append_query(U("city"),U(address[1]));
        builder.append_query(U("state"),U(address[2]));
        builder.append_query(U("zip"),U(address[3]));
        builder.append_query(U("apikey"),U(""));
        builder.append_query(U("format"),U("csv"));
        builder.append_query(U("census"),U("true"));
        builder.append_query(U("censusYear"),U("2010"));
        builder.append_query(U("notStore"),U("false"));
        builder.append_query(U("version"),U("4.01"));
        std::cout << builder.to_string() << std::endl;
        return client.request(methods::GET, builder.to_string());
    })

    .then([=](http_response response) {     //handle the response from the server
        std::cout << "received response status code: " << response.status_code() << std::endl;

        //write reponse to the file
        return response.body().read_to_end(fileStream->streambuf());
    })

    .then([=](size_t) {   //close the file stream
        return fileStream->close();
    });

    try //wait for any I/O to finish and handle exceptions
    {
        requestTask.wait();

    }
    catch (const std::exception &e)
    {
        std::cout << "Error exception: " << e.what() << std::endl;
    }
}