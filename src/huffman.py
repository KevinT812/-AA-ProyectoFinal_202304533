"""
Implementación del algoritmo de Huffman para codificación óptima.

El algoritmo de Huffman construye un código de prefijo óptimo para comprimir datos
asignando códigos más cortos a los caracteres más frecuentes.
"""

import heapq
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx


class NodoHuffman:
    """
    Representa un nodo en el árbol de Huffman.
    
    Attributes:
        caracter (str): Carácter almacenado (None para nodos internos).
        frecuencia (int): Frecuencia del carácter o suma de frecuencias.
        izquierdo (NodoHuffman): Hijo izquierdo.
        derecho (NodoHuffman): Hijo derecho.
    """
    
    def __init__(self, caracter, frecuencia):
        """
        Inicializa un nodo de Huffman.
        
        Args:
            caracter (str): Carácter o None para nodos internos.
            frecuencia (int): Frecuencia del carácter.
        
        Complejidad: O(1)
        """
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierdo = None
        self.derecho = None
    
    def __lt__(self, otro):
        """
        Compara nodos por frecuencia (para el heap).
        
        Args:
            otro (NodoHuffman): Otro nodo a comparar.
        
        Returns:
            bool: True si este nodo tiene menor frecuencia.
        
        Complejidad: O(1)
        """
        return self.frecuencia < otro.frecuencia


def construir_arbol_huffman(texto):
    """
    Construye el árbol de Huffman a partir de un texto.
    
    Args:
        texto (str): Texto a codificar.
    
    Returns:
        NodoHuffman: Raíz del árbol de Huffman.
    
    Complejidad: O(n log n) donde n es el número de caracteres únicos
        - O(n) para contar frecuencias
        - O(n log n) para construir el árbol usando heap
    """
    if not texto:
        return None
    
    # Contar frecuencias de caracteres
    frecuencias = Counter(texto)
    
    # Crear heap con nodos hoja
    heap = []
    for caracter, frecuencia in frecuencias.items():
        nodo = NodoHuffman(caracter, frecuencia)
        heapq.heappush(heap, nodo)
    
    # Construir árbol
    while len(heap) > 1:
        izquierdo = heapq.heappop(heap)
        derecho = heapq.heappop(heap)
        
        # Crear nodo interno
        padre = NodoHuffman(None, izquierdo.frecuencia + derecho.frecuencia)
        padre.izquierdo = izquierdo
        padre.derecho = derecho
        
        heapq.heappush(heap, padre)
    
    return heap[0]


def generar_codigos(nodo, codigo_actual="", codigos=None):
    """
    Genera los códigos de Huffman recorriendo el árbol.
    
    Args:
        nodo (NodoHuffman): Nodo actual del árbol.
        codigo_actual (str): Código binario acumulado.
        codigos (dict): Diccionario para almacenar códigos.
    
    Returns:
        dict: Diccionario {caracter: codigo_binario}
    
    Complejidad: O(n) donde n es el número de nodos en el árbol.
    """
    if codigos is None:
        codigos = {}
    
    if nodo is None:
        return codigos
    
    # Si es hoja, guardar código
    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigo_actual if codigo_actual else "0"
        return codigos
    
    # Recorrer subárboles
    generar_codigos(nodo.izquierdo, codigo_actual + "0", codigos)
    generar_codigos(nodo.derecho, codigo_actual + "1", codigos)
    
    return codigos


def generar_representacion_arbol(nodo, prefijo="", es_izquierdo=True):
    """
    Genera una representación textual del árbol de Huffman.
    
    Args:
        nodo (NodoHuffman): Nodo actual.
        prefijo (str): Prefijo para la visualización.
        es_izquierdo (bool): Indica si es hijo izquierdo.
    
    Returns:
        str: Representación textual del árbol.
    
    Complejidad: O(n) donde n es el número de nodos.
    """
    if nodo is None:
        return ""
    
    resultado = ""
    
    # Símbolo del nodo
    if nodo.caracter is not None:
        etiqueta = f"'{nodo.caracter}'" if nodo.caracter != ' ' else "'espacio'"
        resultado += f"{prefijo}{'└── ' if es_izquierdo else '┌── '}{etiqueta} ({nodo.frecuencia})\n"
    else:
        resultado += f"{prefijo}{'└── ' if es_izquierdo else '┌── '}* ({nodo.frecuencia})\n"
    
    # Extensión del prefijo
    extension = prefijo + ("    " if es_izquierdo else "│   ")
    
    # Recorrer hijos (derecho primero para mejor visualización)
    if nodo.derecho:
        resultado += generar_representacion_arbol(nodo.derecho, extension, False)
    if nodo.izquierdo:
        resultado += generar_representacion_arbol(nodo.izquierdo, extension, True)
    
    return resultado


