#!/bin/bash
# Test script for all modes of geocoder.
make
./main
./main -help
./main -f /path/to/file
./main -c -1,1 -1,1
make clean