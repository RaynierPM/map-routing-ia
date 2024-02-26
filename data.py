from xml.etree.ElementTree import parse
from grafo import Grafo
from node import node
import haversine as hs
import re
    # Retorna un grafo de los datos que se le hayan ingresado enteriormente por parametros
    # Parametros (archivo) = Nombre/Ruta del archivo que se va a procesar

    # Retorna 2 valores, son:
        # Clase Grafo con lista de adyacencia lista y nodos
        # Xml Element, que contiene las coordenadas limites del mapa cargado por xml
def cargarGrafo(archivo = "santo_domingo.osm"):

    try:
        xml = parse(archivo)
        
        # Arreglo que contendra todos los nodos
        listaNodos = []
        # Itera entre todos los elementos del tipo node/nodo en el XML
        for n in xml.findall("node"):
            tags = []
            # Itera en las etiquetas de los nodos, para luego agregarlas a la clase
            for c in n:
                tags.append({c.get("k"): c.get("v")})
            # Y luego de extraer los datos importantes, es agregada a la lista de nodos
            listaNodos.append(node(n.get("id"), float(n.get("lon")), float(n.get("lat")), tags))

        # Se crea el grafo con los nodos guardados
        nodes = Grafo(listaNodos)

        # Itera entre todos los elementos del tipo way/via en el XML, dichos elementos contienen la relacion entre todos los nodos, delimitando los vecinos
        for way in xml.findall("way"):
            oneway = False
            Agregar = True
            building = False
            for c in way.findall("tag"):
                if c.get('k') == "oneway" and c.get("v") == "yes":
                    oneway = True
                if (c.get("k") == "highway" and c.get("v") == "footway"):
                    Agregar = False
                
                # Actualizacion del estado del nodo, si un nodo esta en parte de los nodos de un edificio, este no sera tomado en cuenta al buscar una ruta
                if (re.search("building*",c.get("k"))) or (c.get("v") == "footway" or c.get("v") == "sidewalk"):
                    building = True 
            
            if Agregar:
                refs = way.findall("nd")
                # Itera en el elemnto nd, que contiene dichas relaciones
                for i in range(len(refs)):
                    # Condiciono el loop para que no se salgan los indexes/indices del arreglo al iterar

                    nodes.find(refs[i].get("ref")).building = building
                    if i < len(refs)-1:
                        # Uso la funcion de la clase nodo, para obtener una tupla con las coordenadas de los datos
                        loc1 = nodes.getLocation(refs[i].get("ref"))
                        loc2 = nodes.getLocation(refs[i+1].get("ref"))
                        # hs.haversine() es una funciona de una libreria que hace el calculo entre puntos geograficos de manera no euclediana, ni por aire (Comprobado)
                        nodes.addVecino(refs[i].get("ref"), refs[i+1].get("ref"), hs.haversine(loc1, loc2))
                        # Si no es una via, agrega los vecinos de manera inversa para que sea de doble via
                        if not oneway:
                            nodes.addVecino(refs[i+1].get("ref"), refs[i].get("ref"), hs.haversine(loc2, loc1))
            
        # Bounds, elemento del XML que contiene los limites(Coordenadas minimas y maximas) del XML/Mapa en cuestion
        infoMapa = xml.find("bounds")
        return nodes, infoMapa
    except:
        print("Ha ocurrido un error")

    