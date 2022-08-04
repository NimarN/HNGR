from geopy.geocoders import Nominatim
from unicodedata import name
import urllib.request
import json
import ssl

from flaskr.search import results

#define the geolocation function, takes in string location, uses geopy api call, 
# returns latitude and longitude of location as a string

def geoLocate(location):

    geolocator = Nominatim(user_agent="hngr")

    location = geolocator.geocode(location)
    lat = str(location.latitude)
    long = str(location.longitude)
    stringlatLong = lat + ',' + long
    return stringlatLong
    
#Local search function takes the location and type input the user inputs from search 
# and makes a call to Bing maps api to return the Type of business near Location 
#return type is a json object that is passed to the client side javascript 
def localSearch(location, type):
    
    ssl._create_default_https_context = ssl._create_unverified_context
    BingMapsKey = 'AkJ9_GW-rfjfJ_pzoKduCoZ0MTZwdaNwPp9XAWBdBoJ5fT9enMmiIX7k4pZ8KHvd'
    routeUrl = f'https://dev.virtualearth.net/REST/v1/LocalSearch/?query={type}&userLocation={location}&key=' + BingMapsKey
    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)


    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)


    r = response.read().decode(encoding="utf-8")
    result = json.loads(r)

    return result
