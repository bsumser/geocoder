import requests
import json

def main():
    queryFields = getUserInput()
    sendRequest(queryFields)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def sendRequest(queryFields):
    httpClient = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/HTTP/default.aspx?"
    completeQuery = httpClient + queryFields
    response = requests.get(completeQuery)
    print(response.status_code)
    jprint(response.json())

def getUserInput():
    lat = "lat=30.610487"
    lon = "&lon=-96.327766"
    state = "&state=tx"
    apikey = "&apikey=1553f4ca4c3e4e84a4c22adc3aae1886"
    format = "&format=json"
    notStore = "&notStore=false"
    version = "&version=4.10"
    queryFields = lat + lon + state + apikey + format + notStore + version
    return queryFields

if __name__ == "__main__":
    main()