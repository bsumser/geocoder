## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Turn-by-turn Algorithm](#turn-by-turnalgorithm)

## Description
Geocoder is an attempt to produce turn by turn directions from a gpx file/route by using the [Texas A&M Geoservices web API.](https://geoservices.tamu.edu/Services/Geocode/). 

## Installation
To install you only need to clone the repo.
It is possible that you will have to install some dependency libraries, this can be found detailed below under [Dependencies](#dependencies).

## Dependencies
Geocoder relies upon the requests, and gpxpy module, you can use pip to install these if you use pip.

```
pip install requests
pip install gpxpy
```

## Usage
Once you have the repo cloned, and have sorted out any dependency issues, simply run:
```
python main.py
```
You can also run the program to produce more output information for functions
by typing 
```
python main.py -v
```
or
```
python main.py --verbose
```
## turn-by-turnalgorithm
Below is pseudocode for the turn-by-turn algorithm that geocode utilizes to determine
at which points in the route turns occur.