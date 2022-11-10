import json
import pandas as pd
from geopy.geocoders import Nominatim
import sqlite3

conn = sqlite3.connect('ubigeo.sqlite')
cur = conn.cursor()

# cur.execute('''CREATE TABLE IF NOT EXISTS ubigeoperu
#     (nomdpto TEXT, iddpto INTEGER, nomprov TEXT, idprov INTEGER, nomdist TEXT, iddist INTEGER, lat REAL, long REAL, localizacion TEXT, existe INTEGER DEFAULT 1)''')

# datos = []
# with open('ubiperu.json', 'r') as file:
#     data = json.load(file)
#     #len(data['features'])
#     for dpto in range(len(data['features'])):
#         #print(data['features'][dpto]['properties']['NOMBPROV'], data['features'][dpto]['properties']['IDDIST'])
#         nomdpto = data['features'][dpto]['properties']['NOMBDEP']
#         iddpto = data['features'][dpto]['properties']['IDDPTO']
#         nomprov = data['features'][dpto]['properties']['NOMBPROV']
#         idprov = data['features'][dpto]['properties']['IDPROV']
#         nomdist = data['features'][dpto]['properties']['NOMBDIST']
#         iddist = data['features'][dpto]['properties']['IDDIST']
      
#         if (data['features'][dpto]['geometry'] is not None):
#             for geo in range(len(data['features'][dpto]['geometry']['coordinates'][0])):
                
#                 lat = data['features'][dpto]['geometry']['coordinates'][0][geo][1]
#                 lon = data['features'][dpto]['geometry']['coordinates'][0][geo][0]
                
#                 cur.execute('''INSERT OR IGNORE INTO ubigeoperu (nomdpto, iddpto, nomprov, idprov, nomdist, iddist, lat, long, localizacion) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (nomdpto, iddpto, nomprov, idprov, nomdist, iddist, lat, lon, '') )
        
#         conn.commit()
# #                 try:
#                     geolocator = Nominatim(user_agent="MyAppGeo")
#                     lat = data['features'][dpto]['geometry']['coordinates'][0][geo][1]
#                     lon = data['features'][dpto]['geometry']['coordinates'][0][geo][0]
#                     if lat != None and lon != None:
#                         ubic = (lat, lon)
#                         #print(ubic, '-', )
#                         location = geolocator.reverse(ubic)
#                 except IOError as e:
#                     print('error location')
#                 #print(location.address)
#                 else:
#                     datos.append((nomdpto, iddpto, nomprov, idprov, nomdist, iddist, data['features'][dpto]['geometry']['coordinates'][0][geo][1], data['features'][dpto]['geometry']['coordinates'][0][geo][0], (location.address)))            
#                     print( nomdpto, iddpto, nomprov, idprov, nomdist, iddist, data['features'][dpto]['geometry']['coordinates'][0][geo], (location.address) )

# df = pd.DataFrame.from_records(datos, columns =['Dpto', 'IdDpto', 'Provincia', 'IdProv', 'Distrito', 'IdDist','LAT', 'LONG','Zona']) 
# df.to_excel ('UbigeoPER.xls', index = False, header=True)    

cur.execute('''SELECT iddist, lat, long FROM ubigeoperu where existe = 1 limit 5000''')
rows = cur.fetchall()
for ubigeo in rows:
    dist_id = ubigeo[0]
    latitud = ubigeo[1]
    longitud = ubigeo[2]
    print(ubigeo)
    try:
        geolocator = Nominatim(user_agent="MyAppGeo")
        if latitud != None and longitud != None:
            ubic = (latitud, longitud)
            #print(ubic, '-', )
            location = geolocator.reverse(ubic)
    except IOError as e:
            print('error location')
            #print(location.address)
    else:
        cur.execute('''UPDATE ubigeoperu SET localizacion = ?, existe = 0 where iddist = ? and lat = ? and long = ?''', (location.address, dist_id, latitud, longitud ))
        conn.commit()