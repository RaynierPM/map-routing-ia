from os import system
import webbrowser
from data import cargarGrafo
from ucs import getDistanciaTotal, ucs
import folium
from geopy.geocoders import Nominatim
from art import text2art

system("cls")
app = Nominatim(user_agent="tycgis")

p1 = 'Republica Dominicana, Santo Domingo, '

print("Cargando...")
grafo, mapa = cargarGrafo()

system("cls")
print(text2art("Bienvenidos"))
print("""Esta es una app de GPS en desarrollo :D, por favor tener paciencia.

Nota: Solo ubicaciones de Santo Domingo.""")

input("Presiona Enter para continuar: >> ")
system("cls")


while True:
    try:
        #Punto 1
        punto1 = input("Introduze la primera localización de Santo Domingo: >> ")
        localizacion1 = p1 + punto1
        print("Primer punto -> " , localizacion1)
        location1 = app.geocode(localizacion1).raw

        latitude1 = float(location1["lat"])
        if(latitude1 < 18.3956000 or latitude1 > 18.5750000):
            print('Latitud fuera de los limites...Ingrese la direccion otra vez')
            continue
        
        longitude1 = float(location1["lon"])
        if(longitude1 < -70.0965000 or longitude1 > -69.7773000):
            print('Longitud fuera de los limites...Ingrese la direccion otra vez')
            continue
        else:
            break
    except:
        print("Intentelo de nuevo, localidad no reconocida")

while True:
    try:
        #Punto 2
        punto2 = input("Introduze la segunda localización de Santo Domingo: >> ")
        localizacion2 = p1 + punto2
        print("Segundo punto -> " , localizacion2)

        location2 = app.geocode(localizacion2).raw

        latitude2 = float(location2["lat"])
        if(latitude2 < 18.3956000 or latitude2 > 18.5750000):
            print('Latitud fuera de los limites...Ingrese la direccion otra vez')
            continue

        longitude2 = float(location2["lon"])
        if(longitude2 < -70.0965000 or longitude2 > -69.7773000):
            print('Longitud fuera de los limites...Ingrese la direccion otra vez')
            continue
        else:
            break
    except:
        print("Intentelo de nuevo, localidad no reconocida")


origen = (latitude1, longitude1)
destino = (latitude2, longitude2)

origen = grafo.getNearestNode(origen)
destino = grafo.getNearestNode(destino)

system("cls")
print("Buscando la ruta mas corta...")
ruta = ucs(grafo, origen, destino)
if (ruta != None):        
    print("Ruta mas corta encontrada")

    # Extraccion de informacion del mapa
    minlat = float(mapa.get("minlat"))
    minlon = float(mapa.get("minlon"))
    maxlat = float(mapa.get("maxlat"))
    maxlon = float(mapa.get("maxlon"))

    map = folium.Map(location=(18.735693, -70.162651), zoom_start=11)

    coordenadas = [grafo.getLocation(nodo[0]) for nodo in ruta]

    i = 0
    for point in [coordenadas[0], coordenadas[-1]]:
        if i == 0:
            mensaje = "<b>Inicio recorrido</b>"
        else:
            distancia = "{:.2f}".format(getDistanciaTotal(ruta)/1000)
            mensaje = f"<b>Fin del recorrido</b>, <i>distancia: {distancia}Km<i>"
        folium.Marker(point, popup=mensaje).add_to(map)
        i+=1

    folium.PolyLine(coordenadas, opacity=1, weight=3).add_to(map)

    input("Presiona Enter para continuar: >> ")
    map.save("nidea.html")
    webbrowser.open("nidea.html")
else:
    print("No hubo una ruta para los puntos")


