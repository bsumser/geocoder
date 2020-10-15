import requests
import json
import gpxpy
import gpxpy.gpx
import numpy as np
from numpy import arctan2, sin, cos, arccos, degrees, radians
import numpy as np
import math
import logging
import argparse

def main():
    parseArgs()
    path = "data/sample.gpx"
    coordinateList = gpxParser(path)    #parse sample file at path to list of points
    queryFields = getUserInput(coordinateList[0])   #pass coordinate point to from query fields for API
    # json_data = sendRequest(queryFields)   #send request to API with query fields
    # address = getAddress(json_data)    #get address field from json from request to API
    geocodeCoordinate(coordinateList[0], coordinateList[1])     #get heading from comparison of start and end points
    getDistance(coordinateList[0], coordinateList[1]) 
    #addressListTest = addressParser(coordinateList)

    address = np.array([' main st ', ' main st ', ' main st ', ' bob ave ',
                        ' bob ave ', ' bob ave ', ' sam ', ' sam ', ' tim rd ',
                        ' tim rd ', ' tim rd ', ' tim rd '])

    key = np.array([], dtype=int)  # initializes empty array using numpy library

    start = 0  # starting element to make the comparison
    n = (len(addressListTest) - 1)  # n = number of total elements in the address
    end = n  # ending element to make the comparison
    key_points(start, end, key, addressListTest)
    
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="increases output verbosity", action="store_true")
    args = parser.parse_args()
    if (args.verbose):
        logging.basicConfig(level=logging.INFO)
        print("-v or --verbose flag used, logging mode set to info")
    else:
        print("no arguments selected")

    address = np.array([' main st ', ' main st ', ' main st ', ' bob ave ',
                        ' bob ave ', ' bob ave ', ' sam ', ' sam ', ' tim rd ',
                        ' tim rd ', ' tim rd ', ' tim rd '])

    key = np.array([], dtype=int)  # initializes empty array using numpy library

    start = 0  # starting element to make the comparison
    n = (len(address) - 1)  # n = number of total elements in the address
    end = n  # ending element to make the comparison
    key_points(start, end, key, address)

def getAddress(json_data):    #Get the address from json response from API
    return json_data['StreetAddresses'][0]['StreetAddress']

def sendRequest(queryFields):
    httpClient = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx?"
    completeQuery = httpClient + queryFields
    response = requests.get(completeQuery)
    json_data = json.loads(response.text)
    return(json_data)

def getUserInput(coordinate):
    lat = "lat=" + str(coordinate.latitude)
    lon = "&lon=" + str(coordinate.longitude)
    state = "&state=or"
    apikey = "&apikey=1553f4ca4c3e4e84a4c22adc3aae1886"
    format = "&format=json"
    notStore = "&notStore=false"
    version = "&version=4.10"
    queryFields = lat + lon + state + apikey + format + notStore + version
    logging.info("getUserInput() query is: %s",queryFields)
    return queryFields

def getBearing(endPoint, startPoint):     #Function to determine bearing
    endLatitude = radians(float(endPoint.latitude))
    endLongitude = radians(float(endPoint.longitude))
    startLatitude = radians(float(startPoint.latitude))
    startLongitude = radians(float(startPoint.longitude))
    X = cos(endLatitude) * sin((endLongitude - startLongitude))
    Y = (cos(startLatitude) * sin(endLatitude)) - (sin(startLatitude) * cos(endLatitude) * cos((endLongitude - startLongitude)))
    bearingDegrees = degrees(arctan2(X,Y))
    bearingDegrees = (bearingDegrees + 360) % 360
    logging.info("Bearing in degrees is %i", bearingDegrees)
    return getCompassDirection(bearingDegrees)

def getCompassDirection(bearingDegrees):
    direction = int(round(bearingDegrees / 22.5))
    choices = {
        1: "NNE",
        2: "NE",
        3: "ENE",
        4: "E",
        5: "ESE",
        6: "SE",
        7: "SSE",
        8: "S",
        9: "SSW",
        10: "SW",
        11: "WSW",
        12: "W",
        13: "WNW",
        14: "NW",
        15: "NNW",
        16: "N"
    }
    return choices.get(direction, 'default')

def getDistance(endPoint, startPoint):  #distance between coordinates using haversine formula
    endLatitude = radians(float(endPoint.latitude))
    endLongitude = radians(float(endPoint.longitude))
    startLatitude = radians(float(startPoint.latitude))
    startLongitude = radians(float(startPoint.longitude))
    unit = "miles"

    distance = 3963.0 * arccos((sin(startLatitude) * sin(endLatitude)) +
    cos(startLatitude) * cos(endLatitude) * cos(endLongitude - startLongitude))

    if (distance < 1):
        distance = int(round(distance * 5280))
        unit = "feet"

    distanceString = " distance from previous point is {0} {1}".format(distance, unit)
    logging.info("%s",distanceString)
    return distanceString

def geocodeCoordinate(endPoint, startPoint):
    endLatitude = float(endPoint.latitude)
    endLongitude = float(endPoint.longitude)
    startLatitude = float(startPoint.latitude)
    startLongitude = float(startPoint.longitude)
    queryFields = getUserInput(endPoint)
    bearing = getBearing(endPoint, startPoint)
    json_data = sendRequest(queryFields)
    address = getAddress(json_data)
    distance = getDistance(endPoint, startPoint)
    logging.info("Location is (%i,%i)",endLatitude, endLongitude)
    return address


def gpxParser(path):
    coordinateList = []
    gpx_file = open(path,'r')

    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinateList.append(point)
    print(coordinateList[0].latitude)
    return coordinateList

def key_points(start, end, key, address):

    n = (len(address)-1)  # n = number of total elements in the address
    midpoint = int(math.ceil((end - start) / 2) + start)  # ceiling function to find midpoint
    # print('midpoint', midpoint)

    end = midpoint

    # 1 Base case(s) 0 turns are made, or we have reached the end of the points.
    if address[start] == address[n]:
        # print('case1')
        key = np.append(key, n)
        print_key(key, address)
        exit()

    # 2 midpoint doesn't match starting and starting point is next to end point
    if address[start] != address[midpoint] and (start+1) == end:
            key = np.append(key, start)
            start = start+1
            end = n
            key_points(start, end, key, address)

    # 3 midpoint doesn't match starting and starting point is not next to end point
    if address[start] != address[midpoint] and (start+1) != end:
        # print('case3')
        key_points(start, end, key, address)

    # 4 starting point matches midpoint
    if address[start] == address[midpoint]:
        # print('case4')
        start = midpoint
        end = n
        key_points(start,end, key, address)


def print_key(key, address): # key is the array holding the elements

    if len(key) == 1:
        print('No turns made')

    i = 0
    print('\nYour turns were made at the points of the first column and the streets of the second column: \n')
    while i < len(key):
        print( key[i], address[key[i]])
        i = i+1

def addressParser(coordinateList):
    addressStringList = np.array([],dtype=object)
    print(coordinateList[0])

    for i in range(len(coordinateList)):
        address = geocodeCoordinate(coordinateList[i],coordinateList[i])
        address = address.split(" ",1)[1]
        addressStringList = np.append(addressStringList, address)
    return addressStringList

if __name__ == "__main__":
    main()