def visualizar_arbol_huffman(nodo, archivo_salida="huffman_tree.png"):
    """
    Genera una imagen del árbol de Huffman.
    
    Args:
        nodo (NodoHuffman): Raíz del árbol.
        archivo_salida (str): Nombre del archivo PNG de salida.
    
    Returns:
        None
    
    Complejidad: O(n) donde n es el número de nodos.
    """
    grafo = nx.DiGraph()
    pos = {}
    etiquetas = {}
    contador = [0]
    
    def agregar_nodos(nodo, x=0, y=0, capa=1, ancho=4.0):
        """Función auxiliar recursiva para agregar nodos al grafo."""
        if nodo is None:
            return
        
        id_nodo = contador[0]
        contador[0] += 1
        
        # Etiqueta del nodo
        if nodo.caracter is not None:
            etiqueta = f"'{nodo.caracter}'\n{nodo.frecuencia}"
            if nodo.caracter == ' ':
                etiqueta = f"'□'\n{nodo.frecuencia}"
        else:
            etiqueta = f"*\n{nodo.frecuencia}"
        
        grafo.add_node(id_nodo)
        pos[id_nodo] = (x, y)
        etiquetas[id_nodo] = etiqueta
        
        # Agregar hijos
        siguiente_ancho = ancho / 2
        if nodo.izquierdo:
            id_izq = contador[0]
            agregar_nodos(nodo.izquierdo, x - ancho, y - 1, capa + 1, siguiente_ancho)
            grafo.add_edge(id_nodo, id_izq, label='0')
        
        if nodo.derecho:
            id_der = contador[0]
            agregar_nodos(nodo.derecho, x + ancho, y - 1, capa + 1, siguiente_ancho)
            grafo.add_edge(id_nodo, id_der, label='1')
    
    agregar_nodos(nodo)
    
    plt.figure(figsize=(16, 10))
    
    # Dibujar nodos
    nx.draw_networkx_nodes(grafo, pos, node_color='lightblue', 
                          node_size=2000, alpha=0.9)
    
    # Dibujar aristas
    nx.draw_networkx_edges(grafo, pos, edge_color='gray', 
                          arrows=True, arrowsize=20, width=2)
    
    # Etiquetas de nodos
    nx.draw_networkx_labels(grafo, pos, etiquetas, font_size=9, 
                           font_weight='bold')
    
    # Etiquetas de aristas
    edge_labels = nx.get_edge_attributes(grafo, 'label')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels, font_size=10, 
                                 font_color='red')
    
    plt.title("Árbol de Huffman", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Imagen del árbol guardada: {archivo_salida}")


def visualizar_frecuencias(frecuencias, archivo_salida="huffman_freq.png"):
    """
    Genera un gráfico de barras con las frecuencias de caracteres.
    
    Args:
        frecuencias (dict): Diccionario {caracter: frecuencia}.
        archivo_salida (str): Nombre del archivo PNG de salida.
    
    Returns:
        None
    
    Complejidad: O(n log n) por el ordenamiento.
    """
    # Ordenar por frecuencia descendente
    items = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    
    # Tomar los 20 más frecuentes si hay muchos
    if len(items) > 20:
        items = items[:20]
    
    caracteres = []
    freqs = []
    
    for char, freq in items:
        if char == ' ':
            caracteres.append('espacio')
        elif char == '\n':
            caracteres.append('\\n')
        elif char == '\t':
            caracteres.append('\\t')
        else:
            caracteres.append(char)
        freqs.append(freq)
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(caracteres)), freqs, color='steelblue', alpha=0.8)
    plt.xlabel('Caracteres', fontsize=12, fontweight='bold')
    plt.ylabel('Frecuencia', fontsize=12, fontweight='bold')
    plt.title('Frecuencias de Caracteres - Top 20', fontsize=14, fontweight='bold')
    plt.xticks(range(len(caracteres)), caracteres, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Gráfico de frecuencias guardado: {archivo_salida}")


def ejecutar_huffman(archivo_txt='data/texto_huffman.txt'):
    """
    Ejecuta el algoritmo de Huffman completo: lectura, procesamiento y visualización.
    
    Args:
        archivo_txt (str): Ruta al archivo de texto a codificar.
    
    Returns:
        None
    
    Complejidad: O(n log n) donde n es el número de caracteres únicos.
    """
    print("\n" + "="*60)
    print("ALGORITMO DE HUFFMAN - CODIFICACIÓN ÓPTIMA")
    print("="*60)
    
    try:
        # Leer archivo de texto
        with open(archivo_txt, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
        
        print(f"\nArchivo cargado exitosamente")
        print(f"Longitud del texto: {len(texto)} caracteres")
        print(f"Caracteres únicos: {len(set(texto))}")
        
        # Calcular frecuencias
        frecuencias = Counter(texto)
        
        # Construir árbol de Huffman
        arbol = construir_arbol_huffman(texto)
        
        # Generar códigos
        codigos = generar_codigos(arbol)
        
        # Mostrar tabla de códigos
        print(f"\n--- Tabla de Códigos de Huffman ---")
        print(f"{'Carácter':<12} {'Frecuencia':<12} {'Código Binario'}")
        print("-" * 50)
        
        for caracter in sorted(codigos.keys(), key=lambda x: frecuencias[x], reverse=True):
            char_repr = repr(caracter) if caracter in ['\n', '\t', ' '] else f"'{caracter}'"
            print(f"{char_repr:<12} {frecuencias[caracter]:<12} {codigos[caracter]}")
        
        # Calcular eficiencia
        bits_originales = len(texto) * 8
        bits_huffman = sum(frecuencias[c] * len(codigos[c]) for c in codigos)
        tasa_compresion = (1 - bits_huffman / bits_originales) * 100
        
        print(f"\n--- Estadísticas de Compresión ---")
        print(f"Bits originales (8 bits/char): {bits_originales}")
        print(f"Bits con Huffman: {bits_huffman}")
        print(f"Tasa de compresión: {tasa_compresion:.2f}%")
        
        # Representación textual del árbol
        print(f"\n--- Representación del Árbol ---")
        print(generar_representacion_arbol(arbol))
        
        # Generar imágenes
        visualizar_arbol_huffman(arbol, "docs/evidencias/huffman_tree.png")
        visualizar_frecuencias(frecuencias, "docs/evidencias/huffman_freq.png")
        
        print("✓ Proceso completado exitosamente")
        print("="*60 + "\n")
        
    except FileNotFoundError:
        print(f"\n✗ Error: El archivo '{archivo_txt}' no fue encontrado")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ Error al ejecutar Huffman: {e}")
        print("="*60 + "\n")


if __name__ == "__main__":
    ejecutar_huffman()