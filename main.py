import requests
import json
import gpxpy
import gpxpy.gpx
from numpy import arctan2, sin, cos, arccos, degrees, radians

def main():
    path = "data/sample.gpx"
    gpxParser(path)

def getAddress(json_data):    #Get the address from json response from API
    return json_data['StreetAddresses'][0]['StreetAddress']

def sendRequest(queryFields):
    httpClient = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx?"
    completeQuery = httpClient + queryFields
    response = requests.get(completeQuery)
    json_data = json.loads(response.text)
    return(json_data)

def getUserInput(latFloat, longFloat):
    lat = "lat=" + str(latFloat)
    lon = "&lon=" + str(longFloat)
    state = "&state=or"
    apikey = "&apikey=1553f4ca4c3e4e84a4c22adc3aae1886"
    format = "&format=json"
    notStore = "&notStore=false"
    version = "&version=4.10"
    queryFields = lat + lon + state + apikey + format + notStore + version
    return queryFields

def getBearing(firstLatitude, firstLongitude, secondLatitude, secondLongitude):     #Function to determine bearing
    firstLatitude = radians(firstLatitude)
    firstLongitude = radians(firstLongitude)
    secondLatitude = radians(secondLatitude)
    secondLongitude = radians(secondLongitude)
    X = cos(secondLatitude) * sin((secondLongitude - firstLongitude))
    Y = (cos(firstLatitude) * sin(secondLatitude)) - (sin(firstLatitude) * cos(secondLatitude) * cos((secondLongitude - firstLongitude)))
    bearingDegrees = degrees(arctan2(X,Y))
    bearingDegrees = (bearingDegrees + 360) % 360
    print("Bearing in degrees is {0}".format(bearingDegrees))
    return getCompassDirection(bearingDegrees)

def getCompassDirection(bearingDegrees):
    direction = int(round(bearingDegrees / 22.5))
    #print(direction)
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
    #print (choices.get(direction, 'default'))
    return choices.get(direction, 'default')

def getDistance(firstLatitude, firstLongitude, secondLatitude, secondLongitude):  #distance between coordinates using haversine formula
    firstLatitude = radians(firstLatitude)
    firstLongitude = radians(firstLongitude)
    secondLatitude = radians(secondLatitude)
    secondLongitude = radians(secondLongitude)
    unit = "miles"

    distance = 3963.0 * arccos((sin(firstLatitude) * sin(secondLatitude)) +
    cos(firstLatitude) * cos(secondLatitude) * cos(secondLongitude - firstLongitude))

    if (distance < 1):
        distance = int(round(distance * 5280))
        unit = "feet"

    distanceString = " distance from previous point is {0} {1}".format(distance, unit)
    return distanceString

def geocodeCoordinate(endPoint, startPoint):
    endLatitude = float(endPoint.latitude)
    endLongitude = float(endPoint.longitude)
    startLatitude = float(startPoint.latitude)
    startLongitude = float(previousPoint.longitude)
    queryFields = getUserInput(endLatitude, endLongitude)
    bearing = getBearing(startLatitude, startLongitude, endLatitude, endLongitude)
    json_data = sendRequest(queryFields)
    address = getAddress(json_data)
    distance = getDistance(startLatitude, startLongitude, endLatitude, endLongitude)
    print('Location is ({0},{1}) heading {2} at address {3}'.format(endLatitude, endLongitude, bearing, address) + 
    distance)

def gpxParser(path):
    startLatitude = 0      #initiate current latitude and longitude to 0
    startLongitude = 0
    gpx_file = open(path,'r')

    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print("load all lats and longs into array")


if __name__ == "__main__":
    main()