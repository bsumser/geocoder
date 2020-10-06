import requests
import json
import gpxpy
import gpxpy.gpx
from numpy import arctan2, sin, cos, arccos, degrees, radians

def main():
    gpxParser()

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def sendRequest(queryFields):
    httpClient = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx?"
    completeQuery = httpClient + queryFields
    response = requests.get(completeQuery)
    print(response.status_code)
    jprint(response.json())

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
    print("Bearing in degrees is {0}".format(bearingDegrees))
    return getCompassDirection(bearingDegrees)

def getCompassDirection(bearingDegrees):
    direction = int(round(bearingDegrees / 22.5))
    print(direction)
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

    print("distance from ({0},{1}) to ({2},{3}) is {4} {5}"
    .format(firstLatitude, firstLongitude, secondLatitude, secondLongitude, distance, unit))

def gpxParser():
    curLat = 0      #initiate current latitude and longitude to 0
    curLong = 0
    gpx_file = open('data/sample.gpx','r')

    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1})'.format(point.latitude, point.longitude) + ' heading {0}'.format(getBearing(curLat, curLong, float(point.latitude), float(point.longitude))))
                getDistance(curLat, curLong, float(point.latitude), float(point.longitude))
                #queryFields = getUserInput(point.latitude, point.longitude)
                #sendRequest(queryFields)
                curLat = float(point.latitude)     #update current latitude and longitude
                curLong = float(point.longitude)


if __name__ == "__main__":
    main()