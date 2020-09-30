## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)

## Description
Geocoder is an attempt to produce turn by turn directions by using the [Texas A&M Geoservices web API.](https://geoservices.tamu.edu/Services/Geocode/) Programmed in C++, geocoder also makes use of Microsoft's [C++ REST SDK](https://github.com/microsoft/cpprestsdk) in order to facilitate access to the geoservices web API.

## Installation
The geocoder repo includes a Makefile, and can be compiled with make. Use make clean to remove the executable if needed.

## Dependencies
Geocoder relies upon the [C++ REST SDK](https://github.com/microsoft/cpprestsdk), so
please take whatever steps are neccesary on the repo to install onto your system.

## Usage
Geocoder has a help command available if you ever need to check the arguments in the terminal.
```
./main -help
```
There are a few options for loading in coordinates to geocoder.
```
./main -f /path/to/file
```
Running geocoder in this manner will let you load a text file of coordinates into the program.

If you want to, you can also input coordinates via the command line.
```
./main -c -latitudeStart,longitudeStart -latitudeFinish,longitudeFinish
```