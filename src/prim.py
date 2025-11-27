"""
Implementación del algoritmo de Prim para Árbol de Expansión Mínima.

El algoritmo de Prim construye un MST agregando iterativamente la arista
de menor peso que conecta un vértice en el árbol con uno fuera del árbol.
"""

import heapq
import networkx as nx
from utils.graph_utils import leer_grafo_csv, visualizar_grafo


def algoritmo_prim(grafo, nodo_inicio=None):
    """
    Implementa el algoritmo de Prim para encontrar el Árbol de Expansión Mínima.
    
    Args:
        grafo (nx.Graph): Grafo no dirigido y ponderado.
        nodo_inicio (str): Nodo desde donde iniciar (opcional).
    
    Returns:
        tuple: (mst_aristas, peso_total)
            - mst_aristas: Lista de tuplas (u, v, peso) del MST
            - peso_total: Peso total del MST
    
    Complejidad: O(E log V) usando heap binario
        - E: número de aristas
        - V: número de vértices
    """
    if len(grafo.nodes()) == 0:
        return [], 0
    
    # Si no se especifica nodo inicio, tomar el primero
    if nodo_inicio is None:
        nodo_inicio = list(grafo.nodes())[0]
    
    visitados = set()
    mst_aristas = []
    peso_total = 0
    
    # Heap con tuplas (peso, nodo_actual, nodo_anterior)
    heap = [(0, nodo_inicio, None)]
    
    while heap and len(visitados) < len(grafo.nodes()):
        peso, nodo_actual, nodo_anterior = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        # Agregar arista al MST (excepto para el primer nodo)
        if nodo_anterior is not None:
            mst_aristas.append((nodo_anterior, nodo_actual, peso))
            peso_total += peso
        
        # Agregar vecinos al heap
        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                peso_arista = grafo[nodo_actual][vecino]['weight']
                heapq.heappush(heap, (peso_arista, vecino, nodo_actual))
    
    return mst_aristas, peso_total


def ejecutar_prim(archivo_csv='data/grafo.csv'):
    """
    Ejecuta el algoritmo de Prim completo: lectura, procesamiento y visualización.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV con el grafo.
    
    Returns:
        None
    
    Complejidad: O(E log V) dominada por el algoritmo de Prim.
    """
    print("\n" + "="*60)
    print("ALGORITMO DE PRIM - ÁRBOL DE EXPANSIÓN MÍNIMA")
    print("="*60)
    
    try:
        # Leer grafo
        grafo = leer_grafo_csv(archivo_csv)
        print(f"\nGrafo cargado exitosamente")
        print(f"Nodos: {len(grafo.nodes())}")
        print(f"Aristas: {len(grafo.edges())}")
        
        # Ejecutar Prim
        mst_aristas, peso_total = algoritmo_prim(grafo)
        
        # Mostrar resultados
        print(f"\n--- Resultados del MST (Prim) ---")
        print(f"Peso total del MST: {peso_total:.2f}")
        print(f"\nAristas del MST:")
        for u, v, peso in mst_aristas:
            print(f"  {u} -- {v} : {peso:.2f}")
        
        # Crear grafo MST para visualización
        mst_grafo = nx.Graph()
        for u, v, peso in mst_aristas:
            mst_grafo.add_edge(u, v, weight=peso)
        
        # Generar imagen
        aristas_mst = [(u, v) for u, v, _ in mst_aristas]
        visualizar_grafo(
            grafo, 
            aristas_resaltadas=aristas_mst,
            titulo=f"Árbol de Expansión Mínima - Prim\nPeso Total: {peso_total:.2f}",
            archivo_salida="docs/evidencias/prim_mst.png"
        )
        
        print("\n✓ Proceso completado exitosamente")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error al ejecutar Prim: {e}")
        print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_prim()