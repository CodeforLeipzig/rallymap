import csv
import hashlib
import json
import os
import requests
import time

script_dir = os.path.dirname(__file__) # Script directory
ORS_API_KEY = os.getenv('ORS_API_KEY')
LEIPZIG = 'Leipzig, '

nominatimUrl = 'https://nominatim.openstreetmap.org/search.php?format=jsonv2&q='
orsGeocodeUrl = f'https://api.openrouteservice.org/geocode/search?api_key={ORS_API_KEY}&text='
orsDirectionsUrl = 'https://api.openrouteservice.org/v2/directions/foot-walking/geojson'

inputCsv = os.path.join(script_dir, '../resources/Versammlungsgeschehen 24.03. bis 27.03.2023_Presse.csv')

print ('Load rallys...')

with open(inputCsv) as csvfile:
  rallysCsv = csv.reader(csvfile, delimiter=';', quotechar='"')
  rallysJson = []

  i = 1
  for rallyCsv in rallysCsv:
    print(f'Resolving route of rally {i}...')
    rallyGeojson = None
    rallyCoordinates = []

    locations = rallyCsv[3].split(', ')

    # only one location is given, use ORS Geocode endpoint to get GeoJSON for rally
    if len(locations) == 1:
      print(f'  Loading GeoJSON for location "{LEIPZIG}{locations[0]}"...')
      orsHeaders = {'Authorization': f'Bearer {ORS_API_KEY}'}
      orsResponse = requests.get(orsGeocodeUrl + LEIPZIG + locations[0], headers=orsHeaders)
      rallyGeojson = json.loads(orsResponse.text)

    # a route is given
    # use Nominatim to get coordinates for locations
    # use coordinates with ORS Directions endpoint to get GeoJSON for rally
    else:
      for location in rallyCsv[3].split(', '):
        print(f'  Resolving coordinates for location "{LEIPZIG}{location}"...')
        time.sleep(1.1)
        nominatimResponse = requests.get(nominatimUrl + LEIPZIG + location)
        responseJson = nominatimResponse.json()
        print('    lat: ' + responseJson[0].get('lat'))
        print('    lon: ' + responseJson[0].get('lon'))
        rallyCoordinates.append([responseJson[0].get('lon'), responseJson[0].get('lat')])

      routeJson = {"coordinates": rallyCoordinates}

      print('  Loading GeoJSON for list of coordinates...')
      orsHeaders = {'Authorization': f'Bearer {ORS_API_KEY}','Content-Type':'application/json'}
      orsResponse = requests.post(orsDirectionsUrl, headers=orsHeaders, data=json.dumps(routeJson))
      rallyGeojson = json.loads(orsResponse.text)

    # remove unnecessary GeoJSON features
    if len(rallyGeojson['features']) > 1:
      del rallyGeojson['features'][1:]

    rallyGeojson['features'][0]['properties']['lfd. Nr'] = rallyCsv[0]
    rallyGeojson['features'][0]['properties']['Datum'] = rallyCsv[1]
    rallyGeojson['features'][0]['properties']['angezeigter Ort / Route'] = rallyCsv[2]
    rallyGeojson['features'][0]['properties']['angezeigte Zeit (von; bis)'] = rallyCsv[4]
    rallyGeojson['features'][0]['properties']['Veranstalter'] = rallyCsv[5]
    rallyGeojson['features'][0]['properties']['Art'] = rallyCsv[6]
    rallyGeojson['features'][0]['properties']['Thema/Motto'] = rallyCsv[7]
    rallyGeojson['features'][0]['properties']['Teilnehmer angezeigt'] = rallyCsv[8]
    rallyGeojson['features'][0]['properties']['colorHex'] = '#' + hashlib.md5(json.dumps(rallyGeojson).encode()).hexdigest()[-6:]

    rallysJson.append(rallyGeojson)

    with open(os.path.join(script_dir, f'../resources/Rally {i} - Versammlungsgeschehen 24.03. bis 27.03.2023_Presse.geojson'), 'w') as f:
      json.dump(rallyGeojson, f, indent=2)

    i = i + 1

  indexHtml = open(os.path.join(script_dir, '../../../docs/index.html'), 'w')
  with open(os.path.join(script_dir, 'index.template.html'), 'r') as htmlTemplate:
    for line in htmlTemplate:
      indexHtml.write(line.replace('var rallys = [];', f'var rallys = {json.dumps(rallysJson)};'))
  indexHtml.close()
