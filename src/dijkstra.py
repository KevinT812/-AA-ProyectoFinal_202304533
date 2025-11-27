"""
Implementación del algoritmo de Dijkstra para caminos más cortos.

El algoritmo de Dijkstra encuentra las rutas más cortas desde un nodo origen
a todos los demás nodos en un grafo con pesos no negativos.
"""

import heapq
import networkx as nx
from utils.graph_utils import leer_grafo_csv, visualizar_grafo


def algoritmo_dijkstra(grafo, nodo_origen):
    """
    Implementa el algoritmo de Dijkstra para encontrar caminos más cortos.
    
    Args:
        grafo (nx.Graph): Grafo no dirigido y ponderado.
        nodo_origen (str): Nodo desde donde calcular las distancias.
    
    Returns:
        tuple: (distancias, predecesores)
            - distancias: Diccionario {nodo: distancia_minima}
            - predecesores: Diccionario {nodo: nodo_anterior} para reconstruir rutas
    
    Complejidad: O((V + E) log V) usando heap binario
        - V: número de vértices
        - E: número de aristas
    """
    if nodo_origen not in grafo.nodes():
        raise ValueError(f"El nodo origen '{nodo_origen}' no existe en el grafo")
    
    # Inicializar distancias y predecesores
    distancias = {nodo: float('inf') for nodo in grafo.nodes()}
    distancias[nodo_origen] = 0
    predecesores = {nodo: None for nodo in grafo.nodes()}
    
    # Heap con tuplas (distancia, nodo)
    heap = [(0, nodo_origen)]
    visitados = set()
    
    while heap:
        dist_actual, nodo_actual = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        # Revisar vecinos
        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                peso_arista = grafo[nodo_actual][vecino]['weight']
                nueva_distancia = dist_actual + peso_arista
                
                # Si encontramos un camino más corto, actualizamos
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(heap, (nueva_distancia, vecino))
    
    return distancias, predecesores


def reconstruir_camino(nodo_destino, predecesores):
    """
    Reconstruye el camino desde el origen hasta un nodo destino.
    
    Args:
        nodo_destino (str): Nodo de destino.
        predecesores (dict): Diccionario de predecesores.
    
    Returns:
        list: Lista de nodos que forman el camino, o None si no hay camino.
    
    Complejidad: O(V) en el peor caso.
    """
    if predecesores[nodo_destino] is None and nodo_destino in predecesores:
        # Si el predecesor es None, verificar si es el nodo origen
        return None
    
    camino = []
    nodo_actual = nodo_destino
    
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = predecesores[nodo_actual]
    
    camino.reverse()
    
    # Si el camino solo tiene un nodo y no es accesible, retornar None
    if len(camino) == 1 and predecesores[camino[0]] is not None:
        return None
    
    return camino


def obtener_aristas_caminos(predecesores, nodo_origen):
    """
    Obtiene todas las aristas que forman parte de los caminos más cortos.
    
    Args:
        predecesores (dict): Diccionario de predecesores.
        nodo_origen (str): Nodo origen.
    
    Returns:
        list: Lista de tuplas (u, v) representando aristas de caminos más cortos.
    
    Complejidad: O(V) donde V es el número de vértices.
    """
    aristas = []
    for nodo, predecesor in predecesores.items():
        if predecesor is not None:
            aristas.append((predecesor, nodo))
    return aristas


def ejecutar_dijkstra(archivo_csv='data/grafo.csv', nodo_origen=None):
    """
    Ejecuta el algoritmo de Dijkstra completo: lectura, procesamiento y visualización.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV con el grafo.
        nodo_origen (str): Nodo desde donde calcular distancias (opcional).
    
    Returns:
        None
    
    Complejidad: O((V + E) log V) dominada por el algoritmo de Dijkstra.
    """
    print("\n" + "="*60)
    print("ALGORITMO DE DIJKSTRA - CAMINOS MÁS CORTOS")
    print("="*60)
    
    try:
        # Leer grafo
        grafo = leer_grafo_csv(archivo_csv)
        print(f"\nGrafo cargado exitosamente")
        print(f"Nodos: {len(grafo.nodes())}")
        print(f"Aristas: {len(grafo.edges())}")
        
        # Si no se especifica origen, pedir al usuario o usar el primero
        if nodo_origen is None:
            nodos_disponibles = list(grafo.nodes())
            print(f"\nNodos disponibles: {', '.join(nodos_disponibles)}")
            nodo_origen = input("Ingrese el nodo origen: ").strip()
            
            if nodo_origen not in grafo.nodes():
                print(f"Nodo '{nodo_origen}' no válido. Usando '{nodos_disponibles[0]}'")
                nodo_origen = nodos_disponibles[0]
        
        # Ejecutar Dijkstra
        distancias, predecesores = algoritmo_dijkstra(grafo, nodo_origen)
        
        # Mostrar resultados
        print(f"\n--- Distancias mínimas desde '{nodo_origen}' ---")
        for nodo in sorted(distancias.keys()):
            dist = distancias[nodo]
            if dist == float('inf'):
                print(f"  {nodo}: ∞ (no alcanzable)")
            else:
                print(f"  {nodo}: {dist:.2f}")
        
        print(f"\n--- Reconstrucción de caminos ---")
        for nodo in sorted(grafo.nodes()):
            if nodo != nodo_origen:
                camino = reconstruir_camino(nodo, predecesores)
                if camino:
                    camino_str = " → ".join(camino)
                    print(f"  {nodo_origen} → {nodo}: {camino_str} (distancia: {distancias[nodo]:.2f})")
                else:
                    print(f"  {nodo_origen} → {nodo}: No hay camino")
        
        # Obtener aristas de caminos más cortos para visualización
        aristas_caminos = obtener_aristas_caminos(predecesores, nodo_origen)
        
        # Generar imagen
        visualizar_grafo(
            grafo,
            aristas_resaltadas=aristas_caminos,
            titulo=f"Caminos Más Cortos - Dijkstra\nDesde nodo: {nodo_origen}",
            archivo_salida="docs/evidencias/dijkstra_paths.png",
            nodo_origen=nodo_origen
        )
        
        print("\n✓ Proceso completado exitosamente")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error al ejecutar Dijkstra: {e}")
        print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_dijkstra()