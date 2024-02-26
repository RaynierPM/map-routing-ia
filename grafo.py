import haversine as hs
from heapq import heappop, heappush
# Clase grafo, que contiene todos los nodos, y los relaciona para usar los datos desde su clase
class Grafo:
    def __init__(self, nodos = []):
        self.listaNodos = {nodo.id:nodo for nodo in nodos}
        self.nodosToDistancia = nodos


    # Ingresa un nodo al grafo
    def push(self, node):
        self.listaNodos[node.id] = node
        self.nodosToDistancia.append(node)

    # Retorna un nodo
    def find(self, id):
        try:
            return self.listaNodos[id]
        except:
            return None

    # Retorna la lista de vecinos
    def getVecinos(self, id):
        return self.find(id).getVecinos()

    # retorna la distancia entre un nodo y otro
    def getDistanciaVecino(self, nodo, vecinoId):
        try:
            return self.find(nodo).getCostos()[vecinoId]
        except:
            return None
    # Funcion de suma importancia que se encarga de agregar la relacion entre los nodos, creando las aristas 
    def addVecino(self, nodoId, vecinoId, distancia = 0):
        if (self.find(nodoId) != None and self.find(vecinoId) != None):
            return self.find(nodoId).addVecino(vecinoId, distancia)
        else:
            raise("Uno de los nodos no existe")            

    # Funcion situacional para saber si son vecino
    def esVecino(self, actual, vecino):
        try:
            self.find(actual).costos[vecino]
            return True
        except:
            return False


    # Funcion que permite obtener una dupla con las coordenadas de un nodo
    def getLocation(self, id):
        try:
            self.listaNodos[id]
            return (self.find(id).lat, self.find(id).lon)
        except:
            return None
    

    # Funcion que retorna el nodo(de calle) mas cercano a la coordenda dada
    # Parametros:
        # Coord: Una tupla con las coordendas geograficas (latitud, longitud)
    # Retorna:
        # Id: ID del nodo(De calle) mas cercano a la coordenada

    # Nota: La coordenada debe ser validada como valida antes de usar la funcion, para evitar errores
    def getNearestNode(self, coord):
        distancias = []
        for nodo in self.nodosToDistancia:
            if not nodo.building:
                distancia = hs.haversine(self.getLocation(nodo.id), coord)
                heappush(distancias, (distancia, nodo.id))
        return heappop(distancias)[1]
