## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)

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