class node:
    # Es una clase que contendra la informacion mas basica de cada nodo, para luego ser agregada al grafo

    def __init__(self, id, lon, lat, tags):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.tags = tags
        self.vecinos = []
        self.costos = {}
        self.building = True
    
    # Funcion que retorna todos los vecinos previamente agregados al arreglo
    def getVecinos(self):
        return self.vecinos

    # Funcion que retorna todas las distancias
    def getCostos(self):
        return self.costos

    # Agrega relacion entre vecinos
    def addVecino(self, vecinoId, distancia):
        self.vecinos.append (vecinoId)
        self.costos[vecinoId] = distancia
