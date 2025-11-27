"""
Implementación del algoritmo de Kruskal para Árbol de Expansión Mínima.

El algoritmo de Kruskal construye un MST ordenando todas las aristas por peso
y agregando iterativamente aristas que no formen ciclos usando Union-Find.
"""

import networkx as nx
from utils.graph_utils import leer_grafo_csv, visualizar_grafo


class UnionFind:
    """
    Estructura de datos Union-Find (Disjoint Set) con path compression.
    
    Permite determinar eficientemente si dos elementos pertenecen al mismo conjunto
    y unir conjuntos.
    """
    
    def __init__(self, elementos):
        """
        Inicializa Union-Find con cada elemento en su propio conjunto.
        
        Args:
            elementos (list): Lista de elementos.
        
        Complejidad: O(n) donde n es el número de elementos.
        """
        self.padre = {elem: elem for elem in elementos}
        self.rango = {elem: 0 for elem in elementos}
    
    def encontrar(self, elemento):
        """
        Encuentra el representante (raíz) del conjunto que contiene el elemento.
        
        Usa path compression para optimizar futuras búsquedas.
        
        Args:
            elemento: Elemento a buscar.
        
        Returns:
            Representante del conjunto.
        
        Complejidad: O(a(n)) amortizada, donde a es la inversa de Ackermann.
        """
        if self.padre[elemento] != elemento:
            self.padre[elemento] = self.encontrar(self.padre[elemento])
        return self.padre[elemento]
    
    def unir(self, elem1, elem2):
        """
        Une los conjuntos que contienen elem1 y elem2.
        
        Usa union by rank para mantener árboles balanceados.
        
        Args:
            elem1: Primer elemento.
            elem2: Segundo elemento.
        
        Returns:
            bool: True si se unieron (estaban en conjuntos diferentes), False si no.
        
        Complejidad: O(a(n)) amortizada.
        """
        raiz1 = self.encontrar(elem1)
        raiz2 = self.encontrar(elem2)
        
        if raiz1 == raiz2:
            return False
        
        # Union by rank
        if self.rango[raiz1] < self.rango[raiz2]:
            self.padre[raiz1] = raiz2
        elif self.rango[raiz1] > self.rango[raiz2]:
            self.padre[raiz2] = raiz1
        else:
            self.padre[raiz2] = raiz1
            self.rango[raiz1] += 1
        
        return True


def algoritmo_kruskal(grafo):
    """
    Implementa el algoritmo de Kruskal para encontrar el Árbol de Expansión Mínima.
    
    Args:
        grafo (nx.Graph): Grafo no dirigido y ponderado.
    
    Returns:
        tuple: (mst_aristas, peso_total)
            - mst_aristas: Lista de tuplas (u, v, peso) del MST
            - peso_total: Peso total del MST
    
    Complejidad: O(E log E) donde E es el número de aristas
        - Dominado por la ordenación de aristas
        - Las operaciones Union-Find son O(E * a(V)) ≈ O(E)
    """
    if len(grafo.nodes()) == 0:
        return [], 0
    
    # Obtener todas las aristas con sus pesos
    aristas = []
    for u, v, datos in grafo.edges(data=True):
        peso = datos['weight']
        aristas.append((peso, u, v))
    
    # Ordenar aristas por peso (O(E log E))
    aristas.sort()
    
    # Inicializar Union-Find
    uf = UnionFind(list(grafo.nodes()))
    
    mst_aristas = []
    peso_total = 0
    
    # Procesar aristas en orden de peso
    for peso, u, v in aristas:
        # Si los nodos están en diferentes componentes, agregar arista
        if uf.unir(u, v):
            mst_aristas.append((u, v, peso))
            peso_total += peso
            
            # Si ya tenemos V-1 aristas, terminamos
            if len(mst_aristas) == len(grafo.nodes()) - 1:
                break
    
    return mst_aristas, peso_total


def ejecutar_kruskal(archivo_csv='data/grafo.csv'):
    """
    Ejecuta el algoritmo de Kruskal completo: lectura, procesamiento y visualización.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV con el grafo.
    
    Returns:
        None
    
    Complejidad: O(E log E) dominada por el algoritmo de Kruskal.
    """
    print("\n" + "="*60)
    print("ALGORITMO DE KRUSKAL - ÁRBOL DE EXPANSIÓN MÍNIMA")
    print("="*60)
    
    try:
        # Leer grafo
        grafo = leer_grafo_csv(archivo_csv)
        print(f"\nGrafo cargado exitosamente")
        print(f"Nodos: {len(grafo.nodes())}")
        print(f"Aristas: {len(grafo.edges())}")
        
        # Ejecutar Kruskal
        mst_aristas, peso_total = algoritmo_kruskal(grafo)
        
        # Mostrar resultados
        print(f"\n--- Resultados del MST (Kruskal) ---")
        print(f"Peso total del MST: {peso_total:.2f}")
        print(f"\nAristas del MST (en orden de selección):")
        for u, v, peso in mst_aristas:
            print(f"  {u} -- {v} : {peso:.2f}")
        
        # Generar imagen
        aristas_mst = [(u, v) for u, v, _ in mst_aristas]
        visualizar_grafo(
            grafo,
            aristas_resaltadas=aristas_mst,
            titulo=f"Árbol de Expansión Mínima - Kruskal\nPeso Total: {peso_total:.2f}",
            archivo_salida="docs/evidencias/kruskal_mst.png"
        )
        
        print("\n✓ Proceso completado exitosamente")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error al ejecutar Kruskal: {e}")
        print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_kruskal()