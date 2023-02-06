from geopy.geocoders import Nominatim


def getLocation(name):
    geolocator = Nominatim(user_agent="volgavit15@mail.ru")
    location = geolocator.geocode(f"{name}")
    lon = location.longitude
    lat = location.latitude
    return lon, lat


