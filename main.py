import requests
import json
import gpxpy
import gpxpy.gpx
import numpy as np
import math
import time
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from numpy import arctan2, sin, cos, arccos, degrees, radians

def main():
    parseArgs()
    path = "data/sample.gpx"
    
    # parse sample file at path to list of points
    coordinateList = gpxParser(path)
    
    #addressListTest = addressParser(coordinateList)

    # test multiThreadQueryMaker
    queryList = multiThreadQueryMaker(coordinateList)

    # run the query list to get the address list
    addressListTest = queryRunner(queryList)

    address = np.array([' main st ', ' main st ', ' main st ', ' bob ave ',
                        ' bob ave ', ' bob ave ', ' sam ', ' sam ', ' tim rd ',
                        ' tim rd ', ' tim rd ', ' tim rd '])

    # initializes empty array using numpy library
    key = np.array([], dtype=int)  
    
    # starting element to make the comparison
    start = 0

    # n = number of total elements in the address
    n = (len(addressListTest) - 1)  
    
    # ending element to make the comparison
    end = n  
    
    keyArray = key_points(start, end, key, addressListTest)

    turnDetector(keyArray, addressListTest, coordinateList)
    
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="increases output verbosity", action="store_true")
    parser.add_argument("-d","--debug", help="logs function info to log file", action="store_true")
    args = parser.parse_args()
    t = time.time()
    t = str(t)
    log = "logs/log-" + t + ".log"
    print(log)
    if (args.verbose):
        f= open(log,"w+")
        f.close()
        FORMAT = "[%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=FORMAT, filename=log,level=logging.INFO)
        print("-v or --verbose flag used, logging mode set to info")
    if (args.debug):
        f= open(log,"w+")
        f.close()
        FORMAT = "[%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=FORMAT, filename=log,level=logging.DEBUG)
        print("-d or --debug flag used, logging mode set to debug")
    else:
        print("no arguments selected")

def getAddress(json_data):
    """Get the address from json response from API"""

    #Return street address, indexed from json argument
    return json_data['StreetAddresses'][0]['StreetAddress']

def sendRequest(completeQuery):
    """Send request to Texas A&M API
    
    Parameters: 
    argument1 (string): Completed request URL to API
    
    Returns:
    json: Reponse from API in json format
    """
    # make the request from API
    response = requests.get(completeQuery)

    # Get the status code from the request.
    responseCode = response.status_code

    # Store json_data as object.
    json_data = json.loads(response.text)

    # log the request URL and reponse code.
    logging.debug("sendRequest() request URL is: %s \n Status Code:%i",completeQuery,responseCode)

    # Return the json data from request.
    return json_data

def formRequestURL(coordinate):
    """Form a request URL from a GPX coordinate as argument.
    
    Parameters: 
    argument1 (gpx point): Coordinate to geocode in request URL
    
    Returns:
    str:Completed query URL to Texas A&M API
    """
    # Convert the GPX point latitude and longitude to strings.
    coordLat = str(coordinate.latitude)
    coordLong = str(coordinate.longitude)

    # URL for Texas A&M Geocoding API
    httpClient = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx?"

    # Format latitude and longitude fields for the request URL
    lat = "lat="
    lon = "&lon="
    lat = lat + coordLat
    lon = lon + coordLong

    # API key field for request URL
    apikey = "&apikey=1553f4ca4c3e4e84a4c22adc3aae1886"
    
    # Format of data from request result
    formatT = "&format=json"
    
    # Choose whether to store 
    notStore = "&notStore=false"
    
    # Verion field for API
    version = "&version=4.10"
    
    # Combine all fields to form complete request URL
    completeQuery = httpClient + lat + lon + apikey + formatT + notStore + version
    
    # Debug log of completed query string
    logging.debug("Complete query: %s",completeQuery)
    
    # Return the query string
    return completeQuery

def getBearing(endPoint, startPoint):
    """Function to determine bearing using start and end GPX points
    
    Parameters: 
    argument1 (gpx point): Ending point
    argument2 (gpx point): Starting point
    
    
    Returns:
    int:Bearing betweeen 2 points in degrees
    """

    # Convert all latitudes and longitudes for GPX point to float and then 
    endLatitude = radians(float(endPoint.latitude))
    endLongitude = radians(float(endPoint.longitude))
    startLatitude = radians(float(startPoint.latitude))
    startLongitude = radians(float(startPoint.longitude))

    # Spherical Law of Cosines determination of bearing
    X = cos(endLatitude) * sin((endLongitude - startLongitude))
    Y = (cos(startLatitude) * sin(endLatitude)) - (sin(startLatitude) 
        * cos(endLatitude) 
        * cos((endLongitude - startLongitude)))
    
    # Convert radians to degrees
    bearingDegrees = degrees(arctan2(X,Y))

    # Normalize result to compass bearing since arctan2 returs values in range
    # of -180 to +180
    bearingDegrees = (bearingDegrees + 360) % 360

    # Log bearing info
    logging.debug("Bearing in degrees is %i", bearingDegrees)

    # Return the bearing
    return bearingDegrees

