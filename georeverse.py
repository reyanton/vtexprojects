from geopy.geocoders import Nominatim
import pandas as pd

excel_file = 'Ubigeo.xlsx'
df = pd.read_excel(excel_file, convert_float=False)

print(df)

geolocator = Nominatim(user_agent="MyAppGeo")
location = geolocator.reverse("-15.986128858428573, -69.94445310441618")
print(location.address)
ruta = (location.address).split(',')
dist = ruta[len(ruta)-4].upper()
prov = ruta[len(ruta)-3].upper()
print(dist, prov)
dffin = df[df['PROVINCIA'].str.contains(dist)]

# dffin = df[df['PROVINCIA'].str.contains(prov) & df['DISTRITO'].str.contains(dist)]
if len(dffin) > 0: print(dffin)