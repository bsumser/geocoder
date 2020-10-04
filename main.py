import requests
import json
import gpxpy
import gpxpy.gpx

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

def gpxParser():
    gpx_file = open('data/sample.gpx','r')

    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1})'.format(point.latitude, point.longitude))
                queryFields = getUserInput(point.latitude, point.longitude)
                sendRequest(queryFields)


if __name__ == "__main__":
    main()