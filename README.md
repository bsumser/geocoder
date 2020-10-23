---
   ###### author(s): [Justin stewart](https://github.com/stewartjustinl), [Brett Sumser](https://github.com/bsumser)

---
- [Description](#description)
- [Codebase](#codebase)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage(command line)](#usage)
- [Turn-by-turn Algorithm](#turn-by-turnalgorithm)
---
## Description

Geocoder is an attempt to produce turn by turn directions from a gpx file/route by using the [Texas A&M Geoservices web API.](https://geoservices.tamu.edu/Services/Geocode/). To accomplish the intended results we used a reverse geocoder that takes in the Longitude and Latitude coordinates and returns addresses. We then use the addresses to return to the user a set of turn by turn directions as well as the distance between each turn. 

---
## Codebase
To find out information about the functionality of the code you can look inside the "main.py" file. Each of the functions have been documented using python docstrings if the user wishes to print the docstrings for main.py they can do so by the below command
```
python3 main.py --docs
```
---
## Installation
 To install you only need to clone the repo.
It is possible that you will have to install some dependency libraries, this can be found detailed below under [Dependencies](#dependencies).

---
## Dependencies

   Geocoder relies upon the requests, numpy, and gpxpy module, you can use "pip3" to install these via the command below. The user will need there own valid Texas A&M geocoding API key as well to utilize their service for program functionality.

```
pip3 install -r requirements.txt
```

---
## Usage(command line)
Once you have the repo cloned, and have sorted out any dependency issues, simply run:
```
python3 main.py
```
You can also run the program to produce more output information for functions
by typing 
```
python3 main.py -v
```
Or
```
python3 main.py --verbose
```
To run the program and save the debug portion of the code to a log file use the command:
```
python3 main.py -d
```
Or
```
python3 main.py --debug
```
To clear log files from program use the command:
```
python3 main.py -c
``` 
To run the program using a sample .gpx file that we provide use the command:
```
python3 main.py -s 
```
Or
```
python3 main.py --sample
```
Once you have made your choice of how you want to run the program. You will be prompted to enter in a file path to feed the .gpx file and a valid user API key.   

---
## Turn-by-turn Algorithm
Below is pseudocode for the turn-by-turn algorithm that geocode utilizes to determine at which points in the route turns occur. To accomplish this we used a modified version of binary search to return a list of key points that turns are made. 


![Alt text](img/Algorithm.png?raw=true "Algorithm")

___

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
