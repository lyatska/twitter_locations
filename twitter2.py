import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


print('')
acct = input('Enter Twitter Account:')

url = twurl.augment(TWITTER_URL,
                    {'screen_name': acct, 'count': '5'})


connection = urllib.request.urlopen(url, context=ctx)
data = connection.read().decode()

js = json.loads(data)
new = []
for u in js['users']:
                    # print(u['screen_name'])
    if u['location'] == "":
        continue
    s = u['location']

    new.append([u['screen_name'],u['location']])




import folium
from geopy.geocoders import Nominatim
coordinates = []
geolocator = Nominatim(user_agent="specify_your_app_name_here", timeout = None,scheme = 'http')

for location in range(len(new)):
    try:

        location3 = geolocator.geocode(new[location][1])
        location3 =   [location3.latitude, location3.longitude]
        coordinates.append([new[location][0],location3])
    except AttributeError:
        continue

map = folium.Map()
twittie = folium.FeatureGroup(name="Twitter locations")
for coord in range(len(coordinates)):
    twittie.add_child(folium.Marker(location= coordinates[coord][1],
                            popup= coordinates[coord][0] + "\n",
                            icon=folium.Icon()))


    map.add_child(twittie)
    map.save('Twitter_locations.html')
