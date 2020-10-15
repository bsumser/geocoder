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
## Turn-by-turn Algorithm
Below is pseudocode for the turn-by-turn algorithm that geocode utilizes to determine
at which points in the route turns occur.
![Alt text](img/equation.svg?raw=true "Algorithm")

<!---
\begin{split}
N = \text{# of address's elements}\\
S = \text{index of starting element}\\
E = \text{index of ending element}\\
M = \text{Midpoint between S & E}\\
\text{def key_points(S,E)}:\\
&M = \left \lceil{\frac{E-S}{2}}\right \rceil + S\\
&E = M\\
&if \text{ }arr[S] = arr[N]\\
&&\text{points_arr.append[arr[S]]}\\
&&\text{return}\\
&if\text{ }arr[S] = arr[M]\\
&&S = M + 1\\
&&\text{points_arr.append[arr[M]]}\\
&&E = N\\
&&\text{key_points(S,E)}\\
&else\\
&&\text{key_points(S,E)}\\
\end{split}
-->