def getCompassDirection(bearingDegrees):
    """Determines direction on 16 point compass based on bearing in degrees"""
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

    # Return the direction on compass 
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
    distanceReturn = "{0} {1}".format(distance, unit)
    logging.debug("%s",distanceString)
    return distanceReturn

def geocodeCoordinate(endPoint, startPoint):
    # TODO: perhaps change this function to be overload, so you could call with one coordinate
    endLatitude = float(endPoint.latitude)
    endLongitude = float(endPoint.longitude)
    startLatitude = float(startPoint.latitude)
    startLongitude = float(startPoint.longitude)
    queryFields = formRequestURL(endPoint)
    bearing = getBearing(endPoint, startPoint)
    json_data = sendRequest(queryFields)
    address = getAddress(json_data)
    distance = getDistance(endPoint, startPoint)
    logging.debug("Location is (%i,%i)",endLatitude, endLongitude)
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
            return key_points(start, end, key, address)

    # 3 midpoint doesn't match starting and starting point is not next to end point
    if address[start] != address[midpoint] and (start+1) != end:
        # print('case3')
        return key_points(start, end, key, address)

    # 4 starting point matches midpoint
    if address[start] == address[midpoint]:
        # print('case4')
        start = midpoint
        end = n
        return key_points(start,end, key, address)

    # return start, end, key, address

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
        logging.debug("adding address:%s to addressStringList", address)

        # append address to addressStringList
        addressStringList = np.append(addressStringList, address)
    return addressStringList

def multiThreadQueryMaker(coordinateList):
    launcherQueryStringList = []

    for i in range(len(coordinateList)):
        logging.debug("calling formRequestURL on coordinateList index %i, point:(%i,%i)",
        i, coordinateList[i].latitude,coordinateList[i].longitude)
        # convert coordinate to query parameters
        completeQuery = formRequestURL(coordinateList[i])

        # append the completeQuery to launcherQueryStringList
        launcherQueryStringList.append(completeQuery)

    return launcherQueryStringList

def queryRunner(launcherQueryStringList):
    addressList = [None] * len(launcherQueryStringList)
    futures = [None] * len(launcherQueryStringList)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(len(launcherQueryStringList)):
            futures[i] = executor.submit(sendRequest, launcherQueryStringList[i])
    for i in range(len(futures)):
        addressList[i] = getAddress(futures[i].result())
    
        logging.debug("addressList[%i] removing numbers",i)
        
        # shave off the number part of the address
        addressList[i] = addressList[i].split(" ",1)[1]

    logging.debug("address list is: ",addressList)
    return addressList

def bearingDifCalc(startPoint, midPoint, endPoint):
    bearingDelta1 = getBearing(midPoint, startPoint)
    bearingDelta2 = getBearing(endPoint, midPoint)
    totalBearingDelta = bearingDelta2 - bearingDelta1
    logging.debug("change in bearing is: %i = %i - %i",totalBearingDelta, bearingDelta2, bearingDelta1)
    return totalBearingDelta

def turnDetector(turnArray, addressArray, coordinateList):
    # given array of turns point indexes, and matching array of addresses to 
    # array of coordinates, detect what kind of turn happens

    # list to hold directions
    directions = []

    # first direction
    start = "0 miles Start at " + addressArray[0] 

    # append to directions
    directions.append(start)

    for i in turnArray:
        print(i)

    print("turn detector")
    
    # print first direction before loop
    print(directions[0])
    
    for i in range(len(turnArray)):
        if turnArray[i] < len(coordinateList):

            # calculate change in bearing between turn point, and its previous and next point
            bearingDelta = bearingDifCalc(coordinateList[turnArray[i] - 1],
            coordinateList[turnArray[i]], coordinateList[turnArray[i] + 1])

            distance = getDistance(coordinateList[turnArray[i]], coordinateList[turnArray[i - 1]])

            # set the turn direction depending on change in bearing
            if bearingDelta < 0: turn = "Left" 
            elif bearingDelta > 0: turn = "Right"
            
            #print("{0} turn detected of bearingDelta: {1} at addressArray index {2} at address {3} at coordinate({4})".format
            #(turn,bearingDelta,turnArray[i],addressArray[turnArray[i]],coordinateList[turnArray[i]]))

            direction = distance + " " + turn  + " " + "on " + addressArray[turnArray[i]]
            print(direction)
    
    print(directions)

if __name__ == "__main__":
    main()