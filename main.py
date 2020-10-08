import requests
import json
import gpxpy
import gpxpy.gpx
from numpy import arctan2, sin, cos, arccos, degrees, radians

def main():
    path = "data/sample.gpx"
    coordinateList = gpxParser(path)
    queryFields = getUserInput(coordinateList[0])
    #json_data = sendRequest(queryFields)
    #address = getAddress(json_data)
    geocodeCoordinate(coordinateList[0], coordinateList[1])

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
    print('Location is ({0},{1}) heading {2} at address {3}'.format(endLatitude, endLongitude, bearing, address) + 
    distance)

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

if __name__ == "__main__":
    main()