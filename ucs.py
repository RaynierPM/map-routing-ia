from operator import truediv
from priorityQueue import priorityQueue
# Archivo que contiene el algoritmo USC/BCU (Uniform-cost-search/Busqueda de costo uniforme) y funciones para la gestion de la informacion resultante


# Retoruna si un nodo esta en la frontera
def inFrontera(frontera, nodo):
    for fronter in frontera.data:
        if nodo == fronter[1]:
            return True
    return False

# Retoruna si un nodo esta en los explorado
def inExplorados(explorados, nodo):
    try:
        explorados[nodo]
        return True
    except:
        False

# Funcion que toma los nodos explorados y la relacion durante el viaje, para extraer la ruta mas corta de las recorridas o posible
def getRuta(explorados, nodoMeta):
    meta = explorados[nodoMeta]
    rutaNeta = [((meta[0], meta[1]))]

    antecesor = meta[2]
    while True:
        if antecesor != '':
            rutaNeta.append((antecesor, explorados[antecesor][1]))
            antecesor = explorados[antecesor][2]
        else:
            break
    
    rutaNeta.reverse()
    return rutaNeta

# Funcion para retornar la distancia total del recorrido
    # Parametros:
        # Explorados: Arreglo de nodos explorados
        # Modo: "metros"/"milomentros" || Default: Metros
    
    # Retorno:
        # El numero de la distancia total del viaje
    
    # Exception:
        # Retorna None, si el arreglo Explorado no es valido
    
def getDistanciaTotal(ruta, modo = "metros"):
    try:
        if (modo.lower() == "kilometros"):
            d = 1
        else:
            d = 1000
        return ruta[-1][1]*d
    except:
        return None    

# Algoritmo de busqueda uniforme
# Parametros
    # Grafo: varible de tipo grafo que contiene la lista de adyacencia
    # Origen: La id del nodo de origen
    # Meta: La id del nodo meta

# Retorna:
    # Ruta: la ruta mas corta entre los puntos dados

# Excepciones:
    # Puede retornar None, en el caso de que no haya una forma de llegar a dicho nodo
def ucs(grafo, origen, meta):
    if grafo.find(origen) == None or grafo.find(meta) == None:
        raise Exception("Uno de los 2 nodos no existe.")
    # Creo los almacenes de datos, un queue para sacar el minimo siempre, un array para los explorados y una lista para la relacion de rutas en el transcurso
    frontera = priorityQueue()
    explorados = {}

    # Añado el nodo de origen
    frontera.add(origen, 0, "")

    # Mientras la frontera no este vacia
    while not frontera.isEmpty():
        # Saco la info, le nodo actual, la distancia y quien lo expandio
        actual, distancia, expansor = frontera.minPop()
        # Lo agrego a los nodos explorados
        explorados[actual] = (actual, distancia, expansor)
        # Y en el diccionario creo una llave con la id del nodo actual, y con la informacion de quien lo expandio y la distancia acumulada

        # Verifico si llego a la meta, si es true retorno los nodos explorados y las rutas
        if (actual == meta):
            return getRuta(explorados, meta)
        
        # Si un nodo vecino no esta en la frontera o fue explorado, se agrega a la frontera como un nodo en lista de expansion
        # Si el nodo esta en frontera o explorado, y se encuentra en la frontera, se verifica si este nuevo camino tiene menos costo, si es el caso, se edita su antiguo valor y se le da un nuevo costo y se cambia que lo expandio
        for vecino in grafo.getVecinos(actual):
            if not inExplorados(explorados, vecino):
                if not inFrontera(frontera, vecino):
                    frontera.add(vecino, grafo.getDistanciaVecino(actual, vecino) + distancia, actual) 
                elif inFrontera(frontera, vecino):
                    frontera.bajarLlave(vecino, grafo.getDistanciaVecino(actual, vecino) + distancia, actual)
    # Si no hay un camino posible, retorna None
    return None