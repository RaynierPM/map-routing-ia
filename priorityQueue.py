import heapq
# Clase de tipo - Estructura de datos- que manipula los datos para sacar del arreglo el dato con  menor costo(Distancia en este contexto)
class priorityQueue:


    def __init__(self):
        self.data = []
    
    def add(self, nodo, distancia, expansor):
        heapq.heappush(self.data, [distancia, nodo, expansor])
        # Formato de array
        # Data[] y contiene otro array [distancia, id] distancia en el index 0 e ID en el index 1

    def minPop(self):
        datos = heapq.heappop(self.data)
        return datos[1], datos[0], datos[2]

    # Retorna el estado binario del queue (Vacio/lleno)
    def isEmpty(self):
        return len(self.data) == 0

    # Si halla un nodo repetido y esta relacion tiene menor  'costo' le cambia la llave
    def bajarLlave(self, nuevoNodo, nuevoValor, expansor):
        for i in range(len(self.data)):
            if (self.data[i][1] == nuevoNodo) and self.data[i][0] > nuevoValor:
                self.data[i][0] = nuevoValor
                self.data[i][2] = expansor
            elif self.data[i][1] == nuevoNodo and self.data[i][0] < nuevoValor:
                break