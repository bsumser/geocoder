import requests
import json
import gpxpy
import gpxpy.gpx
import numpy as np
import math
import logging
import argparse
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from numpy import arctan2, sin, cos, arccos, degrees, radians

def main():
    parseArgs()
    path = "data/sample.gpx"
    coordinateList = gpxParser(path)    #parse sample file at path to list of points
    queryFields = getUserInput(coordinateList[0])   #pass coordinate point to from query fields for API
    #json_data = sendRequest(queryFields)   #send request to API with query fields
    #address = getAddress(json_data)    #get address field from json from request to API
    #geocodeCoordinate(coordinateList[0], coordinateList[1])     #get heading from comparison of start and end points
    getDistance(coordinateList[0], coordinateList[1]) 

    for i in range(len(coordinateList) - 2):
        bearingDifCalc(coordinateList[i], coordinateList[i+1], coordinateList[i+2])
    #addressListTest = addressParser(coordinateList)

    # test multiThreadQueryMaker
    # queryList = multiThreadQueryMaker(coordinateList)

    # check queryList
    # print(queryList)

    # run the query list
    # queryRunner(queryList)

    address = np.array([' main st ', ' main st ', ' main st ', ' bob ave ',
                        ' bob ave ', ' bob ave ', ' sam ', ' sam ', ' tim rd ',
                        ' tim rd ', ' tim rd ', ' tim rd '])

    key = np.array([], dtype=int)  # initializes empty array using numpy library

    start = 0  # starting element to make the comparison
    n = (len(address) - 1)  # n = number of total elements in the address
    end = n  # ending element to make the comparison
    keyArray = key_points(start, end, key, address)
    print(keyArray)
    turnDetector(keyArray, address, coordinateList)
    
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="increases output verbosity", action="store_true")
    args = parser.parse_args()
    if (args.verbose):
        logging.basicConfig(level=logging.INFO)
        print("-v or --verbose flag used, logging mode set to info")
    else:
        print("no arguments selected")

def getAddress(json_data):    #Get the address from json response from API
    return json_data['StreetAddresses'][0]['StreetAddress']

def sendRequest(completeQuery):
    # try/catch block for requests error handling
    response = requests.get(completeQuery)
    responseCode = response.status_code
    json_data = json.loads(response.text)
    #logging.info("sendRequest() request URL is: %s \n Status Code:%i",completeQuery,responseCode)
    return json_data

def getUserInput(coordinate):
    httpClient = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx?"
    lat = "lat=" + str(coordinate.latitude)
    lon = "&lon=" + str(coordinate.longitude)
    state = "&state=or"
    apikey = "&apikey=1553f4ca4c3e4e84a4c22adc3aae1886"
    format = "&format=json"
    notStore = "&notStore=false"
    version = "&version=4.10"
    completeQuery = httpClient + lat + lon + state + apikey + format + notStore + version
    #logging.info("Complete query: %s",completeQuery)
    return completeQuery

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
    return bearingDegrees

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
    # TODO: perhaps change this function to be overload, so you could call with one coordinate
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
        return key

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
    # numpy array of python objects to feed into key_points()
    addressStringList = np.array([],dtype=object)

    # loop through coordinateList and extract address from each point
    for i in range(len(coordinateList)):
        address = geocodeCoordinate(coordinateList[i],coordinateList[i])

        # shave off the number part of the address
        address = address.split(" ",1)[1]

        # verbose information about address produced
        logging.info("adding address:%s to addressStringList")

        # append address to addressStringList
        addressStringList = np.append(addressStringList, address)
    return addressStringList

def multiThreadQueryMaker(coordinateList):
    launcherQueryStringList = []

    for i in range(len(coordinateList)):
        logging.info("calling getUserInput on coordinateList index %i, point:(%i,%i)",
        i, coordinateList[i].latitude,coordinateList[i].longitude)
        # convert coordinate to query parameters
        completeQuery = getUserInput(coordinateList[i])

        # append the completeQuery to launcherQueryStringList
        launcherQueryStringList.append(completeQuery)

    return launcherQueryStringList

def queryRunner(launcherQueryStringList):
    threads = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(len(launcherQueryStringList)):
            file_name = uuid.uuid1()
            threads.append(executor.submit(sendRequest,launcherQueryStringList[i]))
        
        for task in as_completed(threads):
            print(task.result())

def bearingDifCalc(startPoint, midPoint, endPoint):
    bearingDelta1 = getBearing(midPoint, startPoint)
    bearingDelta2 = getBearing(endPoint, midPoint)
    totalBearingDelta = bearingDelta2 - bearingDelta1
    logging.info("change in bearing is: %i = %i - %i",totalBearingDelta, bearingDelta2, bearingDelta1)

def turnDetector(turnArray, addressArray, coordinateList):
    # given array of turns point indexes, and matching array of addresses to 
    # array of coordinates, detect what kind of turn happens
    print("turn detector")
    for i in turnArray:
        #bearingDifCalc(coordinateList[turnArray[i] - 1],
        #coordinateList[turnArray[i]], coordinateList[turnArray[i] + 1])
        logging.info("Turn detected at addressArray index %i at address %s at coordinate(%s)",
        turnArray[i],addressArray[turnArray[i]],coordinateList[turnArray[i]])

if __name__ == "__main__":
    main()