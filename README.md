---
   ###### author(s): [Justin stewart](https://github.com/stewartjustinl), [Brett Sumser](https://github.com/bsumser), [Jake Petersen](https://github.com/jpeter17)

---
- [Description](#description)
- [Codebase](#codebase)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Turn-by-turn Algorithm](#turn-by-turnalgorithm)
---
## Description

Geocoder is an attempt to produce turn by turn directions from a gpx file/route by using the [Texas A&M Geoservices web API.](https://geoservices.tamu.edu/Services/Geocode/). To accomplish the intended results we used a reverse geocoder that takes in the Longitude and Latitude coordinates and returns addresses. We then use the addresses to return to the user a set of turn by turn directions as well as the distance between each turn. 

---
## Codebase
To find out information about the functionality of the code you can look inside the "main.py" file. Each of the functions have been documented using python docstrings if the user wishes to print the docstrings for main.py they can do so by the below command
```
python3 flaskr/algorithm.py --docs
```

---
## Dependencies

   Geocoder relies upon the requests, numpy, and gpxpy module, you can use "pip3" to install these via the command below. The user will need there own valid Texas A&M geocoding API key as well to utilize their service for program functionality.

---
## Installation

Clone the repo 

```bash
git clone https://github.com/jpeter17/geocoder.git
```

Create a Virtual Environment in the project folder

```bash
mkdir <venv_name>
python3 -m venv <venv_name>
```

Activate the Virtual Environment 

```bash
. <venv_name>/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements to run this project.

```bash
pip install -e . 
```

Setup Environment Variables and run the project

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run
```

Your project will be available at http://127.0.0.1:5000/

---
## Usage 

Create a User by clicking [Register](http://127.0.0.1:5000/auth/register)

Your Texas A&M API Key will be entered in here 

Log-in and Create a new trip by clicking [New](http://127.0.0.1:5000/create)

Acceptable file formats include .gpx 

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