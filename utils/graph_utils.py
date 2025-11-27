"""
Utilidades para manejo de grafos.

Este módulo proporciona funciones auxiliares para leer grafos desde archivos CSV
y visualizarlos usando NetworkX y Matplotlib.
"""

import csv
import networkx as nx
import matplotlib.pyplot as plt


def leer_grafo_csv(archivo_csv):
    """
    Lee un grafo no dirigido y ponderado desde un archivo CSV.
    
    El archivo CSV debe tener el formato: origen,destino,peso
    Sin encabezados.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV con los datos del grafo.
    
    Returns:
        nx.Graph: Grafo no dirigido con pesos en las aristas.
    
    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el formato del archivo es incorrecto.
    
    Complejidad: O(E) donde E es el número de aristas.
    """
    grafo = nx.Graph()
    
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if len(fila) != 3:
                    raise ValueError(f"Formato incorrecto en línea: {fila}")
                
                origen = fila[0].strip()
                destino = fila[1].strip()
                peso = float(fila[2].strip())
                
                grafo.add_edge(origen, destino, weight=peso)
        
        return grafo
    
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_csv}' no fue encontrado.")
        raise
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        raise


def visualizar_grafo(grafo, aristas_resaltadas=None, titulo="Grafo", 
                     archivo_salida="grafo.png", nodo_origen=None):
    """
    Visualiza un grafo y guarda la imagen en formato PNG.
    
    Args:
        grafo (nx.Graph): Grafo a visualizar.
        aristas_resaltadas (list): Lista de tuplas (u, v) de aristas a resaltar.
        titulo (str): Título del gráfico.
        archivo_salida (str): Nombre del archivo PNG de salida.
        nodo_origen (str): Nodo origen a resaltar (opcional).
    
    Returns:
        None
    
    Complejidad: O(V + E) donde V es número de vértices y E número de aristas.
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(grafo, seed=42, k=2)
    
    # Dibujar todas las aristas en gris claro
    nx.draw_networkx_edges(
        grafo, pos, edge_color='lightgray', width=2, alpha=0.6
    )
    
    # Resaltar aristas específicas si se proporcionan
    if aristas_resaltadas:
        nx.draw_networkx_edges(
            grafo, pos, edgelist=aristas_resaltadas,
            edge_color='red', width=3
        )
    
    # Dibujar nodos
    colores_nodos = []
    for nodo in grafo.nodes():
        if nodo == nodo_origen:
            colores_nodos.append('lightgreen')
        else:
            colores_nodos.append('lightblue')
    
    nx.draw_networkx_nodes(
        grafo, pos, node_color=colores_nodos, 
        node_size=700, alpha=0.9
    )
    
    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(
        grafo, pos, font_size=12, font_weight='bold'
    )
    
    # Dibujar pesos de aristas
    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(
        grafo, pos, edge_labels=edge_labels, font_size=10
    )
    
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Imagen guardada: {archivo_salida}")